"""Contrôle complet du robot MT5, sans aucun ordre, en une commande.

1. Audit statique (le robot n'est pas exécuté).
2. Seulement si l'audit ne trouve aucun envoi d'ordre atteignable depuis
   `check` : lancement de `check` avec le garde-fou (ordres bloqués, sortie
   masquée).

Usage (sur le PC, dans le dossier du robot, terminal MT5 démo ouvert) :
    python controle_complet.py spider_v12_mt5.py

Le rapport est affiché et enregistré dans rapport_controle.txt, prêt à être
collé dans la conversation (identifiant, serveur et mot de passe masqués).
"""

import os
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from check_sans_ordre import masquer, valeurs_env_sensibles  # noqa: E402

DUREE_MAX_CHECK = 300  # secondes
RAISONS_REFUS = {
    2: "fichier du robot illisible",
    3: "d'après le code, `check` peut envoyer un ordre",
    4: "aiguillage de `check` introuvable dans le code : lecture humaine nécessaire",
}


def lancer(args, cwd):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, *args], cwd=cwd, env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          timeout=DUREE_MAX_CHECK)


def main(argv):
    script = Path(argv[1] if len(argv) > 1 else "spider_v12_mt5.py").resolve()
    if not script.is_file():
        print(f"Script introuvable : {script}")
        return 2

    parties = [f"Contrôle complet — {script.name} — Python {sys.version.split()[0]}", ""]
    audit = lancer([str(ICI / "audit_statique.py"), str(script)], cwd=script.parent)
    parties += ["===== 1. Audit statique =====", audit.stdout, audit.stderr]

    code = audit.returncode
    if code in RAISONS_REFUS:
        parties.append(f"===== 2. check NON LANCÉ : {RAISONS_REFUS[code]} =====")
    else:
        try:
            check = lancer([str(ICI / "check_sans_ordre.py"), str(script)], cwd=script.parent)
            parties += [f"===== 2. check avec garde-fou (code de sortie {check.returncode}) =====",
                        check.stdout, check.stderr]
            code = check.returncode
        except subprocess.TimeoutExpired:
            parties.append(f"===== 2. check ARRÊTÉ au bout de {DUREE_MAX_CHECK} s "
                           "(ne rend pas la main) =====")
            code = 5

    texte = masquer("\n".join(p for p in parties if p is not None), valeurs_env_sensibles())
    Path("rapport_controle.txt").write_text(texte, encoding="utf-8")
    print(texte)
    print("\nRapport enregistré dans rapport_controle.txt (à coller dans la conversation).")
    return code


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    sys.exit(main(sys.argv))
