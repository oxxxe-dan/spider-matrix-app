# Outils de contrôle du robot MT5 (chantier 2)

Outils à lancer sur le PC Windows, dans le dossier du robot. Aucun n'envoie d'ordre.
Le robot `spider_v12_mt5.py` reste sur le PC : il n'est pas dans ce dépôt public (voir `.gitignore`).

## En une commande (recommandé)

Copier le dossier `outils/mt5` sur le PC, puis, terminal MT5 démo ouvert :

```
python chemin\vers\outils\mt5\controle_complet.py spider_v12_mt5.py
```

1. Audit statique (le robot n'est pas exécuté).
2. `check` avec garde-fou, **seulement** si l'audit ne trouve pas d'envoi d'ordre atteignable depuis
   `check` (code 3) et a bien trouvé la commande `check` (sinon code 4 : lecture humaine d'abord).
3. Rapport affiché et enregistré dans `rapport_controle.txt`, à coller dans la conversation.
   Numéro de compte, serveur, nom du titulaire et mots de passe y sont remplacés par `***`.

`check` est arrêté s'il ne rend pas la main au bout de 5 minutes (code 5).

## 1. Audit statique (ne lance rien)

```
python audit_statique.py spider_v12_mt5.py
```

Il lit le script comme du texte, sans l'importer ni l'exécuter, et indique :

0. si la commande `check` peut atteindre `order_send`, `Buy`, `Sell` ou `Close`, avec le chemin d'appel ;
1. les indices du mode démo / réel (type de compte vérifié, confirmation du réel) ;
2. l'arrêt d'urgence par fichier : où il est testé (au démarrage, dans la boucle) et ce qui se passe ;
3. les limites du robot de référence, comparées aux valeurs attendues ;
4. la protection contre les doublons (magic, commentaire, lecture des positions avant envoi, envoi dans une boucle) ;
5. les secrets : valeurs écrites en clair (jamais affichées, seulement le nom et la ligne), lecture externe, affichage dans les journaux.

Ce sont des indices trouvés par nom de variable. Ils ne remplacent pas la lecture du code.
Code de sortie : 3 `check` peut envoyer un ordre · 4 `check` introuvable · 1 secret en clair ·
0 rien de bloquant · 2 fichier illisible.

## 2. `check` avec garde-fou

```
python check_sans_ordre.py spider_v12_mt5.py
```

Il remplace `order_send`, `Buy`, `Sell` et `Close` du module MetaTrader5 par une fonction qui n'envoie
rien (elle note la tentative et renvoie `None`, comme un envoi refusé), puis lance `spider_v12_mt5.py check`.
La connexion, le compte, les prix et `order_check` restent réels, en lecture seule.

À la fin : nombre de tentatives bloquées. Code 3 si le robot a essayé d'envoyer un ordre.
Tout ce que le robot affiche passe par un masque (compte, serveur, titulaire, variables
d'environnement contenant PASS, LOGIN, SERVER, TOKEN, SECRET, KEY…).

Limite : le garde-fou couvre le module MetaTrader5 chargé par le robot. Un ordre passé par un autre
moyen (autre processus, autre bibliothèque) ne serait pas intercepté ; l'audit statique sert à le repérer.

## Tests

Sous Linux ou Windows, sans terminal MT5 (faux module MetaTrader5) :

```
python -m unittest outils/mt5/tests/test_outils.py -v
```

Les robots de `tests/exemples/` sont fictifs et servent seulement aux tests.
