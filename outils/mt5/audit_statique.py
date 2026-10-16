"""Audit statique du robot MT5 (Spider Matrix V12) — lecture seule.

Lit le script cible comme du texte et l'analyse avec `ast`. Le script n'est
jamais importé ni exécuté : aucune connexion MT5, aucun ordre possible.

Usage (sur le PC, dans le dossier du robot) :
    python audit_statique.py spider_v12_mt5.py

Les secrets éventuellement trouvés dans le code ne sont jamais affichés :
seuls le nom de la variable et la ligne sont indiqués.

Code de sortie (le plus grave l'emporte) :
    3  `check` peut atteindre un envoi d'ordre : ne pas lancer `check`
    4  aiguillage de `check` introuvable : ne pas lancer `check` avant lecture
    1  secret écrit en clair dans le code (`check` peut tourner)
    0  rien de bloquant détecté
    2  fichier illisible
"""

import ast
import re
import sys
from pathlib import Path

COMMANDE = "check"
APPELS_ORDRE = {"order_send", "Buy", "Sell", "Close"}

# Limites du robot de référence (registre des décisions : C1 et section 27 pour le risque,
# 0,25 % en démo et en réel ; C2 pour le R:R).
# Plusieurs valeurs acceptées quand le code peut exprimer un pourcentage en fraction.
LIMITES = [
    ("Risque par trade", "0,25 %", {0.25, 0.0025}),
    ("R:R", "1,50", {1.5}),
    ("Perte journalière max", "1 %", {1.0, 0.01}),
    ("Trades par jour", "2", {2}),
    ("Pertes consécutives max", "3", {3}),
    ("Lot max", "0,10", {0.1}),
    ("Stop ATR ×", "1,30", {1.3}),
    ("Break-even (déclenchement en R)", "1 R", {1.0}),
    ("Break-even (marge en points)", "+2 points", {2}),
    ("Spread max (points)", "20", {20}),
    ("Déviation (points)", "10", {10}),
]

MOTS_SECRETS = ("password", "passwd", "pwd", "mdp", "motdepasse", "secret", "token", "apikey")


def nom_secret(n, valeur):
    """Vrai si une variable de ce nom, avec cette valeur littérale, ressemble à un secret."""
    if valeur in (None, "", 0) or isinstance(valeur, bool):
        return False
    if any(m in n for m in MOTS_SECRETS):
        return True
    if n.endswith("login") and isinstance(valeur, (int, str)):
        return True
    return n.endswith(("server", "serveur")) and isinstance(valeur, str)
MOTS_ARRET = re.compile(r"(stop|kill|arret|arrêt|urgence|halt|panic)", re.I)


def norm(nom):
    return re.sub(r"[^a-z0-9]", "", nom.lower())


def a_un(n, *mots):
    return any(m in n for m in mots)


def regle_limite(n):
    """Associe un nom de variable normalisé à une limite (index dans LIMITES)."""
    if a_un(n, "day", "daily", "jour", "journ") and a_un(n, "loss", "perte", "dd", "drawdown",
                                                         "risk", "risque"):
        return 2
    if a_un(n, "consec", "streak", "row", "suite", "serie") and a_un(n, "loss", "perte"):
        return 4
    if n in ("maxlosses", "maxpertes"):
        return 4
    if "trade" in n and a_un(n, "day", "daily", "jour") and not a_un(n, "loss", "perte"):
        return 3
    if "breakeven" in n or (n.startswith("be") and not n.startswith(("beta", "before", "best", "betsize"))):
        return 8 if a_un(n, "off", "buffer", "point", "pts", "plus", "lock", "pip") else 7
    if n.startswith("rr") or n.endswith("rr") or a_un(n, "riskreward", "rewardrisk"):
        return 1
    if (a_un(n, "risk", "risque") and not a_un(n, "total", "global", "reward")):
        return 0
    if "lot" in n and "max" in n:
        return 5
    if "atr" in n and a_un(n, "sl", "stop", "mult"):
        return 6
    if "spread" in n and "max" in n:
        return 9
    if a_un(n, "deviation", "slippage"):
        return 10
    return None


def est_nombre(v):
    return (isinstance(v, ast.Constant) and isinstance(v.value, (int, float))
            and not isinstance(v.value, bool))


def nom_cible(t):
    if isinstance(t, ast.Name):
        return t.id
    if isinstance(t, ast.Attribute):
        return t.attr
    return None


