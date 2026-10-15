# Spider Matrix V2 — Registre des mises à jour décidées et état réel

_Établi le 14/10/2026. Complète `PLAN_AMELIORATIONS_V12_V2.md`._

Légende : ✅ fait · 🟡 partiel · ❌ à faire · ⛔ bloqué / abandonné · ❓ décision contradictoire à trancher

> **Méthode** : les anciennes conversations ne sont pas lisibles depuis cette session. Les décisions ont été reconstituées à partir des traces qu'elles ont laissées, puis **vérifiées dans le code en ligne** (pas seulement dans les textes affichés).

## Sources des décisions

| Réf. | Source | Date |
|---|---|---|
| **S1** | Feuille de route du Labo V12 (onglet Cockpit : V1 / **V2** / V3, « En attente de votre part », phases StrategyTune) | 9–13/10 |
| **S2** | Courriel « Spider Matrix V12 — Dossier de travail France / Demo / Battle Arena / Partenariats » | 14/09 |
| **S3** | Visuel « Spider Matrix V10 — Vision globale / Toile éternelle » (Drive) | 12/09 |
| **S4** | Couche « V12 Extension Layer » et « Unified Core » du labo éducatif | jusqu'au 13/10 |
| **S5** | « Prochaine vague d'amélioration » de Jarvis Evolution (labo éducatif) | jusqu'au 13/10 |
| **S6** | Protocole ChatGPT ↔ Claude et pont StrategyTune (PR #1, fermée sans fusion) | 11/10 |

---

## 1. Feuille de route officielle « V2 » (S1)

| Décision V2 | État | Constat dans le code |
|---|---|---|
| Lanceur multi-timeframes (M5, M15, M30, H1 en parallèle) | ✅ | Onglet Lancer. **Mais** H1 ne s'échauffe jamais sur 59 jours et M15/M30 très peu (voir plan, constat 6) |
| Arène live « 7 modes » | ✅ | **6 modes** codés ; libellé corrigé en « 6 modes » le 14/10 |
| Paramètres par tableau + retour à l'origine + export/import JSON | ✅ | Onglet Lancer, réglages du tableau |
| Statut OANDA démo en lecture seule | ✅ | Prix et résumé de compte Practice, réservé au propriétaire |
| Réglages avancés : stop suiveur, pause après une perte | ✅ | Désactivés par défaut, n'altèrent pas les résultats de référence |
| **Walk-forward sur historique MT5 long** (« V2 » dans le rapport A–F et StrategyTune phase 6) | ❌ | Absent du moteur V12. Un walk-forward existe seulement dans le labo éducatif (or 15 min, moteur séparé) |
| Import d'historique MT5 (CSV) | ✅ | Avec décalage horaire serveur |
| StrategyTune phase 2 « Analyse des pertes » | 🟡 | Entonnoir + motifs de sortie ; pas d'attribution des pertes par cause |
| Profil « Arena » : reproduire le signal EMA d'Arena | ❌ | Indiqué « pas encore reproduit » |

**Ajouté en V2 au-delà de la feuille de route** (✅ en ligne) : Multi-marchés (46 marchés), Chasse hebdomadaire avec correction statistique, Auto-évolution or + EUR/USD, onglet Spider Agent (duel, table de conformité), panneau Jarvis Alpha (règle de fusion), options Bollinger et arrêt sur drawdown, offres Gratuit/Pro (paiement non ouvert).

### Prévu pour la V3 (non commencé, conforme à la décision)
| Décision V3 | État |
|---|---|
| Pont Python + MT5 sur Windows, démo d'abord, réel seulement après activation explicite, arrêt d'urgence, limites dures | ❌ |
| StrategyTune phase 7 « Validation MT5 démo » | ❌ |
| Grille Terre · 8 pattes · Cyclone · Poulpe · Vague | ❌ |
| Jarvis Alpha complet · Kraken · 7 cerveaux | ❌ (seule une règle de fusion minimale existe, non backtestée) |
| Spider Sentinel Guardian | ❌ dans le V12 (un « Sentinel » de balayage tourne dans le labo éducatif) |

### En attente de ta part (S1, toujours ouvert)
| Élément demandé | État |
|---|---|
| Robot MQL5 « EURUSD Intraday Pullback » (.mq5) pour aligner Hurst et déclencheur M5 | ❌ non fourni |
| Exports MT5 XAUUSD et EURUSD (M1/M5, plusieurs mois) | ❌ non fournis |
| Emplacement du robot : PC Windows ou VPS Windows | ❓ |
| Broker démo : OANDA MT5 ou Axi MT5 | ❓ (voir conflit C4) |
| Heure de référence des sessions : Paris ou heure serveur MT5 | ❓ |
| R:R de référence officiel : 1,5 (robot) ou 2,0 (baseline) | ❓ (voir conflit C2) |

---

## 2. Dossier de travail France / Démo / Battle Arena (S2)

| Décision | État | Constat |
|---|---|---|
| Analyse multi-marchés et multi-stratégies | ✅ | 46 marchés, 8 agents |
| Backtests historiques + hors échantillon | ✅ | Recherche 60 % / validation 20 % / test final masqué 20 % |
| Battle Arena sur scénarios identiques | ✅ | Mêmes données, coûts, capital |
| Profils de référence immuables + variantes temporaires | ✅ | Versions, surcharges par tableau, champion vs base |
| Apprentissage entre agents sans réécrire l'historique | 🟡 | Évolution par agent, historique conservé ; aucun transfert d'un agent à l'autre |
| Demo Lab OANDA/MT5 Demo | 🟡 | OANDA Practice en lecture de prix uniquement ; MT5 = V3 |
| Demo Lab Saxo | ⛔ | Accès OpenAPI refusé par Saxo (16/09) |
| Risk Engine par position (risque, pertes consécutives, spread, glissement, fréquence) | ✅ | Dans le moteur, par agent |
| Risk Engine **global** (exposition totale, corrélation, arrêt automatique de portefeuille) | ❌ | Aucun plafond d'exposition entre marchés/agents |
| Compliance Gate | 🟡 | Table de statuts affichée ; aucun mécanisme qui bloque réellement une fonction selon le statut |
| Audit Trail (paramètres, versions, décisions, résultats, erreurs) | 🟡 | Journal et versions conservés ; historique d'auto-évolution limité à 12 événements par agent ; pas d'export |
| Séparation stricte DEMO / LIVE, LIVE désactivé | ✅ | Aucun ordre possible |
| Métriques Arena : rendement, drawdown, profit factor, Monte-Carlo, OOS | ✅ | |
| Métriques Arena : stabilité, volatilité des résultats, résistance spread/slippage (stress), performance par régime | ❌ | |
| Métriques Arena : walk-forward | ❌ (V12) / 🟡 (labo éducatif) | |
| Les meilleurs agents proposent des variantes qui repassent les tests | ✅ | StrategyTune + Auto-évolution (voir réserves du plan, constats 14–15) |
| Démarche AMF | ❌ | Aucune trace d'envoi |
| Démarche ACPR | 🟡 | Réponse le 18/09 : **document de présentation demandé**, pas encore envoyé (selon Gmail) |
| Démarche OANDA (ticket #07312883) | 🟡 | Renvoyé vers le support UE (OTMS) ; API annoncée indisponible pour OTMS |
| Démarche Saxo | ⛔ | Refus |
| MetaTrader : documenter Python/MT5 | ❌ | |
| TradingView : alertes/webhooks | 🟡 | Webhook sécurisé présent dans Jégouzo Vision, pas relié au V12 |
| France FinTech, Finance Innovation, French Tech, Station F, Bpifrance | ❌ | Aucune trace |
| cTrader (contact non prévu au dossier) | 🟡 | Spotware invite à déposer une application Open API |
| Principe : jamais se dire agréé/partenaire sans écrit | 🟡 | Respecté dans le V12 ; le labo éducatif liste 11 brokers « Demo/Live séparés » sans accord |

---

## 3. Visuel V10 « Toile éternelle » (S3)

| Décision | État | Constat |
|---|---|---|
| Force relative des 8 devises | ❌ | Valeurs simulées dans le labo éducatif (aucun calcul réel) |
| Scan des 28 paires | 🟡 | Backtestées dans Multi-marchés et la Chasse ; pas de scan/classement en continu |
| Carré 1 · Tendance H1 (EMA 50/200, structure) | ✅ | Référence V12 : EMA 50/200 H1 |
| Carré 2 · Force D1/H4 (force relative, accélération, rotation, divergences) | ❌ | |
| Carré 3 · Momentum M15/M5 (RSI, volume, ATR, VWAP) | ✅ | |
| Carré 4 · Liquidité (ouverture Londres, breakout, retest, spread, volatilité) | 🟡 | Sessions et spread max seulement |
| Confluence des 4 carrés + classement score/100 | ❌ | |
| Capital 100 € : risque 0,25 %/trade, max 0,50 %, risque global 1 %, 3 positions max, DD jour 2 %, DD total 10 %, arrêt si DD | 🟡 | Agents à 0,5 % ; perte jour 1 % ; pas de risque global, pas de limite de 3 positions ; arrêt DD optionnel (désactivé). Voir conflit C1 |
| Cycle Spider en 8 étapes (scan → analyse → score → risque → entrée → suivi → sortie/apprentissage → recommencer) | 🟡 | Réalisé en backtest ; pas de boucle en avant journalisée |
| Statistiques journalières (jour/semaine/mois, réussite, PF, DD, meilleure/pire paire) | 🟡 | Disponibles par backtest, pas en suivi quotidien |
| Étapes : Backtest → Optimisation → Paper trading → Démo → Réel | 🟡 | Backtest ✅ · Optimisation ✅ · Paper 🟡 (suivi en avant de l'auto-évolution) · Démo ❌ · Réel ⛔ |
| Objectif « 0,20 % à 0,50 % par jour » | ⛔ | À ne pas utiliser en communication (risque AMF) |

---

## 4. Couche « V12 Extension Layer » du labo éducatif (S4)

| Décision | État | Constat |
|---|---|---|
| Spider Intelligence Score explicable (11 facteurs) | ❌ | Valeurs écrites en dur ; le bouton « recalculer » les décale arbitrairement |
| Pipeline StrategyTune : Génération → Backtest → Walk-Forward → OOS → Promotion LAB → VALIDATION → APPROVED | 🟡 | Walk-forward et états de promotion formels absents du V12 |
| Global Spider Grid (8 pattes) | ❌ | Visuel seulement (prévu V3), alors que le Gold Command Center l'affiche « actif » avec des scores fixes (Spider Alpha 96/100, Sentinel 98/100) |
| Universal Broker Gateway (11 brokers) | ❌ | Seul OANDA Practice en lecture. Saxo refusé ; Binance contredit l'exclusion crypto |
| Chaîne Market Data → Normalisation → Agents → Sentinel → Risk → Compliance → Execution Gate | 🟡 | Agents et risque par agent ; pas de Sentinel/Compliance/Execution Gate réels dans le V12 |
| Auto-amélioration contrôlée : analyse d'erreurs, baseline/variante/OOS, walk-forward anti-surapprentissage, promotion versionnée + rollback, « Strategy DNA » | 🟡 | Versions + rollback ✅ ; analyse d'erreurs et walk-forward ❌ |
| Persistance : save/restore Spider Alpha, rotation 12 h de l'historique opérationnel, traçabilité | 🟡 | Sauvegarde côté navigateur pour l'Unified Core ; « rotation 12 h » affichée dans l'interface mais aucun mécanisme côté serveur |
| Battle Royale : métriques par régime, replay | 🟡 | Replay ✅ (V12) ; régimes ❌ |
| Human Trading (tests de 10 min, humain vs agents) | ❌ | |
| Economic Calendar Hub | ✅ | Calendrier + archivage automatique par semaine (tâche horaire) |
| Money Management avec kill switch | 🟡 | Limites par agent ✅ ; kill switch global ❌ |
| Détection de régime (NORMAL, TREND, RANGE, HIGH VOL, NEWS) | ❌ | Choix manuel seulement |
| Indicateurs Fibonacci, Order Blocks, Liquidity, Market Structure | 🟡 | Order blocks dans le scanner du labo éducatif ; absents du moteur V12 |

---

## 5. « Prochaine vague d'amélioration » Jarvis Evolution (S5)

| Décision | État |
|---|---|
| Données or indépendantes de Yahoo | 🟡 OANDA Practice (spot) branché pour l'or dans le V12 ; pas dans le labo éducatif |
| Spread, glissement, commissions et latence dans les simulations | 🟡 Spread + glissement ✅ (V12) ; commissions et latence ❌ |
| Walk-forward sur plusieurs régimes | ❌ |
| Benchmark permanent, promotion seulement si le score augmente | 🟡 Auto-évolution (critère à corriger, plan constat 14) |
| Graphe de connaissances Or (banques centrales, ETF, CFTC, CME, macro) | ❌ (liste de sources seulement) |
| Code exécuté en sandbox isolé avant toute proposition de déploiement | ❌ |
| Paramètres V12 actuels = baseline immuable | ✅ |

---

## 6. Collaboration ChatGPT ↔ Claude ↔ StrategyTune (S6)

| Décision | État |
|---|---|
| Pont MCP isolé, lecture seule, notes « en attente de revue », jeton obligatoire | ⛔ PR fermée sans fusion, jamais déployé |
| Import des rapports StrategyTune en JSON | ❌ |
| GitHub comme source de vérité partagée (`docs/`) | 🟡 Ce dossier `docs/` existe désormais ; le code des apps n'est pas encore versionné |
| Critères minimum avant promotion (pas d'anticipation, walk-forward, coûts réalistes, drawdown, plusieurs régimes) | 🟡 Anticipation ✅, coûts ✅ ; walk-forward et régimes ❌ |

---

## 7. Décisions arrêtées le 14/10/2026 (ex-conflits C1 à C6)

| # | Sujet | Décision | Appliqué dans |
|---|---|---|---|
| **C1** | Risque par trade | **Plafond absolu 0,5 % partout.** Recherche V12 à 0,5 % (valeur de la Référence, inchangée). Démo et réel (profil 100 €, futur pont MT5) à **0,25 %**, risque global 1 %, 3 positions maximum. | Labo V12 : saisie et serveur plafonnés à 0,5 %, profil Arena ramené de 1 % à 0,5 %. Labo éducatif : agents à 0,5 %, profil 100 € à 0,25 € (au lieu de 0,05 €), réglages plafonnés à 0,5 % |
| **C2** | R:R de référence | **1,5** (robot MT5 et Référence V12). 2,0 reste une variante à tester. Chaque agent garde son propre R:R du registre V12. | Labo V12 (Cockpit). Labo éducatif : R:R des agents alignés (au lieu de 2 pour tous) |
| **C3** | Crypto | **Exclue de tout l'écosystème** tant que MiCA est bloqué. | Labo éducatif : BTC/ETH retirés du terminal, du tableau Battle (onglet Crypto supprimé), des visuels, de la liste brokers ; MiCA passé en « bloqué » ; le serveur refuse l'analyse d'un symbole crypto. Bot : BTC/USD remplacé par GBP/JPY |
| **C4** | Broker démo V3 | **OANDA MT5 (OANDA TMS) via le pont Python local**, démo d'abord. Plan B : IBKR Paper. cTrader : candidature possible. Saxo : accès refusé, abandonné. Axi non retenu. | Labo V12 (Cockpit, feuille de route V3). Labo éducatif : liste brokers réduite à 4 statuts factuels, Saxo marqué « accès refusé », Sentinel verrouillé sur « pont MT5 requis » |
| **C5** | Fuseau des sessions | **Heure de Paris.** L'heure serveur MT5 est convertie à l'import CSV et par le futur pont. | Labo V12 (Cockpit). Labo éducatif : profil 100 € et protocole indiquent Europe/Paris |
| **C6** | Registre des agents | **Le registre du Labo V12 fait foi.** | Labo éducatif : les 7 agents de la Battle reprennent noms et paramètres V12 (EMA, RSI, ATR, R:R, risque, limites, filtres, unité M5) ; les anciens réglages enregistrés dans le navigateur ne sont plus rechargés |

Ce qui reste du ressort du porteur : confirmer par écrit auprès du support OANDA OTMS que l'usage d'un robot MT5 en démo est autorisé, fournir le robot .mq5 et les exports MT5, choisir PC ou VPS Windows.

---

## 8. Ce qu'il reste à lancer pour boucler la V2

Dans l'ordre :
1. ~~Trancher C1 à C6~~ ✅ fait le 14/10/2026 (section 7).
2. **Walk-forward dans le moteur V12** (dernier engagement V2 non tenu) — plan, Lot 2.4.
3. **Vérité des données du labo éducatif** : force des 8 devises, Spider Intelligence Score et Battle calculés sur données réelles, ou marqués fictifs — plan, Lot 1.
4. **Risk Engine global** (risque total 1 %, 3 positions max, DD jour 2 %, DD total 10 %, kill switch) — décision V10 + dossier S2.
5. **Libellés exacts** : « 6 modes » ✅ et statut des brokers ✅ corrigés le 14/10 ; reste le retrait du « LIVE-READY ».
6. **Dossier de présentation ACPR** (demandé le 18/09) puis démarche AMF.
7. Fournir les éléments « En attente de ta part » (robot .mq5, exports MT5) pour préparer la V3.

---

## 9. Jeux de réglages des agents (Labo V12, onglet Agents) — mis en ligne le 15/10/2026

Demande : depuis l'onglet **Agents** (tableaux, graphiques et réglages des 8 agents), pouvoir **enregistrer les réglages des agents** puis les **tester dans les autres modes**, en particulier **Battle** et **Évaluation (Rapport A–F)**.

| Élément | Ce qui a été fait |
|---|---|
| Enregistrer | Encadré « Jeux de réglages (les 8 agents) » : un nom, une note facultative, puis « Enregistrer les réglages des 8 agents ». Le jeu garde les paramètres des 8 agents tels qu'ils sont à l'écran, la liste des agents modifiés par rapport à l'origine et la période de données utilisée. Stockage sur le serveur, réservé au propriétaire, jamais supprimé. Le serveur revérifie chaque agent (mêmes limites que les versions, risque ≤ 0,5 % selon C1). |
| Recharger | « Charger dans l'éditeur » remet les réglages d'un jeu dans l'onglet Agents. Le journal note quels agents ont été remplacés. |
| Battle | Choix des paramètres testés : réglages actuels, profils d'origine ou un jeu enregistré, avec l'option « Comparer avec une 2e source ». Les deux sources courent côte à côte : jusqu'à 16 courbes, la seconde en pointillés. Raccourcis « Battle de ce jeu » et « Battle contre l'origine » depuis la liste des jeux. Les résultats de l'onglet Agents ne sont pas écrasés, et le Cockpit indique de quel jeu vient le meilleur agent. |
| Évaluation | Onglet Rapport A–F : choix « Paramètres évalués ». Le rapport est recalculé sur le jeu choisi et affiche « Évalué avec : … ». L'évaluation est bloquée si les coûts sont invalides. Un résultat devenu périmé est signalé. |
| Autres modes | Lancer / Arène : « Charger ce jeu dans le tableau ». Multi-marchés : choix de la source des paramètres. |
| Brouillon | Les réglages en cours sont gardés sur l'appareil et retrouvés après un rechargement de la page, même si le journal est momentanément indisponible. Seuls les champs modifiés sont conservés : une mise à jour du registre V12 s'applique donc toujours aux autres champs. Un agent réglé explicitement sur l'appareil n'est jamais écrasé par le rechargement automatique des versions. Cela vaut pour une édition, un « Réinitialiser », une version restaurée ou un jeu chargé. Deux onglets ouverts n'effacent plus les réglages l'un de l'autre, et un message prévient quand un autre onglet les a changés. Une valeur hors limites est reprise telle quelle et signalée, jamais corrigée. |
| Fiabilité | Un message « Chargement des jeux… » s'affiche pendant le chargement. Une panne est affichée avec un bouton « Réessayer », et les jeux se chargent même si le journal est indisponible. Jusqu'à 500 jeux sont listés. Un double appui n'enregistre qu'un seul jeu. Les jeux sont identifiés par leur nom et leur date partout (Battle, Rapport, Cockpit, Multi). Une note longue se déplie d'un toucher. Le journal a un type dédié « Jeu de réglages ». |

Hors périmètre, inchangé : la Chasse et l'Auto-évolution partent toujours du registre V12 côté serveur (C6).

Vérifications avant mise en ligne :
- relecture adverse en trois passes, sans défaut bloquant :
  - 1re passe : 20 défauts mineurs confirmés ;
  - 2e passe : 9 autres, dont un important sur le brouillon ;
  - 3e passe : 3 cas limites (passage de 100 versions, horloge décalée, deux onglets) ;
  - tous corrigés puis revérifiés ;
- typage strict sans erreur ;
- dix scénarios simulés, couvrant :
  - l'enregistrement d'un jeu ;
  - la Battle à 1 ou 2 sources ;
  - le Rapport A–F, Lancer et Multi-marchés ;
  - le brouillon après rechargement (journal en panne, plus de 100 versions, deux onglets) ;
  - la pagination, les pannes et le double appui ;
- après mise en ligne : aucune erreur interface ni serveur, tâches planifiées (Chasse, Auto-évolution) toujours en succès, et code en ligne identique à la version testée (nombre de lignes de chacun des 13 fichiers modifiés).
