"""Robot fictif fautif (exemple de test, pas le vrai robot)."""
import sys

import MetaTrader5 as mt5

PASSWORD = "faux-mot-de-passe-de-test"
MT5_LOGIN = 12345678
RISK = 1.0
LOT_MAX = 0.5


def tester_ordre():
    print("mot de passe", PASSWORD)
    for _ in range(2):
        r = mt5.order_send({"action": 1, "symbol": "XAUUSD", "volume": LOT_MAX})
        if r is None:
            continue
    mt5.Buy("EURUSD", 0.01)


COMMANDES = {"check": tester_ordre}

if __name__ == "__main__":
    mt5.initialize(login=MT5_LOGIN, password=PASSWORD)
    COMMANDES[sys.argv[1]]()
