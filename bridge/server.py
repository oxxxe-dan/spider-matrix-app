"""Spider Matrix collaboration bridge: Claude/ChatGPT shared MCP tools.

Safety contract:
- Does not call broker APIs or send orders.
- Does not change Spider Matrix V12 or its parameters.
- StrategyTune data is read from exported JSON reports; no undocumented API assumed.
"""
from __future__ import annotations

import base64
import hmac
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

APP_NAME = "Spider Matrix Collaboration Bridge"
REPO = os.getenv("GITHUB_REPO", "oxxxe-dan/spider-matrix-app")
REF = os.getenv("GITHUB_REF", "bridge/chatgpt-claude-strategytune")
REPORT_DIR = Path(os.getenv("STRATEGYTUNE_REPORT_DIR", "data/strategytune_reports"))
INBOX_DIR = Path(os.getenv("RESEARCH_INBOX_DIR", "data/research_inbox"))
MAX_NOTE_CHARS = 12000
mcp = FastMCP(APP_NAME)


def _safe_json_files(directory: Path) -> list[dict[str, Any]]:
    if not directory.exists():
        return []
    result: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json"), key=lambda p: p.name):
        if path.is_file() and not path.is_symlink():
            try:
                stat = path.stat()
                result.append({
                    "filename": path.name,
                    "size_bytes": stat.st_size,
                    "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                })
            except OSError:
                continue
    return result


@mcp.tool()
def bridge_status() -> dict[str, Any]:
    """Return bridge health, enabled integrations, and safety boundaries."""
    return {
        "name": APP_NAME,
        "status": "ready",
        "utc": datetime.now(timezone.utc).isoformat(),
        "github_repo": REPO,
        "github_ref": REF,
        "strategytune_export_directory": str(REPORT_DIR),
        "strategytune_reports_available": len(_safe_json_files(REPORT_DIR)),
        "github_read": "configured (read-only)",
        "strategytune_connection": "JSON export/import only; no public API assumed",
        "broker_execution": "disabled",
        "spider_matrix_v12_mutations": "disabled",
        "parameter_changes": "proposal-only; never applied",
    }


@mcp.tool()
def list_strategy_reports() -> list[dict[str, Any]]:
    """List StrategyTune JSON reports exported into the bridge's report directory."""
    return _safe_json_files(REPORT_DIR)


@mcp.tool()
def read_strategy_report(filename: str) -> dict[str, Any]:
    """Read one exported StrategyTune JSON report by filename."""
    if Path(filename).name != filename or not filename.endswith(".json"):
        raise ValueError("Use a single .json filename; paths are not accepted.")
    target = (REPORT_DIR / filename).resolve()
    if target.parent != REPORT_DIR.resolve() or not target.is_file() or target.is_symlink():
        raise FileNotFoundError("Report not found in the configured StrategyTune export directory.")
    if target.stat().st_size > 2_000_000:
        raise ValueError("Report exceeds the 2 MB read limit.")
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Report is not valid JSON.") from exc


@mcp.tool()
def submit_research_note(title: str, body: str, source: str = "assistant", confidence: str = "unverified") -> dict[str, Any]:
    """Save a research note for cross-assistant review; it does not change code or trading settings."""
    title = title.strip()
    body = body.strip()
    if not title or len(title) > 200:
        raise ValueError("Title must contain 1–200 characters.")
    if not body or len(body) > MAX_NOTE_CHARS:
        raise ValueError(f"Body must contain 1–{MAX_NOTE_CHARS} characters.")
    if source not in {"chatgpt", "claude", "human", "assistant"}:
        raise ValueError("source must be chatgpt, claude, human, or assistant.")
    if confidence not in {"unverified", "hypothesis", "tested", "validated"}:
        raise ValueError("Unsupported confidence label.")
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc)
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", title).strip("-").lower()[:50] or "note"
    filename = f"{stamp.strftime('%Y%m%dT%H%M%SZ')}-{slug}.json"
    record = {
        "title": title,
        "body": body,
        "source": source,
        "confidence": confidence,
        "created_utc": stamp.isoformat(),
        "status": "pending_review",
        "applies_to_live_system": False,
    }
    target = INBOX_DIR / filename
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"saved": True, "filename": filename, "status": "pending_review", "live_system_changed": False}


@mcp.tool()
def list_research_notes() -> list[dict[str, Any]]:
    """List pending cross-assistant notes; no note is automatically applied."""
    return _safe_json_files(INBOX_DIR)


@mcp.tool()
def read_github_document(path: str) -> dict[str, Any]:
    """Read an allowlisted shared project document from the configured GitHub repo/ref."""
    normalized = path.strip().lstrip("/")
    if ".." in Path(normalized).parts or normalized.startswith(".github/"):
        raise ValueError("Path is not allowed.")
    if not (normalized == "README.md" or normalized.startswith("docs/") or normalized.startswith("bridge_shared/")):
        raise ValueError("Only README.md, docs/*, and bridge_shared/* are readable through this tool.")
    url = f"https://api.github.com/repos/{REPO}/contents/{quote(normalized, safe='/')}"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, params={"ref": REF}, timeout=15)
    if response.status_code == 404:
        raise FileNotFoundError(f"GitHub document not found: {normalized}")
    response.raise_for_status()
    payload = response.json()
    if payload.get("type") != "file" or "content" not in payload:
        raise ValueError("The requested GitHub path is not a readable text file.")
    raw = base64.b64decode(payload["content"])
    if len(raw) > 1_000_000:
        raise ValueError("Document exceeds the 1 MB read limit.")
    return {
        "path": normalized,
        "repo": REPO,
        "ref": REF,
        "content": raw.decode("utf-8"),
        "html_url": payload.get("html_url"),
        "read_only": True,
    }


app = mcp.streamable_http_app()


class BearerAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.rstrip("/") == "/healthz":
            return JSONResponse({"status": "ok", "service": APP_NAME})
        expected = os.getenv("BRIDGE_API_TOKEN", "")
        if len(expected) < 32:
            return JSONResponse(
                {"error": "Bridge is not configured: set BRIDGE_API_TOKEN to a random secret of at least 32 characters."},
                status_code=503,
            )
        supplied = request.headers.get("authorization", "")
        if not supplied.startswith("Bearer ") or not hmac.compare_digest(supplied[7:], expected):
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)


app.add_middleware(BearerAuthMiddleware)


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))
