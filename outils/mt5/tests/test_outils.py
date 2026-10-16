"""Tests des outils MT5 (Linux, faux module MetaTrader5, aucun terminal)."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ICI = Path(__file__).resolve().parent
OUTILS = ICI.parent
EXEMPLES = ICI / "exemples"


def lancer(*args, cwd):
    env = dict(os.environ, PYTHONPATH=str(ICI / "faux_mt5"), MT5_LOGIN="55550001",
               MT5_PASSWORD="faux-secret-env", MT5_SERVER="Faux-Demo-Serveur",
               PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, *args], cwd=cwd, env=env,
                          capture_output=True, text=True, encoding="utf-8")


class AuditStatique(unittest.TestCase):
    def audit(self, nom):
        return lancer(str(OUTILS / "audit_statique.py"), str(EXEMPLES / nom), cwd=ICI)

    def test_robot_sain(self):
        r = self.audit("robot_sain.py")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("NON d'après l'analyse", r.stdout)
        self.assertNotIn("ÉCART", r.stdout)
        self.assertNotIn("ABSENT", r.stdout)
        self.assertNotIn("SECRET EN CLAIR", r.stdout)
        self.assertIn("variables d'environnement", r.stdout)
        self.assertIn("ACCOUNT_TRADE_MODE_DEMO", r.stdout)
        self.assertIn("dans une boucle", r.stdout)
        self.assertIn("vérifie avant : positions_get", r.stdout)

    def test_robot_dangereux(self):
        r = self.audit("robot_dangereux.py")
        self.assertEqual(r.returncode, 3, r.stdout)
        self.assertIn("OUI, appel d'ordre atteignable", r.stdout)
        self.assertIn("tester_ordre → order_send", r.stdout)
        self.assertIn("SECRET EN CLAIR", r.stdout)
        self.assertIn("FUITE POSSIBLE", r.stdout)
        self.assertIn("DANS UNE BOUCLE", r.stdout)
        self.assertIn("ÉCART", r.stdout)
        # La valeur du secret ne doit jamais apparaître.
        self.assertNotIn("faux-mot-de-passe-de-test", r.stdout)
        self.assertNotIn("12345678", r.stdout)


    def test_secret_seul_code_1(self):
        r = self.audit("robot_secret.py")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertNotIn("autre-faux-mot-de-passe", r.stdout)

    def test_check_introuvable_code_4(self):
        r = self.audit("robot_sans_check.py")
        self.assertEqual(r.returncode, 4, r.stdout)
        self.assertIn("INDÉTERMINÉ", r.stdout)


class CheckSansOrdre(unittest.TestCase):
    def lancer_check(self, nom):
        with tempfile.TemporaryDirectory() as d:
            r = lancer(str(OUTILS / "check_sans_ordre.py"), str(EXEMPLES / nom), cwd=d)
            return r, (Path(d) / "ordre_envoye.txt").exists()

    def test_robot_sain_aucune_tentative(self):
        r, envoye = self.lancer_check("robot_sain.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("0 tentative(s)", r.stdout)
        self.assertFalse(envoye)
        # Compte, serveur, titulaire et mot de passe masqués.
        for secret in ("55550001", "Faux-Demo-Serveur", "Titulaire Fictif", "faux-secret-env"):
            self.assertNotIn(secret, r.stdout + r.stderr)
        self.assertIn("compte *** serveur *** titulaire ***", r.stdout)

    def test_robot_dangereux_tout_bloque(self):
        r, envoye = self.lancer_check("robot_dangereux.py")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("3 tentative(s)", r.stdout)
        self.assertIn("order_send BLOQUÉ", r.stderr)
        self.assertIn("Buy BLOQUÉ", r.stderr)
        self.assertFalse(envoye, "un ordre a traversé le garde-fou")

    def test_sans_garde_fou_le_temoin_fonctionne(self):
        # Contrôle du test lui-même : sans garde-fou, le faux module écrit bien le témoin.
        with tempfile.TemporaryDirectory() as d:
            lancer(str(EXEMPLES / "robot_dangereux.py"), "check", cwd=d)
            self.assertTrue((Path(d) / "ordre_envoye.txt").exists())


class ControleComplet(unittest.TestCase):
    def controle(self, nom):
        with tempfile.TemporaryDirectory() as d:
            r = lancer(str(OUTILS / "controle_complet.py"), str(EXEMPLES / nom), cwd=d)
            rapport = (Path(d) / "rapport_controle.txt").read_text(encoding="utf-8")
            return r, rapport, (EXEMPLES / "ordre_envoye.txt").exists()

    def test_robot_sain_check_lance(self):
        r, rapport, envoye = self.controle("robot_sain.py")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("2. check avec garde-fou", rapport)
        self.assertIn("0 tentative(s)", rapport)
        self.assertNotIn("55550001", rapport)
        self.assertFalse(envoye)

    def test_robot_dangereux_check_non_lance(self):
        r, rapport, envoye = self.controle("robot_dangereux.py")
        self.assertEqual(r.returncode, 3, r.stdout)
        self.assertIn("check NON LANCÉ", rapport)
        self.assertNotIn("GARDE-FOU] actif", rapport)
        self.assertFalse(envoye)

    def test_robot_sans_check_non_lance(self):
        r, rapport, _ = self.controle("robot_sans_check.py")
        self.assertEqual(r.returncode, 4, r.stdout)
        self.assertIn("check NON LANCÉ", rapport)

    def test_secret_en_clair_check_lance(self):
        r, rapport, _ = self.controle("robot_secret.py")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("À CORRIGER", rapport)
        self.assertIn("connexion ok", rapport)


if __name__ == "__main__":
    unittest.main()
