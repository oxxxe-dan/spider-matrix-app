# Spider Matrix V12 (Labo V2) — Audit de l'écosystème et plan d'améliorations

_Préparé le 14/10/2026. Base de travail pour lancer les prochaines améliorations._

Voir aussi : [`MISES_A_JOUR_DECIDEES_V2.md`](MISES_A_JOUR_DECIDEES_V2.md) — registre des mises à jour déjà décidées et leur état réel.

> **Note de confidentialité** : ce dépôt GitHub est **public**. Ce document ne contient ni secret, ni adresse d'application, ni détail exploitable. Recommandation n°1 du Lot 0 : passer le dépôt en privé avant d'y versionner le code des applications (principe « Protection du projet » du dossier de travail V12).

---

## 0. Sources analysées

| Source | Contenu exploité |
|---|---|
| Dépôt GitHub `spider-matrix-app` | README, branches `main` / `v2-initial-architecture` (identiques au commit initial), PR #1 fermée (pont ChatGPT–Claude–StrategyTune) |
| AppDeploy (6 applications Spider) | Code source complet des versions en ligne, état des déploiements, tâches planifiées, captures QA |
| Gmail | Dossier de travail V12 (14/09), échanges ACPR, OANDA, Saxo, cTrader/Spotware, AppDeploy, Stripe |
| Google Drive | Visuel « Spider Matrix V10 — Vision globale / Toile éternelle » (concept 8 devises, 28 paires, 4 carrés, Risk Engine, cycle Spider) |

« V12 V2 » correspond au **Labo Spider Matrix V12**, dont l'en-tête indique « V2 · Labo de recherche · or en priorité · multi-marchés ».

---

## 1. Cartographie de l'écosystème

