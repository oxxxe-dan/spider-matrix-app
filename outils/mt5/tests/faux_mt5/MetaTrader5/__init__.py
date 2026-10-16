"""Faux module MetaTrader5 pour les tests sous Linux. N'envoie rien nulle part."""
import os
from types import SimpleNamespace

ACCOUNT_TRADE_MODE_DEMO = 0
ACCOUNT_TRADE_MODE_REAL = 2
TRADE_ACTION_DEAL = 1
ORDER_TYPE_BUY = 0
TRADE_RETCODE_DONE = 10009
TEMOIN = os.environ.get("FAUX_MT5_TEMOIN", "ordre_envoye.txt")


def initialize(*a, **k):
    return True


def shutdown():
    return None


def account_info():
    return SimpleNamespace(login=55550001, server="Faux-Demo-Serveur", name="Titulaire Fictif",
                           trade_mode=ACCOUNT_TRADE_MODE_DEMO, balance=10000.0)


def symbol_info(symbol):
    return SimpleNamespace(spread=12, point=0.01, visible=True)


def positions_get(**k):
    return ()


def order_send(request):
    # Témoin : si ce fichier apparaît, un « ordre » est passé malgré le garde-fou.
    with open(TEMOIN, "a") as f:
        f.write(repr(request) + "\n")
    return SimpleNamespace(retcode=TRADE_RETCODE_DONE)


def Buy(symbol, volume):
    return order_send({"action": TRADE_ACTION_DEAL, "symbol": symbol, "volume": volume,
                       "type": ORDER_TYPE_BUY})
