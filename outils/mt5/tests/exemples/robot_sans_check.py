"""Robot fictif sans commande check reconnaissable (exemple de test)."""
import sys

import MetaTrader5 as mt5

if __name__ == "__main__":
    getattr(mt5, sys.argv[1])()
