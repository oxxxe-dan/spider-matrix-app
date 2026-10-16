"""Lance `spider_v12_mt5.py check` avec un garde-fou qui rend tout ordre impossible.

Avant d'exécuter le robot, ce lanceur remplace dans le module MetaTrader5 les
fonctions qui envoient des ordres (order_send, Buy, Sell, Close) par une
fonction qui n'envoie rien : elle note la tentative et renvoie None, comme un
envoi refusé. Le reste (connexion, compte, prix, symboles, order_check) reste
réel et en lecture seule.

Usage (sur le PC, terminal MT5 ouvert) :
    python check_sans_ordre.py chemin\\vers\\spider_v12_mt5.py

Seule la commande `check` est lancée. Code de sortie : celui du robot, ou 3 si
le robot a tenté d'envoyer au moins un ordre (bloqué).
"""

import runpy
import sys
from pathlib import Path

BLOQUEES = ("order_send", "Buy", "Sell", "Close")
CHAMPS_AFFICHES = ("action", "symbol", "volume", "type", "price", "sl", "tp",
                   "deviation", "magic", "position")


def resume(args, kwargs):
    """Résumé de la requête sans commentaire libre ni autre champ."""
    req = args[0] if args and isinstance(args[0], dict) else kwargs
    if not isinstance(req, dict):
        return f"{len(args)} argument(s)"
    return ", ".join(f"{k}={req[k]}" for k in CHAMPS_AFFICHES if k in req) or "requête vide"


def installer_garde_fou(mt5, tentatives):
    for nom in BLOQUEES:
        if not hasattr(mt5, nom):
            continue

        def bloque(*args, _nom=nom, **kwargs):
            tentatives.append((_nom, resume(args, kwargs)))
            print(f"[GARDE-FOU] {_nom} BLOQUÉ, rien n'a été envoyé : {resume(args, kwargs)}",
                  file=sys.stderr, flush=True)
            return None

        setattr(mt5, nom, bloque)


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    script = Path(argv[1]).resolve()
    if not script.is_file():
        print(f"Script introuvable : {script}")
        return 2
    try:
        import MetaTrader5 as mt5
    except ImportError:
        print("Module MetaTrader5 absent (pip install MetaTrader5, sous Windows uniquement).")
        return 2

    tentatives = []
    installer_garde_fou(mt5, tentatives)
    print(f"[GARDE-FOU] actif sur {', '.join(n for n in BLOQUEES if hasattr(mt5, n))}",
          flush=True)

    sys.argv = [str(script), "check"]
    sys.path.insert(0, str(script.parent))
    code = 0
    try:
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        try:
            mt5.shutdown()
        except Exception:
            pass
        print(f"\n[GARDE-FOU] {len(tentatives)} tentative(s) d'ordre bloquée(s).")
        if tentatives:
            print("[GARDE-FOU] La commande check essaie d'envoyer des ordres : "
                  "à corriger avant tout usage sans garde-fou.")
    return 3 if tentatives else code


if __name__ == "__main__":
    # Console Windows ou sortie redirigée : ne jamais planter sur un accent.
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
    sys.exit(main(sys.argv))