def nom_appel(c):
    return nom_cible(c.func) if isinstance(c, ast.Call) else None


class Audit:
    def __init__(self, source):
        self.arbre = ast.parse(source)
        self.parents = {}
        for p in ast.walk(self.arbre):
            for e in ast.iter_child_nodes(p):
                self.parents[e] = p
        self.fonctions = {}
        for n in ast.walk(self.arbre):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.fonctions.setdefault(n.name, n)
        self.secret_en_clair = False
        self.ordre_dans_check = False
        self.check_introuvable = False

    # -- utilitaires -------------------------------------------------------
    def dans_boucle(self, n):
        p = self.parents.get(n)
        while p is not None and not isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if isinstance(p, (ast.While, ast.For)):
                return True
            p = self.parents.get(p)
        return False

    def fonction_de(self, n):
        p = self.parents.get(n)
        while p is not None and not isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef)):
            p = self.parents.get(p)
        return p.name if p is not None else "(niveau module)"

    def affectations(self):
        """(nom, noeud valeur, ligne) pour affectations, clés de dict, mots-clés, argparse."""
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if nom_cible(t):
                        yield nom_cible(t), n.value, n.lineno
            elif isinstance(n, ast.AnnAssign) and n.value is not None and nom_cible(n.target):
                yield nom_cible(n.target), n.value, n.lineno
            elif isinstance(n, ast.Dict):
                for k, v in zip(n.keys, n.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        yield k.value, v, n.lineno
            elif isinstance(n, ast.Call):
                for kw in n.keywords:
                    if kw.arg:
                        yield kw.arg, kw.value, n.lineno
                if nom_appel(n) == "add_argument" and n.args:
                    a0 = n.args[0]
                    defaut = next((k.value for k in n.keywords if k.arg == "default"), None)
                    if isinstance(a0, ast.Constant) and isinstance(a0.value, str) and defaut is not None:
                        yield a0.value.lstrip("-"), defaut, n.lineno

    # -- 1. démo / réel ----------------------------------------------------
    def demo_reel(self):
        indices = []
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Attribute) and n.attr in ("ACCOUNT_TRADE_MODE_DEMO",
                                                           "ACCOUNT_TRADE_MODE_REAL",
                                                           "ACCOUNT_TRADE_MODE_CONTEST"):
                indices.append((n.lineno, f"compare le type de compte ({n.attr})"))
            elif isinstance(n, ast.Attribute) and n.attr == "trade_mode":
                indices.append((n.lineno, "lit account_info().trade_mode"))
            elif isinstance(n, ast.Call) and nom_appel(n) == "input":
                indices.append((n.lineno, "demande une saisie au clavier (input)"))
            elif isinstance(n, ast.Constant) and isinstance(n.value, str):
                s = n.value.lower()
                if re.fullmatch(r"--?(live|real|reel|réel)\b.*", s) or "confirm" in s:
                    indices.append((n.lineno, f"option ou texte « {n.value[:40]} »"))
        for nom, v, ligne in self.affectations():
            nn = norm(nom)
            if isinstance(v, ast.Constant):
                if "mode" in nn and isinstance(v.value, str) and v.value.lower() in (
                        "demo", "démo", "live", "real", "reel", "réel"):
                    indices.append((ligne, f"{nom} = « {v.value} »"))
                elif isinstance(v.value, bool) and nn in (
                        "demo", "live", "real", "reel", "dryrun", "paper", "allowlive",
                        "allowreal", "liveenabled", "realenabled"):
                    indices.append((ligne, f"{nom} = {v.value}"))
        return sorted(set(indices))

    # -- 2. arrêt d'urgence ------------------------------------------------
    def arret_urgence(self):
        noms = sorted({(n.lineno, n.value) for n in ast.walk(self.arbre)
                       if isinstance(n, ast.Constant) and isinstance(n.value, str)
                       and len(n.value) < 60 and MOTS_ARRET.search(n.value)})
        tests = []
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Call) and nom_appel(n) in ("exists", "isfile", "is_file"):
                action = "?"
                p = self.parents.get(n)
                while p is not None and not isinstance(p, (ast.If, ast.stmt)):
                    p = self.parents.get(p)
                if isinstance(p, ast.If):
                    gestes = []
                    for s in p.body:
                        for m in ast.walk(s):
                            if isinstance(m, (ast.Return, ast.Break, ast.Raise)):
                                gestes.append(type(m).__name__.lower())
                            elif isinstance(m, ast.Call) and nom_appel(m):
                                gestes.append(nom_appel(m))
                    action = ", ".join(dict.fromkeys(gestes)) or "rien"
                tests.append((n.lineno, self.fonction_de(n),
                              "dans une boucle" if self.dans_boucle(n) else "hors boucle", action))
        return noms, tests

    # -- 3. limites --------------------------------------------------------
    def limites(self):
        trouve = {i: [] for i in range(len(LIMITES))}
        for nom, v, ligne in self.affectations():
            if est_nombre(v):
                i = regle_limite(norm(nom))
                if i is not None:
                    trouve[i].append((nom, v.value, ligne))
        lignes = []
        for i, (libelle, attendu, ok) in enumerate(LIMITES):
            vals = trouve[i]
            if not vals:
                etat = "ABSENT (non trouvé par nom)"
            elif any(any(abs(x[1] - o) < 1e-9 for o in ok) for x in vals):
                etat = "conforme"
            else:
                etat = "ÉCART"
            detail = "; ".join(f"{n}={val} (l.{l})" for n, val, l in vals[:4])
            lignes.append((libelle, attendu, etat, detail))
        return lignes

    # -- 4. doublons / identifiant ------------------------------------------
    def doublons(self):
        cles = {}
        for nom, v, ligne in self.affectations():
            nn = norm(nom)
            for mot in ("magic", "comment", "decisionid", "requestid", "clientid",
                        "correlation", "tradeid", "uuid"):
                if mot in nn:
                    cles.setdefault(mot, ligne)
        appels = {}
        envois = []
        for n in ast.walk(self.arbre):
            nm = nom_appel(n)
            if nm in ("positions_get", "orders_get", "history_orders_get",
                      "history_deals_get", "order_check", "uuid4", "uuid1"):
                appels.setdefault(nm, n.lineno)
            if nm == "order_send":
                f = self.fonction_de(n)
                fn = self.fonctions.get(f)
                avant = sorted({nom_appel(m) for m in ast.walk(fn) if nom_appel(m) in (
                    "positions_get", "orders_get", "history_orders_get", "history_deals_get")
                    and m.lineno < n.lineno}) if fn else []
                envois.append((n.lineno, f, self.dans_boucle(n), avant))
        retcode = any(isinstance(n, ast.Attribute) and n.attr == "retcode"
                      for n in ast.walk(self.arbre))
        return cles, appels, envois, retcode

    # -- 5. secrets --------------------------------------------------------
    def secrets(self):
        en_clair, fuites = [], []
        for nom, v, ligne in self.affectations():
            nn = norm(nom)
            if isinstance(v, ast.Constant) and nom_secret(nn, v.value):
                en_clair.append((ligne, nom))
        sources = set()
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Attribute) and n.attr == "environ":
                sources.add("variables d'environnement (os.environ)")
            nm = nom_appel(n)
            if nm in ("getenv",):
                sources.add("variables d'environnement (getenv)")
            elif nm in ("load_dotenv", "dotenv_values"):
                sources.add("fichier .env (dotenv)")
            elif nm in ("get_password",):
                sources.add("coffre Windows (keyring)")
            elif nm == "ConfigParser":
                sources.add("fichier .ini (configparser)")
            if nm in ("print", "info", "debug", "warning", "error", "critical",
                      "exception", "log", "write"):
                for a in list(n.args) + [k.value for k in n.keywords]:
                    for m in ast.walk(a):
                        mn = nom_cible(m) if isinstance(m, (ast.Name, ast.Attribute)) else None
                        if mn and any(s in norm(mn) for s in ("password", "passwd", "pwd",
                                                               "mdp", "token", "secret")):
                            fuites.append((n.lineno, f"affiche « {mn} »"))
                        if isinstance(m, ast.Call) and nom_appel(m) == "account_info" \
                                and not isinstance(self.parents.get(m), ast.Attribute):
                            fuites.append((n.lineno, "affiche account_info() entier "
                                                     "(login, nom, serveur)"))
        self.secret_en_clair = bool(en_clair)
        return sorted(set(en_clair)), sorted(sources), sorted(set(fuites))

    # -- 6. ordre atteignable depuis `check` ? ------------------------------
    def chemin_check(self):
        dispatch = set()
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Compare):
                consts = [c for c in [n.left] + n.comparators
                          if isinstance(c, ast.Constant) and c.value == COMMANDE]
                if consts:
                    for c in [n.left] + n.comparators:
                        if not isinstance(c, ast.Constant):
                            dispatch.add(ast.unparse(c))
                for c in n.comparators:
                    if isinstance(c, (ast.Tuple, ast.List, ast.Set)) and any(
                            isinstance(e, ast.Constant) and e.value == COMMANDE for e in c.elts):
                        dispatch.add(ast.unparse(n.left))
        # argparse : sub.add_parser("check") puis p.set_defaults(func=X)
        alias = {}
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) \
                    and nom_appel(n.value) == "add_parser" and n.value.args \
                    and isinstance(n.value.args[0], ast.Constant) \
                    and n.value.args[0].value == COMMANDE:
                var = ast.unparse(n.targets[0])
                for m in ast.walk(self.arbre):
                    if isinstance(m, ast.Call) and nom_appel(m) == "set_defaults" \
                            and isinstance(m.func, ast.Attribute) \
                            and ast.unparse(m.func.value) == var:
                        for k in m.keywords:
                            if nom_cible(k.value):
                                alias[k.arg] = nom_cible(k.value)
        # table de commandes : {"check": fonction, ...}
        tables = {}
        for n in ast.walk(self.arbre):
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict):
                for k, v in zip(n.value.keys, n.value.values):
                    if isinstance(k, ast.Constant) and k.value == COMMANDE and nom_cible(v):
                        tables[ast.unparse(n.targets[0])] = nom_cible(v)
        trouve_entree = bool(dispatch or alias or tables)
        dangers, vus = [], set()

        def branche_commande(test):
            """None si le test ne porte pas sur la commande ; sinon True/False."""
            if isinstance(test, ast.Compare) and len(test.ops) == 1 \
                    and ast.unparse(test.left) in dispatch:
                op, droite = test.ops[0], test.comparators[0]
                if isinstance(droite, ast.Constant):
                    egal = droite.value == COMMANDE
                elif isinstance(droite, (ast.Tuple, ast.List, ast.Set)):
                    egal = any(isinstance(e, ast.Constant) and e.value == COMMANDE
                               for e in droite.elts)
                else:
                    return None
                if isinstance(op, (ast.Eq, ast.In)):
                    return egal
                if isinstance(op, (ast.NotEq, ast.NotIn)):
                    return not egal
            return None

        def resoudre(c):
            if isinstance(c.func, ast.Attribute) and c.func.attr in alias:
                return alias[c.func.attr]
            f = c.func
            if isinstance(f, ast.Subscript) and ast.unparse(f.value) in tables:
                return tables[ast.unparse(f.value)]
            if isinstance(f, ast.Call) and nom_appel(f) == "get" \
                    and isinstance(f.func, ast.Attribute) \
                    and ast.unparse(f.func.value) in tables:
                return tables[ast.unparse(f.func.value)]
            return nom_appel(c)

        def expr(noeud, pile):
            for m in ast.walk(noeud):
                if isinstance(m, ast.Call):
                    nm = resoudre(m)
                    if nm in APPELS_ORDRE:
                        dangers.append((m.lineno, " → ".join(pile + [nm])))
                    elif nm in self.fonctions and nm not in vus:
                        vus.add(nm)
                        bloc(self.fonctions[nm].body, pile + [nm])

        def bloc(stmts, pile):
            for s in stmts:
                if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                if isinstance(s, ast.If):
                    b = branche_commande(s.test)
                    if b is None:
                        expr(s.test, pile)
                        bloc(s.body, pile)
                        bloc(s.orelse, pile)
                    else:
                        bloc(s.body if b else s.orelse, pile)
                    continue
                corps = [getattr(s, a) for a in ("body", "orelse", "finalbody")
                         if isinstance(getattr(s, a, None), list)]
                if corps:
                    for champ, val in ast.iter_fields(s):
                        if isinstance(val, ast.AST) and not isinstance(val, ast.stmt):
                            expr(val, pile)
                    for h in getattr(s, "handlers", []):
                        bloc(h.body, pile)
                    for c in corps:
                        bloc(c, pile)
                    if isinstance(s, (ast.With, ast.AsyncWith)):
                        for it in s.items:
                            expr(it.context_expr, pile)
                else:
                    expr(s, pile)

        bloc(self.arbre.body, ["démarrage"])
        dynamiques = sorted({n.lineno for n in ast.walk(self.arbre)
                             if nom_appel(n) in ("getattr", "eval", "exec", "__import__")})
        self.ordre_dans_check = bool(dangers)
        self.check_introuvable = not trouve_entree
        return trouve_entree, sorted(set(dangers)), dynamiques


