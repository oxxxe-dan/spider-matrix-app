# Spider Matrix collaboration bridge (isolated scaffold)

This service is a separate MCP service. It is **not** Spider Matrix V12 and must not be deployed over the existing V12 app.

## Safety boundary
- No broker connection or order-execution tool is implemented.
- No V12 deployment or parameter mutation is implemented.
- StrategyTune results are imported as JSON exports; this scaffold does not assume an undocumented StrategyTune API.
- Research notes are saved as pending review only. They never apply themselves to code, strategy parameters, or live trading.
- The MCP HTTP endpoint requires a bearer token of at least 32 characters. Store the token only in the host's secret manager.

## Tools exposed
- `bridge_status`: service state and safety boundaries.
- `read_github_document`: read-only access to allowlisted shared documents in README.md, docs/, or bridge_shared/.
- `list_strategy_reports` / `read_strategy_report`: read exported StrategyTune JSON reports.
- `submit_research_note`: write a review note to the bridge's local inbox, not to Spider Matrix V12.
- `list_research_notes`: list saved note files.

## Local run
1. Use Python 3.12.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set `BRIDGE_API_TOKEN` to a randomly generated secret (32+ characters). Never commit the real secret.
4. Set environment variables in the shell or a local dotenv loader (the app intentionally does not auto-load .env).
5. Run: `python server.py`.
6. Health check: `GET /healthz`.
7. MCP endpoint: `/mcp`, with `Authorization: Bearer <token>`.

## StrategyTune workflow
1. Run a backtest in the existing StrategyTune workspace.
2. Export its report as JSON using the platform's supported UI/export route.
3. Place the JSON file in `data/strategytune_reports/` on the bridge host (or mount that folder as persistent storage).
4. Ask either assistant to read the report via MCP tools.
5. Both assistants may submit research notes; a human reviews them before any code or parameter change.

StrategyTune workspace: https://strategytune.com/app

## Claude connection
For Claude.ai, add the deployed HTTPS MCP endpoint under Settings → Connectors → Add custom connector, then configure the bearer/OAuth authentication supported by the deployment. The endpoint must be reachable over HTTPS. Do not expose an unauthenticated public endpoint.

For Claude Messages API use, Anthropic documents remote MCP servers via the `mcp_servers` parameter and a matching `mcp_toolset` tool. Check current account/model availability and required beta headers in Anthropic's current docs.

## ChatGPT connection
ChatGPT's built-in GitHub and StrategyTune connectors remain separate from this service. To have ChatGPT call this custom MCP service directly, configure it through a supported ChatGPT MCP/app integration or use a small orchestration backend that calls the OpenAI API and Claude API. This repository scaffold does not itself grant this chat a new MCP connection.

## Deployment checklist
- Deploy as a **new, separate service**, never as the existing Spider Matrix V12 deployment.
- Configure HTTPS, persistent storage for reports/inbox, and a secret named `BRIDGE_API_TOKEN`.
- Use a GitHub token with read-only contents permission if required.
- Set resource limits and request logging without logging bearer tokens or report secrets.
- Test unauthorized requests return 401 and that no trading endpoint exists.
- Keep live trading disabled.
