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

Tout ce que le robot affiche passe par un masque : numéro de compte, serveur,
nom du titulaire et valeurs des variables d'environnement sensibles (mot de
passe, identifiant, serveur, jeton) sont remplacés par ***. La sortie peut
donc être collée telle quelle dans la conversation.
"""

import os
import re
import runpy
import sys
import traceback
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


VARIABLES_SENSIBLES = re.compile(r"(PASS|PWD|MDP|LOGIN|SERVER|SERVEUR|TOKEN|SECRET|KEY|COMPTE)",
                                 re.I)
LONGUEUR_MIN = 4  # en dessous, masquer abîmerait la sortie (chiffres courants)


def valeurs_env_sensibles():
    return {v for k, v in os.environ.items()
            if VARIABLES_SENSIBLES.search(k) and len(v) >= LONGUEUR_MIN}


def masquer(texte, valeurs):
    for v in sorted(valeurs, key=len, reverse=True):
        texte = texte.replace(v, "***")
    return texte


class FluxMasque:
    """Enveloppe stdout/stderr : masque les valeurs sensibles avant affichage."""

    def __init__(self, flux, mt5, valeurs):
        self._flux, self._mt5, self._valeurs = flux, mt5, valeurs
        self._compte_lu = False

    def _lire_compte(self):
        if self._compte_lu:
            return
        try:
            info = self._mt5.account_info()  # lecture seule ; None tant que non connecté
        except Exception:
            info = None
        if info is not None:
            self._compte_lu = True
            for champ in ("login", "server", "name"):
                v = getattr(info, champ, None)
                if v not in (None, "") and len(str(v)) >= LONGUEUR_MIN:
                    self._valeurs.add(str(v))

    def write(self, texte):
        self._lire_compte()
        return self._flux.write(masquer(texte, self._valeurs))

    def flush(self):
        self._flux.flush()

    def __getattr__(self, nom):
        return getattr(self._flux, nom)


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

    valeurs = valeurs_env_sensibles()
    vrais_flux = sys.stdout, sys.stderr
    sys.stdout = FluxMasque(sys.stdout, mt5, valeurs)
    sys.stderr = FluxMasque(sys.stderr, mt5, valeurs)
    sys.argv = [str(script), "check"]
    sys.path.insert(0, str(script.parent))
    code = 0
    try:
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    except Exception:
        traceback.print_exc()  # passe par le masque
        code = 1
    finally:
        try:
            mt5.shutdown()
        except Exception:
            pass
        print(f"\n[GARDE-FOU] {len(tentatives)} tentative(s) d'ordre bloquée(s).")
        if tentatives:
            print("[GARDE-FOU] La commande check essaie d'envoyer des ordres : "
                  "à corriger avant tout usage sans garde-fou.")
        sys.stdout.flush()
        sys.stdout, sys.stderr = vrais_flux
    return 3 if tentatives else code


if __name__ == "__main__":
    # Console Windows ou sortie redirigée : ne jamais planter sur un accent.
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
    sys.exit(main(sys.argv))
