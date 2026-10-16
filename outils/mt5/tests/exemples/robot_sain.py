"""Robot fictif conforme (exemple de test, pas le vrai robot)."""
import os
import sys
import uuid
from pathlib import Path

import MetaTrader5 as mt5

MODE = "demo"
RISK_PER_TRADE_PCT = 0.25
RR = 1.5
MAX_DAILY_LOSS_PCT = 1.0
MAX_TRADES_PER_DAY = 2
MAX_CONSECUTIVE_LOSSES = 3
MAX_LOT = 0.10
ATR_SL_MULT = 1.3
BE_TRIGGER_R = 1.0
BE_OFFSET_POINTS = 2
MAX_SPREAD_POINTS = 20
DEVIATION = 10
STOP_FILE = Path("STOP_SPIDER.txt")
MAGIC = 120012


def connecter():
    ok = mt5.initialize(login=int(os.environ["MT5_LOGIN"]), password=os.environ["MT5_PASSWORD"],
                        server=os.environ["MT5_SERVER"])
    info = mt5.account_info()
    if MODE == "demo" and info.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        sys.exit("compte réel refusé en mode démo")
    return ok


def check():
    connecter()
    info = mt5.account_info()
    print("compte", info.login, "serveur", info.server, "titulaire", info.name)
    print("mot de passe lu :", os.environ["MT5_PASSWORD"])
    print("spread", mt5.symbol_info("XAUUSD").spread, "max", MAX_SPREAD_POINTS)
    if STOP_FILE.exists():
        print("arrêt d'urgence présent")
        return


def envoyer(symbol, lot):
    if mt5.positions_get(symbol=symbol):
        return None
    req = {"action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": min(lot, MAX_LOT),
           "deviation": DEVIATION, "magic": MAGIC, "comment": uuid.uuid4().hex[:12]}
    res = mt5.order_send(req)
    return res.retcode


def run():
    connecter()
    while True:
        if STOP_FILE.exists():
            break
        envoyer("XAUUSD", 0.01)
        break


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "run":
        run()
    elif cmd == "check":
        check()