| Application | Rôle actuel | Données | État |
|---|---|---|---|
| **Spider Matrix V12 — Labo (V2)** | Cœur de recherche : moteur de backtest M5, 8 agents, Battle, StrategyTune, rapport A–F, arène multi-timeframes, multi-marchés (46 marchés), Chasse hebdomadaire, Auto-évolution (or + EUR/USD), OANDA Practice en lecture seule, offres Gratuit/Pro | Yahoo Finance M5 (~59 j, différé), OANDA Practice (or, EUR/USD), CSV MT5, synthétique | 21 versions (9→13/10), 2 tâches planifiées toutes les 5 min, aucune erreur |
| **Spider Matrix — Labo éducatif** | Vitrine « Jarvis Alpha », Gold World, éducation des agents, Battle Royale, conformité, profil 100 € | Mélange : Yahoo réel sur certains modules, **valeurs simulées (sinus/graines fixes)** sur d'autres | 4 tâches planifiées (Sentinel, Jarvis, calendrier), aucune erreur |
| **Spider Matrix Bot** | Bot de démonstration (compte virtuel 100 $, DCA, analyse caméra d'un graphique) | **Prix générés aléatoirement** | En ligne |
| **Spider Jarvis V1** | Copilote vocal (commande → plan d'action sûr) | IA | En ligne |
| **Spider Matrix Agentic Harness** | Bac à sable de « runs » d'agents | Progression simulée | En ligne |
| **Jégouzo Vision** | Gestion d'entreprise (tâches, clients, factures) + module Spider + abonnement Stripe + webhook TradingView | Bougies envoyées par l'utilisateur / TradingView | En ligne |

Constat global : **6 applications, 3 « Jarvis », 2 « Battle Royale », 4 copies du même graphique « exemple fictif »**, deux définitions différentes des agents (paramètres V2 ≠ paramètres V12). Le seul moteur dont les chiffres sont mesurés est le **Labo V12**.

---

## 2. Points forts à préserver (ne pas casser)

- Moteur de backtest V12 **sans biais d'anticipation** : décision à la clôture, barres H1/M15 clôturées uniquement, entrée à l'ouverture suivante, coûts bid/ask + glissement, stop prioritaire, gestion des gaps.
- Découpage recherche 60 % / validation 20 % / **test final masqué** 20 %, à révéler une seule fois.
- Statistiques honnêtes de la Chasse : p-values, correction Benjamini–Hochberg, intervalle de Wilson, test de permutation, corrélation de rang apprentissage→test, suivi prospectif d'une chasse à l'autre.
- Auto-évolution prudente : mode Surveillance, période d'essai de 20 trades, retour arrière automatique, pauses de sécurité.
- Principe « rien n'est inventé » : erreurs de données affichées, aucun résultat sans données, synthétique clairement marqué.
- Garde-fous : aucun ordre réel, LIVE verrouillé, avertissements de risque, journal et versions jamais supprimés.

---

## 3. Constats

Gravité : 🔴 critique · 🟠 important · 🟡 à améliorer

### A. Vérité des données et communication
1. 🔴 **Labo éducatif : signaux et performances simulés présentés comme réels.** La matrice de force des 8 devises, les signaux ACHAT/VENTE, les courbes « évolution relative » et les P&L / taux de réussite de la Battle Royale sont calculés à partir de graines fixes et de fonctions sinus, sous des badges « LIVE ENGINE » et « LIVE-READY ». Cela contredit le principe V12 et constitue un risque de communication trompeuse (AMF), surtout si la page est montrée à des partenaires.
2. 🔴 **Bot : prix aléatoires + DCA à multiplicateur 1,5 sur 5 niveaux** (moyenne à la baisse). Contraire aux règles d'or « aucune perte incontrôlée » et au Risk Engine V12.
3. 🟠 **Crypto incohérente** : V12 exclut toute cryptomonnaie, mais BTC apparaît dans le labo éducatif (visuel, agent « Neuronal Sentinel ») et dans le bot. La crypto relève d'un autre cadre (MiCA).
4. 🟠 **Objectif « 0,20 % à 0,50 % par jour »** sur le visuel V10 : à ne plus utiliser dans aucune communication, même avec la mention « pas une promesse ».
5. 🟡 Messages contradictoires : « Compte gratuit · Aucun paiement » (labo éducatif) contre offres Gratuit/Pro et Stripe (Labo V12, Jégouzo Vision). Libellé « Or (XAU/USD) » appliqué au contrat à terme GC=F.

### B. Moteur et statistiques (Labo V12)
6. 🔴 **Historique trop court** : ~59 jours de M5 Yahoo → période test ≈ 12 jours, très peu de trades par agent. L'empilement H1 (EMA 200 en D1) ne peut jamais s'échauffer ; M15/M30 (EMA 200 en H4 ≈ 33 jours de bourse) consomment l'essentiel de la fenêtre.
7. 🔴 **Découpage calculé sur les barres brutes, échauffement inclus** : avec des EMA lentes, la période « recherche » est partiellement ou totalement vide de trades. Le découpage doit démarrer à la première barre exploitable.
8. 🟠 **Raccords de contrat GC=F** : la série continue Yahoo change de contrat chaque mois actif ; le saut de prix crée de faux signaux et des ATR gonflés. Écart supplémentaire avec le spot XAU/USD des brokers.
9. 🟠 **Taille de position hors coûts** : le lot est calculé sur la distance du stop sans spread ni glissement → le risque réel par trade dépasse le risque affiché.
10. 🟠 **Pas de walk-forward** (annoncé « V2 » dans le rapport A–F, non construit).
11. 🟠 **p-values supposant des trades indépendants** alors que les marchés et les trades d'un même jour sont corrélés (limite déjà signalée dans le rapport) → bootstrap par blocs (jour/semaine).
12. 🟠 **Jarvis Alpha (règle de fusion) jamais backtesté** : le verdict ACHAT/VENTE/NO-TRADE n'a aucune performance mesurée.
13. 🟡 Métriques manquantes : Sharpe/Sortino, exposition, durée moyenne, MAE/MFE, coût moyen en R. Profit factor « infini » stocké comme `null`. Sorties marquées « BE » après déplacement par le stop suiveur.

### C. Auto-évolution
14. 🔴 **Dérive possible de l'espérance** : un challenger est retenu s'il augmente le taux de réussite avec une espérance ≥ 90 % de celle du champion **courant**. Sur plusieurs générations, l'espérance peut baisser de 10 % à chaque étape (0,9ᵏ) tout en améliorant le taux de réussite.
15. 🔴 **Réutilisation des « derniers 20 % »** comme porte de confirmation à chaque cycle (toutes les 20 min) : la période test devient une période d'optimisation ; la correction BH n'est faite qu'à l'intérieur d'un cycle, pas sur l'ensemble des milliers de challengers testés dans le temps.
16. 🟡 Chasse et Auto-évolution interrogent Yahoo toutes les 5 min chacune, sans cache partagé persistant → risque de limitation.

### D. Données et infrastructure
17. 🟠 **Aucune archive de barres** : chaque calcul re-télécharge 59 jours ; l'historique ne s'accumule jamais. Une archive en base permettrait d'avoir 6–12 mois de M5 réels d'ici quelques mois, et de vrais tests en avant.
18. 🟠 **Source unique** (Yahoo, différé, sans volume FX) pour 44 des 46 marchés. Sources disponibles : OANDA Practice (or, EUR/USD), Twelve Data (connecteur actif, plan gratuit 800 crédits/jour), import CSV MT5, historiques Dukascopy.
19. 🟡 Code uniquement sur AppDeploy : pas d'historique git, pas de revue de code, pas d'intégration continue.

### E. Sécurité et accès
20. 🟠 **Labo éducatif : plusieurs routes API n'exigent qu'une connexion**, pas le rôle propriétaire (dont une qui lance jusqu'à 7 téléchargements Yahoo par appel, avec un symbole choisi par l'appelant). La barrière « propriétaire » de l'interface est seulement visuelle pour ces routes.
21. 🟠 **Identifiants broker stockés en clair dans les secrets** (login/mot de passe IBKR et MT5) alors qu'aucune connexion n'est active ; jeton Saxo SIM encore prévu alors que Saxo a refusé l'accès.
22. 🟠 **Jégouzo Vision** : abonnement Stripe sans webhook (aucune activation/résiliation automatique) ; enregistrement « entreprise » qui accepte n'importe quel champ.
23. 🟡 Adresse du propriétaire écrite en dur dans les 6 applications (front et back). 6 fournisseurs d'IA prévus dans le labo éducatif → surface et coûts à réduire.

### F. Qualité et tests
24. 🔴 **Les tests E2E ne testent rien** : les 16 scénarios du Labo V12 supposent un visiteur anonyme, mais l'application est réservée au propriétaire ; les captures QA montrent uniquement l'écran « Se connecter » : les scénarios n'atteignent jamais l'application. Même situation pour le labo éducatif.
25. 🟠 Labo éducatif : ~480 000 caractères de code sur 42 fichiers, nombreux composants écrits sur une seule ligne ; backend de 105 Ko en un seul fichier. Maintenance difficile et risque de régressions.
26. 🟠 **Deux registres d'agents divergents** (ex. Spider Vision : EMA 13/89 et risque 0,5 % dans V12 ; EMA 21/50 et risque 1 % dans le labo éducatif).

### G. Produit, partenaires et conformité
27. 🔴 **ACPR (Pôle Fintech Innovation) attend un document de présentation** (fonctionnement, type de clients) depuis le 18/09. Aucune réponse trouvée dans Gmail (l'envoi initial venait d'une adresse Outlook : à vérifier).
28. 🟠 **Saxo a refusé** l'accès OpenAPI (16/09 : réservé aux clients Saxo et entités agréées). Le message à l'ACPR mentionne pourtant des « adapters Saxo SIM » → à corriger dans le dossier.
29. 🟠 **OANDA** : le support global renvoie vers le support OTMS (UE) et indique que **l'API n'est pas disponible pour les clients OTMS**. Le Labo V12 utilise un jeton Practice : confirmer par écrit que cet usage est autorisé.
30. 🟡 **cTrader / Spotware** : invitation à déposer une application Open API → piste démo ouverte. **IBKR** : connecteur déjà relié au compte, API paper trading accessible aux particuliers UE → piste à étudier.
31. 🟡 AMF, MetaTrader/Python, TradingView, France FinTech, Bpifrance… : démarches du dossier sans trace d'envoi.
32. 🟡 Offres Pro + liste d'attente + Stripe dans un labo réservé au propriétaire : personne ne peut s'abonner. Toute commercialisation d'analyses/signaux au public doit attendre la qualification réglementaire (risque de conseil en investissement).
33. 🟡 Pont ChatGPT–Claude (PR #1) fermé sans fusion : décider de le reprendre (dans un dépôt privé) ou de l'abandonner.

---

## 4. Plan d'améliorations par lots

Effort : **S** < ½ journée · **M** ≈ 1 journée · **L** plusieurs jours. Chaque lot = un seul déploiement par application concernée.

### Lot 0 — Hygiène, sécurité, versionnement (prioritaire)
| # | Amélioration | App | Critère d'acceptation | Effort |
|---|---|---|---|---|
| 0.1 | Passer le dépôt GitHub en privé, puis y importer le code des 6 apps (un dossier par app) | Toutes | Code versionné, historique git, aucun secret dans le dépôt | M |
| 0.2 | Exiger le rôle propriétaire (ou un quota) sur toutes les routes sensibles du labo éducatif | Labo éducatif | Un compte non propriétaire reçoit 403 sur chaque route de calcul/IA | S |
| 0.3 | Supprimer les identifiants broker en clair et le jeton Saxo ; ne garder que des jetons API révocables | Labo éducatif | Plus aucun mot de passe broker dans les secrets | S |
| 0.4 | Centraliser l'identité du propriétaire (un seul réglage par app) | Toutes | Aucune adresse écrite en dur dans le code | S |
| 0.5 | Webhook Stripe signé (activation/résiliation) + liste blanche des champs « entreprise » | Jégouzo Vision | Abonnement activé et révoqué automatiquement ; champs inconnus rejetés | M |
| 0.6 | Export de sauvegarde (journal, versions, auto-évolution, chasses) | Labo V12 | Export JSON téléchargeable depuis l'onglet Journal | S |

### Lot 1 — Vérité des données (zéro chiffre inventé)
| # | Amélioration | App | Critère d'acceptation | Effort |
|---|---|---|---|---|
| 1.1 | Remplacer la matrice 8 devises simulée par une **force relative calculée sur les 28 paires réelles** (mêmes données que le Labo V12) | Labo éducatif | Chaque valeur affichée provient d'une barre datée ; sinon « Données indisponibles » | M |
| 1.2 | Battle Royale du labo éducatif : afficher les **résultats du moteur V12** ou un bandeau « DÉMO VISUELLE — chiffres fictifs » non masquable | Labo éducatif | Plus aucun P&L / taux de réussite issu d'un sinus sans bandeau | M |
| 1.3 | Retirer « LIVE ENGINE » / « LIVE-READY » ; libellés « Recherche · Démo · Aucun ordre » | Labo éducatif | Aucun badge « LIVE » tant que LIVE est verrouillé | S |
| 1.4 | Retirer la crypto (BTC) de tous les visuels et agents | Labo éducatif, Bot | Aucune référence crypto | S |
| 1.5 | Bot : supprimer le DCA multiplicateur (ou le passer en « interdit par le Risk Engine ») ; prix réels différés ou bandeau « prix simulés » | Bot | Aucun ajout de position à perte ; source de prix affichée | M |
| 1.6 | Renommer « Or (XAU/USD) » en « Or — contrat à terme COMEX (GC=F) » quand la source est Yahoo | Labo V12 | Libellé exact selon la source | S |

### Lot 2 — Fiabilité du moteur V12
| # | Amélioration | Critère d'acceptation | Effort |
|---|---|---|---|
| 2.1 | **Découpage après échauffement** : 60/20/20 calculé à partir de la première barre où tous les indicateurs de l'agent sont prêts | La période recherche contient des trades pour tous les empilements ayant assez de données | M |
| 2.2 | **Taille de position incluant spread + glissement** dans la distance de risque | Perte au stop = risque affiché (±1 %) | S |
| 2.3 | **Raccords GC=F** : détection des sauts de contrat (écart d'ouverture anormal à date de roll) et neutralisation, ou source spot | Aucun signal déclenché par un saut de roll sur l'historique test | M |
| 2.4 | **Walk-forward** glissant (ex. 4 fenêtres apprentissage→test) dans le rapport A–F | Tableau par fenêtre + part des fenêtres à espérance > 0 | L |
| 2.5 | **Bootstrap par blocs** (jour) pour les p-values et le Monte Carlo | p-values « bloc » affichées à côté des p-values classiques | M |
| 2.6 | **Jarvis Alpha comme 9ᵉ agent backtesté** (même moteur, mêmes coûts) | Jarvis apparaît dans Battle, Chasse et rapport avec ses métriques | L |
| 2.7 | Métriques ajoutées : Sharpe/Sortino journaliers, exposition, durée moyenne, MAE/MFE, coût moyen en R ; PF plafonné ; libellé de sortie « SUIVEUR » | Visibles dans le rapport et le journal | M |
| 2.8 | **Tests unitaires du moteur** : absence d'anticipation, comptabilité des coûts, découpage, gaps, taille de position | Suite exécutée avant chaque déploiement | M |

### Lot 3 — Données
| # | Amélioration | Critère d'acceptation | Effort |
|---|---|---|---|
| 3.1 | **Archive de barres** : tâche planifiée qui ajoute les barres M5 clôturées de chaque marché en base (par semaine) | L'historique disponible dépasse 59 jours et croît chaque jour | L |
| 3.2 | Cache de barres partagé entre Chasse, Auto-évolution et interface | Un seul téléchargement par marché et par fenêtre de 10 min | M |
| 3.3 | Barres H1 sur 2 ans (source horaire) pour l'empilement H1 | L'empilement H1 produit des résultats au lieu de « échauffement » | M |
| 3.4 | Deuxième source de contrôle (OANDA Practice / Twelve Data) + comparateur étendu (écart moyen, barres manquantes) | Tableau de concordance par marché | M |
| 3.5 | Import CSV élargi (Dukascopy, MT5 M1) avec contrôle de qualité | Rapport d'import : trous, doublons, spread médian | M |

### Lot 4 — Auto-évolution v2
| # | Amélioration | Critère d'acceptation | Effort |
|---|---|---|---|
| 4.1 | Contrainte d'espérance **ancrée sur la base** de l'agent (jamais sur le champion courant) | Impossible d'adopter une version dont l'espérance est < base | S |
| 4.2 | Objectif principal = **borne basse de l'espérance** (taux de réussite en critère secondaire) | Classement des challengers par borne basse | S |
| 4.3 | Confirmation **uniquement en avant** (barres arrivées après l'adoption) ; les « derniers 20 % » ne servent plus de porte | Journal : aucune adoption définitive sans période d'essai réussie | M |
| 4.4 | **Budget global de tests** : compteur cumulé de challengers et seuil de significativité ajusté dans le temps | Le seuil se durcit avec le nombre total d'essais | M |
| 4.5 | Rapport hebdomadaire : générations, adoptions, retours arrière, champion vs base en avant | Rapport consultable dans l'onglet | M |

### Lot 5 — Tests et vitrine
| # | Amélioration | Critère d'acceptation | Effort |
|---|---|---|---|
| 5.1 | **Mode démo public** du Labo V12 : sans connexion, données synthétiques seulement, aucune route marché | Les 16 scénarios E2E s'exécutent et passent ; captures QA montrant le labo | M |
| 5.2 | Mise à jour des scénarios E2E (propriétaire vs visiteur) | Chaque onglet couvert au moins une fois | M |
| 5.3 | Découpage du labo éducatif en modules lisibles (un composant par fichier, formaté) | Aucun fichier sur une seule ligne > 300 caractères | L |

### Lot 6 — Écosystème et produit
| # | Amélioration | Critère d'acceptation | Effort |
|---|---|---|---|
| 6.1 | **Architecture cible** : Labo V12 = moteur et vérité ; labo éducatif = vitrine/éducation qui **lit les résultats du V12** ; Jarvis = un seul assistant | Plus de calcul de performance hors du V12 | L |
| 6.2 | **Registre d'agents unique** (paramètres V12) réutilisé partout | Paramètres identiques dans toutes les apps | M |
| 6.3 | Archiver ou fusionner Bot, Agentic Harness et le graphique « exemple fictif » dupliqué | ≤ 3 apps Spider actives | M |
| 6.4 | Message commercial unique ; offres Pro gelées tant que le cadre réglementaire n'est pas qualifié | Mêmes mentions légales sur toutes les apps | S |
| 6.5 | Décider du pont ChatGPT–Claude : reprise dans le dépôt privé (lecture seule, propositions en attente de revue) ou abandon | Décision notée dans ce document | S |

### Lot 7 — Partenaires et conformité
| # | Action | Livrable | Effort |
|---|---|---|---|
| 7.1 | **Dossier de présentation ACPR** (fonctionnement, public visé, périmètre recherche/démo, LIVE verrouillé, Risk Engine, audit trail, statut des brokers corrigé) | PDF prêt à envoyer au Pôle Fintech Innovation | M |
| 7.2 | Même dossier adapté à l'**AMF** (Division FinTech, Innovation et Compétitivité) | Courriel + PDF | S |
| 7.3 | Mettre à jour les statuts brokers dans les apps : Saxo refusé, OANDA à confirmer (OTMS), cTrader à candidater, IBKR paper à étudier | Page « Statut partenaires » factuelle | S |
| 7.4 | Question écrite au support OANDA OTMS sur l'usage du jeton Practice en lecture seule | Réponse écrite archivée | S |
| 7.5 | Candidature cTrader Open API (application démo, lecture seule d'abord) | Dossier de candidature | S |
| 7.6 | Page « Statut réglementaire et limites » visible dans chaque app | Page en ligne | S |

---

## 5. Ordre de lancement recommandé

1. **Lot 0 + Lot 1** — risques de sécurité et de communication, rapides à corriger.
2. **Lot 7.1** en parallèle — l'ACPR attend un document depuis le 18/09.
3. **Lot 2 + Lot 3** — sans données plus longues et sans découpage corrigé, les conclusions des agents restent fragiles.
4. **Lot 4** — l'auto-évolution ne doit continuer en mode Auto qu'après 4.1 et 4.3 (en attendant : mode Surveillance conseillé).
5. **Lot 5**, puis **Lot 6**.

## 6. Décisions à prendre par le porteur du projet

1. Passer le dépôt GitHub en privé et y versionner le code des apps ?
2. Labo éducatif : brancher sur les données réelles du V12 (recommandé) ou assumer une « démo visuelle » clairement marquée ?
3. Applications à archiver : Bot, Agentic Harness, autre ?
4. Auto-évolution : passer en mode Surveillance en attendant le Lot 4 ?
5. Feu vert pour les déploiements, lot par lot.
