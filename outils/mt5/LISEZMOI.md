# Outils de contrôle du robot MT5 (chantier 2)

Deux outils à lancer sur le PC Windows, dans le dossier du robot. Aucun des deux n'envoie d'ordre.
Le robot `spider_v12_mt5.py` reste sur le PC : il n'est pas dans ce dépôt public (voir `.gitignore`).

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
Code de sortie : 0 rien de bloquant, 1 point bloquant, 2 fichier illisible.

## 2. `check` avec garde-fou

```
python check_sans_ordre.py spider_v12_mt5.py
```

Il remplace `order_send`, `Buy`, `Sell` et `Close` du module MetaTrader5 par une fonction qui n'envoie
rien (elle note la tentative et renvoie `None`, comme un envoi refusé), puis lance `spider_v12_mt5.py check`.
La connexion, le compte, les prix et `order_check` restent réels, en lecture seule.

À la fin : nombre de tentatives bloquées. Code 3 si le robot a essayé d'envoyer un ordre.

Limite : le garde-fou couvre le module MetaTrader5 chargé par le robot. Un ordre passé par un autre
moyen (autre processus, autre bibliothèque) ne serait pas intercepté ; l'audit statique sert à le repérer.

## Tests

Sous Linux ou Windows, sans terminal MT5 (faux module MetaTrader5) :

```
python -m unittest outils/mt5/tests/test_outils.py -v
```

Les robots de `tests/exemples/` sont fictifs et servent seulement aux tests.