def rapport(chemin):
    try:
        source = Path(chemin).read_text(encoding="utf-8")
        audit = Audit(source)
    except (OSError, UnicodeDecodeError, SyntaxError) as e:
        print(f"Impossible de lire {chemin} : {type(e).__name__}: {e}")
        return 2

    out = print
    out(f"# Audit statique — {Path(chemin).name} ({len(source.splitlines())} lignes)")
    out("Le script n'a pas été exécuté. Indices automatiques : à confirmer en lecture.\n")

    out("## 0. La commande `check` peut-elle envoyer un ordre ?")
    entree, dangers, dyn = audit.chemin_check()
    if not entree:
        out("- INDÉTERMINÉ : aiguillage de la commande « check » non trouvé.")
    if dangers:
        out("- OUI, appel d'ordre atteignable — NE PAS lancer `check` sans garde-fou :")
        for l, c in dangers:
            out(f"  - ligne {l} : {c}")
    elif entree:
        out("- NON d'après l'analyse (aucun order_send / Buy / Sell / Close sur le chemin).")
    if dyn:
        out(f"- Appels dynamiques non suivis (getattr/eval/exec), lignes : {dyn}")

    out("\n## 1. Mode démo / réel")
    ind = audit.demo_reel()
    for l, t in ind:
        out(f"- l.{l} : {t}")
    if not ind:
        out("- Aucun indice : ni contrôle du type de compte, ni confirmation du mode réel.")

    out("\n## 2. Arrêt d'urgence par fichier")
    noms, tests = audit.arret_urgence()
    for l, v in noms:
        out(f"- texte l.{l} : « {v} »")
    for l, f, ou, action in tests:
        out(f"- test d'existence l.{l} dans {f} ({ou}) → action : {action}")
    if not tests:
        out("- Aucun test d'existence de fichier trouvé.")

    out("\n## 3. Limites du robot de référence")
    out("| Limite | Attendu | État | Trouvé |")
    out("|---|---|---|---|")
    for lib, att, etat, det in audit.limites():
        out(f"| {lib} | {att} | {etat} | {det or '—'} |")

    out("\n## 4. Doublons d'ordre et identifiant")
    cles, appels, envois, retcode = audit.doublons()
    out(f"- Clés trouvées : {', '.join(f'{k} (l.{l})' for k, l in cles.items()) or 'aucune'}")
    out(f"- Lectures d'état : {', '.join(f'{k} (l.{l})' for k, l in appels.items()) or 'aucune'}")
    out(f"- Contrôle du retcode : {'oui' if retcode else 'NON'}")
    for l, f, boucle, avant in envois:
        out(f"- order_send l.{l} dans {f} : " + ("DANS UNE BOUCLE (relance = doublon possible) ; "
            if boucle else "") + (f"vérifie avant : {', '.join(avant)}" if avant
                                  else "aucune vérification des positions/ordres avant l'envoi"))

    out("\n## 5. Secrets")
    clair, sources, fuites = audit.secrets()
    for l, nom in clair:
        out(f"- SECRET EN CLAIR l.{l} : {nom} = (valeur masquée)")
    out(f"- Lecture externe : {', '.join(sources) or 'aucune trouvée'}")
    for l, t in fuites:
        out(f"- FUITE POSSIBLE DANS LES JOURNAUX l.{l} : {t}")

    out("\n## Verdict")
    if audit.ordre_dans_check:
        out("- BLOQUANT : `check` peut envoyer un ordre. Ne pas lancer `check`. (code 3)")
        return 3
    if audit.check_introuvable:
        out("- BLOQUANT : commande `check` introuvable. Ne pas la lancer avant lecture. (code 4)")
        return 4
    if audit.secret_en_clair:
        out("- À CORRIGER : secret écrit en clair. `check` peut tourner. (code 1)")
        return 1
    out("- Aucun point bloquant détecté automatiquement (ne remplace pas la lecture du code). "
        "(code 0)")
    return 0


if __name__ == "__main__":
    # Console Windows ou sortie redirigée : ne jamais planter sur un accent.
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(rapport(sys.argv[1]))
