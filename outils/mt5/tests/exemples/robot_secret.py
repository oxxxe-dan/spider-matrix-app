"""Robot fictif : check sans ordre, mais mot de passe écrit en clair (exemple de test)."""
import sys

import MetaTrader5 as mt5

MT5_PASSWORD = "autre-faux-mot-de-passe"

if __name__ == "__main__":
    if sys.argv[1] == "check":
        mt5.initialize(password=MT5_PASSWORD)
        print("connexion ok")
