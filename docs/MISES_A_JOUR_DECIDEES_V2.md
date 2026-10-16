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
2. ~~**Walk-forward dans le moteur V12**~~ ✅ mis en ligne le 16/10/2026 (section 10).
3. **Vérité des données du labo éducatif** : force des 8 devises ✅ sur données réelles et Battle ✅ marquée « chiffres fictifs » le 16/10/2026 (section 11) ; reste le Spider Intelligence Score — plan, Lot 1.
4. **Risk Engine global** (risque total 1 %, 3 positions max, DD jour 2 %, DD total 10 %, kill switch) — décision V10 + dossier S2.
5. **Libellés exacts** : « 6 modes » ✅ et statut des brokers ✅ corrigés le 14/10 ; « LIVE-READY » / « LIVE ENGINE » ✅ retirés le 16/10/2026 (section 11).
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

---

## 10. Moteur et auto-évolution du Labo V12 — mis en ligne le 16/10/2026

Plan d'améliorations, lots 1.6, 2.1 à 2.8 et 4.1 à 4.3. Rien n'envoie d'ordre : tout reste du calcul sur barres clôturées.

| Lot | Ce qui a été fait |
|---|---|
| 2.1 Découpage après échauffement | Les 60/20/20 % (recherche, validation, test final) commencent à la première barre où les indicateurs de tous les agents du registre sont prêts ; aucun trade pendant l'échauffement. Si l'échauffement dépasse la moitié de l'historique (timeframes M15, M30, H1 sur 59 jours), l'ancien découpage est gardé et le rapport l'indique. |
| 2.2 Taille de position | Le lot est calculé sur la perte réelle au stop, glissement compris : perte au stop ≤ risque affiché, hors écart d'ouverture. |
| 2.3 Raccords de contrat GC=F | Les sauts d'échéance du contrat à terme sont détectés (saut positif de 0,25 à 1,5 %, en fin ou début de mois, qui tient au moins une heure, un au plus par 35 jours) et neutralisés par ajustement proportionnel des prix antérieurs. Le rapport (section A) affiche la date et la taille du saut, ou « aucun saut détecté ». Limite : validé sur sauts simulés, à confirmer sur les données réelles. |
| 2.4 Walk-forward | StrategyTune → « Walk-forward (4 fenêtres) » : la variante choisie sur le passé est mesurée sur la tranche suivante, quatre fois. Verdict stable / mitigé / instable / échantillon insuffisant ; section G du rapport. Le test final masqué n'est jamais utilisé. |
| 2.5 Bootstrap par journées | Les trades d'une même journée sont tirés ensemble ; p-value « par journées » affichée à côté de la p-value trade par trade, la plus prudente fait foi. |
| 2.6 Jarvis Alpha, 9e agent | La règle de fusion (au moins 2 agents entrés au même moment dans le même sens, aucun désaccord, tendance H1 commune ≥ 60 %) est rejouée par le même moteur, avec les mêmes coûts. Jarvis apparaît dans Battle, Rapport et Chasse. |
| 2.7 Indicateurs | Sharpe et Sortino journaliers, exposition, durée moyenne d'un trade, coût moyen en R (section C du rapport). |
| 2.8 Tests du moteur | Suite de 13 tests exécutée avant chaque déploiement : déterminisme, absence d'anticipation (y compris trade par trade), découpage, comptabilité, taille de position, limites de risque, walk-forward, bootstrap, Jarvis, raccords GC=F. Trois défauts volontairement introduits ont tous été détectés. |
| 1.6 Libellé de l'or | « Or — contrat à terme COMEX (GC=F) » avec Yahoo, « Or spot XAU/USD » avec OANDA Practice ou un export MT5. |
| 4.1 Espérance ancrée | Une nouvelle version d'un agent ne peut plus être adoptée avec une espérance inférieure à celle de l'agent d'origine (avant : jusqu'à 10 % sous le champion du moment, ce qui permettait une dérive de génération en génération). |
| 4.2 Choix prudent | Le taux de réussite reste la condition d'adoption ; entre plusieurs candidats acceptés, la borne basse de l'espérance (95 %) décide. |
| 4.3 Période d'essai | Une version adoptée reste « à l'essai » jusqu'à 20 trades arrivés après son adoption : confirmée si leur espérance est positive et au moins égale à celle de la base, sinon retour arrière automatique. Les versions déjà en place passent aussi par cet essai. |

Vérifications : 13 tests du moteur et 13 tests de l'auto-évolution réussis, typage strict sans nouvelle erreur, 9 scénarios d'interface simulés (Battle à 9 participants, Rapport, walk-forward, jeux de réglages). Après mise en ligne : aucune erreur interface ni serveur, tâches planifiées (Chasse, Auto-évolution) en succès.

---

## 11. Labo éducatif : vérité des données et protection — mis en ligne le 16/10/2026

| Lot | Ce qui a été fait |
|---|---|
| 1.1 Force des 8 devises | La matrice n'utilise plus de valeurs simulées : la force de chaque devise est la variation moyenne sur 24 h de 15 paires réelles (bougies 1 h différées). Une paire indisponible est signalée, une devise sans donnée affiche « n.d. ». Le graphique d'une paire montre ses 12 dernières heures réelles (directe, inversée ou croisée via USD), sinon « évolution indisponible ». Badge « FORCE RÉELLE · 24 h · date » ou « DONNÉES INDISPONIBLES ». |
| 1.2 Battle | Bandeau permanent « DÉMO VISUELLE — chiffres fictifs » : les courbes et classements de l'arène ne viennent ni de cotations ni du moteur V12. Bouton « ACTUALISER » des résultats des agents corrigé (il ne déclenchait rien). |
| 1.3 Libellés | « LIVE-READY » et « LIVE ENGINE » remplacés par « RECHERCHE · DÉMO · AUCUN ORDRE ». |
| 0.2 Protection | Les routes de calcul qui téléchargent des données de marché (analyse de marché, corrélations, flux des agents de la Battle) sont réservées au propriétaire, comme les routes d'IA. Le test éducatif d'un agent reste ouvert aux comptes connectés avec un quota de 30 tests par heure et par compte. |

Vérifications : calcul de force contrôlé à la main sur un jeu de paires (classement attendu retrouvé), séries de paires et quota testés, typage strict sans erreur. Après mise en ligne : aucune erreur interface ni serveur.

Décision du 16/10/2026 : l'application « Bot » est abandonnée (elle n'apparaît plus dans le compte d'hébergement) ; le lot 1.5 est clos sans suite.


---

## 12. Sauvegarde et budget de tests du Labo V12 — mis en ligne le 16/10/2026

| Lot | Ce qui a été fait |
|---|---|
| 0.6 Sauvegarde | Onglet Journal → « Exporter une sauvegarde (JSON) » : un fichier daté réunit tout le journal des expériences, les versions sauvegardées, les jeux de réglages, ainsi que l'état de l'auto-évolution et de la Chasse. Toutes les pages sont parcourues ; si le journal, les versions ou les jeux ne peuvent pas être lus en entier, l'export est refusé plutôt que tronqué. Une panne de l'auto-évolution ou de la Chasse est notée dans le fichier. Lecture seule : rien n'est modifié. |
| 4.4 Budget global de tests | Le seuil de significativité de l'auto-évolution se durcit avec le nombre total de challengers déjà testés pour chaque agent : seuil de la Chasse (p corrigée ≤ 0,1) pour les 100 premiers, puis baisse comme la racine du nombre d'essais (÷ 2 à 400, ÷ 10 à 10 000). Le seuil en vigueur est affiché à côté du nombre de challengers testés. Conséquence attendue : moins d'adoptions, chacune mieux établie. |

Vérifications : 8 tests dédiés (pagination complète sans doublon, refus d'un export incomplet, panne partielle notée, seuil décroissant), 13 tests du moteur et 13 tests de l'auto-évolution réussis, typage strict sans nouvelle erreur, export vérifié dans l'interface simulée. Après mise en ligne : aucune erreur interface ni serveur.

---

## 13. Consommation de crédits d'hébergement réduite — mis en ligne le 16/10/2026

Constat : le plafond de 1 000 crédits par jour du forfait d'hébergement avait été atteint le 15/10, ce qui suspend les déploiements **et** l'usage des apps jusqu'au lendemain. Seules les deux apps Spider ont des tâches automatiques ; la revue Sentinel par IA était déjà désactivée et ne consommait rien.

| Source de consommation | Avant | Après |
|---|---|---|
| Labo éducatif : pages cachées | Toutes les pages restent chargées ; tant que l'app est ouverte, même sur une autre page ou en arrière-plan, la Battle recalculait les agents côté serveur toutes les 10 s et le centre de décision interrogeait le serveur toutes les 30 s (environ 480 appels par heure) | Rafraîchissement seulement quand la page concernée est affichée et l'onglet du navigateur visible, au plus une fois par minute ; calendrier et force des devises également suspendus en arrière-plan |
| Labo V12 : auto-évolution | Tâche toutes les 5 min, un cycle par agent toutes les 20 min (backtests relancés sur des données quasi identiques) | Tâche toutes les 15 min, un cycle par agent toutes les 2 h |
| Labo V12 : Chasse | Tâche toutes les 5 min | Toutes les 15 min (une chasse complète par semaine, inchangé) |
| Labo éducatif : cycle Sentinel | Toutes les 15 min (13 marchés analysés) | Toutes les heures |
| Labo éducatif : optimisation Jarvis native | Toutes les 30 min | Toutes les 6 h |
| Labo éducatif : archive du calendrier | Toutes les heures | Toutes les 6 h |
| Labo éducatif : revue Sentinel par IA | Désactivée mais réveillée toutes les heures pour ne rien faire | Retirée de la planification |
| Labo éducatif : analyses de marché à l'ouverture | Terminal, labo d'indicateurs et labo risque téléchargeaient et recalculaient le marché dès l'ouverture de l'app, et de nouveau à chaque clic sur une paire de la matrice, même pages cachées | Chargement seulement quand la page concernée est affichée (module commun « pageGate », 8 tests) |

Effet attendu : les exécutions automatiques passent d'environ 744 à environ 200 par jour (−73 %), et le calcul de l'auto-évolution est divisé par environ 5. Les fonctions restent les mêmes : seuls les rythmes changent. Après mise en ligne : aucune erreur interface ni serveur, nouvelles planifications actives.


---

## 14. Graphiques « comment il joue » sur chaque agent — mis en ligne le 16/10/2026

Demande : voir chaque agent, dans chacun des deux labos, jouer en temps réel sur un graphique.

| Labo | Ce qui est affiché |
|---|---|
| Labo V12, onglet Live (8 agents) | Chaque carte : prix, entrées ▲▼ et sorties ● des derniers trades (vert gagnant, rouge perdant), et quand l'agent est en position ou en signal, les lignes Entrée / Stop / Objectif. Sous le graphique, un bandeau « Comment il joue » : courbe de résultat cumulé en R, résultat latent de la position ouverte et les 3 derniers trades datés. |
| Labo V12, onglet Live (Jarvis) | Nouvelle carte Jarvis : même graphique pour le chef d'orchestre, construit à partir des signaux des 8 agents, avec sa position ouverte. |
| Labo éducatif, Battle | Chaque carte d'agent : rejeu des 60 dernières bougies (prix, EMA rapide / lente de l'agent, entrées ▲▼, sorties ●, stop et objectif de la position ouverte), bande ACHAT / VENTE / ATTENTE bougie par bougie, nombre de trades, gagnants et total en R. |

Règles : aucune anticipation (à chaque bougie, l'agent ne voit que les bougies déjà closes), stop compté en premier si stop et objectif sont touchés dans la même bougie, résultats en R et sans frais (démonstration), aucun ordre envoyé. Si le fournisseur de données est indisponible, la carte l'indique : le rejeu n'est alors pas représentatif.

Coût : aucun appel serveur supplémentaire. Dans le Labo V12, les graphiques réutilisent les calculs déjà faits par l'onglet Live dans le navigateur. Dans le labo éducatif, le rejeu est calculé dans la même requête que la Battle, qui reste limitée à une fois par minute, page affichée seulement.

Vérifications : score du rejeu identique au calcul live sur 78 points sur 78, absence d'anticipation, au plus une position ouverte, agent neutre sans trade (8 tests) ; marqueurs et lignes vérifiés dans l'interface simulée ; 13 tests du moteur réussis ; typage strict sans nouvelle erreur.

---

## 15. Registre d'évolution du 12/09/2026 : état au 16/10/2026

Le registre d'évolution du 12/09 (cahier de préparation de la prochaine mise à jour) a été comparé au code réellement en ligne dans le Labo V12 et le labo éducatif. Légende : ✅ en ligne et testé · 🟡 partiel · ❌ absent.

| Rubrique du registre | État | Ce qui existe / ce qui manque |
|---|---|---|
| 2. Cœur Spider Matrix (toile, œil, zéro, relations) | 🟡 | Labo éducatif : toile animée avec œil et zéro central, matrice croisée des paires, force des devises calculée sur données réelles. Manque : dans chaque cellule, la position de la valeur par rapport au zéro central (écart relatif visible en mouvement). |
| 3. Agent IA de marché | ✅ | Analyses structurées (régime, thèse, risques, points à surveiller, confiance) sur les seules données fournies, consensus multi-agents, plans entrée / stop / objectif dans l'onglet Live du V12, rejeu « comment il joue » de chaque agent (section 14). |
| 4. Marchés | 🟡 | V12 : 46 marchés (devises, or, pétrole, indices, actions). Cryptoactifs exclus du V12 par décision ; labo éducatif : sélection plus courte. |
| 5. Caméra / analyse visuelle | ❌ | Aucune lecture de capture d'écran ni extraction de valeurs. À construire : image réduite et compressée dans le navigateur avant envoi, extraction en petit tableau corrigeable à la main, analyse lancée seulement sur les valeurs confirmées. |
| 6. OANDA v20 / Practice | 🟡 | V12 : lecture seule Practice (or, EUR/USD), historique M5 multi-pages pour le backtest et l'auto-évolution, statut avec latence. Manque : prix achat / vente (bid / ask) réels et spread historique dans les simulations (le spread est aujourd'hui modélisé), tableau de diagnostic complet (connexion, fraîcheur des données, erreurs, latence). Point ouvert : confirmation écrite d'OANDA sur l'usage du jeton Practice (section 3). Spider Matrix n'est présenté nulle part comme un produit OANDA. |
| 7. Backtest et validation | ✅ | Moteur M5 avec frais, spread et glissement, découpage 60/20/20 après échauffement, walk-forward, comparaison multi-périodes et multi-marchés, rapport A–F, correction des tests multiples (Chasse, auto-évolution). |
| 8. Conformité et risque | 🟡 | Règles fixes appliquées (risque max par trade, stop obligatoire, limite de perte journalière, validation humaine, aucune exécution), pages conformité France / UE, frais et pénalités. Manque : simulation du levier, de la marge, des appels de marge et des clôtures forcées ; profils réglementaires actualisables par entité et juridiction ; gestion explicite des gaps et des périodes de faible liquidité. |
| 9. Chaîne de sécurité des ordres | ✅ | Aucune fonction n'envoie d'ordre réel : toute recommandation reste une proposition. Le Bot est abandonné (section 13). |
| 10. Journal d'audit | 🟡 | V12 : journal des expériences (paramètres, résultats, versions, sauvegarde JSON). Manque : une fiche par analyse importante avec instrument, heure, données utilisées, signal, confiance, risque, taille, spread / glissement estimés, raisons, décision finale et anomalies. |
| 12. État de déploiement | — | Le blocage « 125/125 déploiements » ne s'applique plus : les deux apps ont été mises à jour le 16/10. La contrainte actuelle est le plafond quotidien de crédits d'hébergement (section 13). |

Lots proposés pour la prochaine mise à jour, par ordre de valeur pour le coût :

| Lot | Contenu | Où |
|---|---|---|
| R1 | Marge et levier dans le backtest : profil réglementaire choisi (par défaut : limites de levier pour clients particuliers en UE), marge immobilisée par position, niveau de marge, appel de marge, clôture forcée simulée, protection contre le solde négatif ; profils datés et modifiables, jamais présentés comme les règles d'une entité OANDA précise | Labo V12 |
| R2 | Journal d'audit par analyse (fiche complète, lecture seule, export JSON) | Labo V12 puis labo éducatif |
| R3 | Diagnostic des sources (connexion, fraîcheur, barres manquantes, erreurs, latence) | Labo V12 |
| R4 | Bid / ask OANDA réels dans les simulations quand la source OANDA est choisie | Labo V12 |
| R5 | Caméra : lecture de capture, tableau corrigeable, analyse sur valeurs confirmées | Labo éducatif |
| R6 | Cellules de la matrice : position de la valeur par rapport au zéro central | Labo éducatif |

Règle conservée : une fonction n'est notée « en ligne » qu'après tests et publication effective.

---

## 16. Lot R1 — marge et levier simulés dans le Labo V12 — mis en ligne le 16/10/2026

Réponse à la rubrique 8 du registre d'évolution (moteur de conformité et de risque) : chaque backtest du Labo V12 simule désormais la marge et le levier.

| Élément | Comportement |
|---|---|
| Profil par défaut | « Particulier UE (limites ESMA) », vérifié le 16/10/2026 : levier maximal 30:1 sur les paires formées de USD, EUR, JPY, GBP, CAD et CHF ; 20:1 sur les autres paires et l'or ; 10:1 sur les autres matières premières et l'indice dollar (classement prudent) ; clôture forcée à 50 % de la marge initiale ; protection contre le solde négatif. Base : mesures d'intervention de l'ESMA sur les CFD pour particuliers, reprises par les autorités nationales. |
| Autres profils | « Personnalisé » (levier 1:1 à 500:1, clôture forcée de 20 à 90 %) et « Désactivé ». Choix dans Coûts & contrat. Les règles réelles dépendent du courtier, de l'entité et de la juridiction : le labo le rappelle et ne présente aucun profil comme les règles d'un courtier précis. |
| Contrôle avant l'ordre | Marge initiale = valeur de la position ÷ levier, jamais plus que les fonds propres : le lot est réduit, ou le signal est refusé si même le lot minimum ne tient pas. L'onglet Live affiche alors « Marge insuffisante ». |
| Pendant la position | Alerte de marge comptée quand, au pire prix de la bougie, les fonds propres passent sous la marge initiale. Clôture forcée simulée si le seuil est atteint avant le stop (sortie « clôture forcée »). |
| Gaps | Sortie de perte exécutée au prix d'ouverture quand le marché saute le stop ; nombre de cas et pire dépassement en R affichés. |
| Solde négatif | Perte plafonnée au solde du compte ; montant non débité affiché. |
| Affichage | Résumé « Marge » dans l'onglet Agents, le détail Multi-marchés et le rapport A–F, avec avertissement si une clôture forcée ou un plafonnement au solde survient. Capitaux de 100, 250 et 500 $ ajoutés pour tester les petits comptes. |

Ce qui ne change pas : avec les réglages par défaut (10 000 $, lot max 0,1, risque ≤ 0,5 % par trade), aucune contrainte de marge n'est atteinte et les résultats sont identiques à ceux d'avant (vérifié sur les 8 agents, or et EUR/USD). Avec un risque plafonné à 0,5 % (décision C1), le stop passe toujours avant la clôture forcée ; celle-ci reste un filet de sécurité pour les écarts d'ouverture et les profils personnalisés.

Vérifications : 9 tests dédiés (catégories ESMA, résultats inchangés par défaut, marge jamais supérieure aux fonds propres, réduction de lot et alertes à 1:1, écart d'ouverture avec protection du solde, clôture forcée au seuil exact, résumés), 13 tests du moteur et 13 tests de l'auto-évolution réussis, parcours de l'interface vérifié (profil ESMA → personnalisé 1:1 → désactivé), typage strict sans nouvelle erreur.

Lots suivants du registre : R2 journal d'audit par analyse, R3 diagnostic des sources, R4 prix achat / vente OANDA réels, R5 caméra, R6 cellules de la matrice.

---

## 17. Lot R2 — journal d'audit par analyse dans le Labo V12 — mis en ligne le 16/10/2026

Réponse à la rubrique 10 du registre d'évolution. Une « analyse importante » est un signal d'un agent dans l'onglet Live, ou un signal bloqué (limites de risque, spread, lot ou marge) : chacune produit une fiche, enregistrée une seule fois sur le compte, jamais modifiée ni supprimée.

| Contenu de la fiche | Détail |
|---|---|
| Marché et heure | Instrument, bougie décisive (décision à sa clôture), heure d'enregistrement |
| Données utilisées | Source, prix différés ou non, nombre de bougies, début des données, âge de la dernière bougie |
| Paramètres | Réglages complets de l'agent et liste des réglages modifiés par rapport au profil d'origine |
| Signal | Sens, étapes franchies (tendance, repli, croisement, horaire, volume, Hurst, VWAP, ADX) |
| Confiance mesurée | Résultats passés de l'agent sur les données chargées : trades, réussite, espérance, facteur de profit, drawdown |
| Risque et taille | Entrée, stop, objectif, lots, montant risqué, % de risque, R:R |
| Coûts | Spread et glissement estimés |
| Marge | Profil, levier maximal, marge requise et part des fonds propres (lot R1) |
| Raisons, décision, anomalies | Raisons de l'agent ; décision « proposition simulée, aucun ordre envoyé » ou « refusé » avec la cause ; anomalies (données différées, flux figé, filtres ignorés, échantillon trop court) |

Consultation dans l'onglet Journal (liste, détail, export JSON complet) ; le journal d'audit est aussi inclus dans la sauvegarde. Les fiches sont enregistrées tant que l'onglet Live est ouvert ; aucune tâche serveur n'est ajoutée (une écriture par signal, quelques-unes par jour).

Vérifications : 23 tests dédiés (une fiche par signal ou blocage et aucune pour les autres états, plan identique à l'affichage, risque ≤ % autorisé, marge ≤ fonds propres, identifiant stable, anomalies, refus motivé, enregistrement sans doublon, refus des fiches invalides ou trop grosses, accès réservé au propriétaire, sauvegarde complète), parcours de l'interface (3 signaux enregistrés, aucun renvoi à la réouverture, liste, détail et export), tests du moteur, de la marge, de la sauvegarde et de l'auto-évolution réussis.

---

## 18. Lot R3 — diagnostic des sources dans le Labo V12 — mis en ligne le 16/10/2026

Réponse à la rubrique 6 du registre d'évolution (tableau de diagnostic : connexion, données, flux, erreurs, latence). Nouvel onglet « Diagnostic », lancé à la demande seulement : aucune interrogation en arrière-plan, donc aucun crédit consommé tant qu'on ne clique pas.

| Source contrôlée | Ce qui est mesuré |
|---|---|
| Yahoo Finance (récent, différé) | Connexion, latence aller-retour, nombre de bougies, âge de la dernière bougie, bougies manquantes, bougies incohérentes ou en double, retours en arrière dans le temps, bougies sans mouvement, présence du volume |
| OANDA Practice, prix récents (or, EUR/USD) | Mêmes mesures |
| OANDA Practice, compte en lecture seule | Jeton configuré ou non, connexion acceptée ou refusée, latence serveur → OANDA, nombre de comptes |
| Données chargées dans le labo | Mêmes mesures de qualité sur l'historique de 59 jours ; fraîcheur mesurée au moment du chargement |
| Concordance Yahoo / OANDA | Bougies communes, écart médian et dispersion de l'écart en points ; pour l'or, l'écart constant entre contrat à terme et prix spot (la base) est signalé comme normal |

Règles : le week-end et la pause quotidienne ne comptent pas comme des trous. Un flux ancien est normal le week-end et signalé en semaine (retard, panne ou jour férié). Verdict par source : Bon, À surveiller (trous > 0,5 %, flux en retard, bougies figées), Inutilisable (aucune bougie, bougies incohérentes, doublons, série non triée, échec de connexion). Les 20 derniers diagnostics restent visibles sur l'appareil.

Vérifications : 19 tests dédiés (série propre, 25 fermetures normales reconnues, trous de 30 min et de 5 h, doublon, bougie incohérente, série non triée, calendrier du week-end, flux en retard en semaine et normal le samedi, pause quotidienne, bougies figées, série vide, base contrat à terme / spot, écart systématique, bougies présentes dans une seule source, horaires décalés), parcours de l'interface (aucun appel sans clic, 4 lignes, concordance, panne OANDA signalée, historique), parcours des lots R1 et R2 et anciens parcours réussis, typage strict sans erreur.

---

## 19. Lot R4 — prix d'achat et de vente OANDA réels dans les simulations du Labo V12 — mis en ligne le 16/10/2026

Réponse à la rubrique 6 du registre d'évolution (intégrer bid / ask et spread dans les simulations).

| Élément | Avant | Après |
|---|---|---|
| Prix OANDA récupérés | Prix milieu seulement | Prix d'achat et de vente de chaque bougie M5 ; le labo en tire le prix milieu exact et le spread réel à l'ouverture, au plus haut, au plus bas et à la clôture |
| Spread dans le backtest | Constant, estimé dans Coûts & contrat | Avec des données OANDA : spread réel bougie par bougie. Entrée à l'ask (achat) ou au bid (vente) de l'ouverture ; stops, objectifs, point mort et stop suiveur contrôlés sur le bid (achat) ou l'ask (vente) ; sortie au temps sur le bid ou l'ask de clôture |
| Filtre « spread max » | Comparé au spread constant | Comparé au spread réel de chaque entrée : une entrée pendant un spread trop large est refusée |
| Source OANDA dans le labo principal | Absente (seulement Arène, Live, auto-évolution) | Bouton « OANDA (spot, achat / vente) » à côté de Yahoo, CSV et synthétique |
| Choix | — | « Spread appliqué » dans Coûts & contrat : réel des données (par défaut quand il existe) ou modélisé constant |
| Affichage | — | Spread moyen, à 95 %, maximum, et spread payé en moyenne à l'entrée : dans Coûts & contrat, l'onglet Agents, le rapport A–F et l'onglet Diagnostic |
| Onglet Live et auto-évolution | Prix milieu OANDA, spread constant | Spread réel OANDA appliqué au signal et aux cycles d'auto-évolution sur la source OANDA |

Ce qui ne change pas : avec Yahoo, un import CSV ou les données synthétiques (pas de prix d'achat et de vente séparés), le spread modélisé s'applique comme avant et les résultats sont identiques (vérifié sur les 8 agents, or et EUR/USD).

Vérifications : 22 tests dédiés (résultats inchangés sans spread réel ; spread réel constant égal au modélisé = mêmes trades et mêmes coûts ; entrée = milieu ± demi-spread ± glissement ; mode modélisé ; refus des entrées quand le spread réel dépasse le maximum ; alignement des spreads après tri ; agrégation H1 ; séries incomplètes écartées ; onglet Live ; route OANDA en prix d'achat et de vente avec bid et ask reconstitués exactement), parcours de l'interface (chargement OANDA, spread réel affiché puis mode modélisé), tous les tests et parcours précédents réussis. Coût de calcul : environ +10 % en spread modélisé et +29 % en spread réel par backtest, sur des durées de quelques millisecondes.

---

## 20. Lot R5 (caméra / analyse visuelle) — mis de côté le 16/10/2026

Décision du porteur : la caméra (rubrique 5 du registre d'évolution) est reportée à plus tard. Rien n'est développé ni déployé pour ce lot. Rappel du cadrage prévu pour sa reprise : image réduite et compressée dans le navigateur avant envoi, valeurs lues présentées dans un petit tableau corrigeable, analyse lancée seulement sur les valeurs confirmées, nombre de lectures par heure limité (coût en crédits à chaque lecture).

Lots restants : R6 (cellules de la matrice : position de chaque valeur par rapport au zéro central, labo éducatif) ; R5 à reprendre plus tard.

---

## 21. Lot R6 — cases de la matrice autour du zéro central (labo éducatif) — mis en ligne le 16/10/2026

Réponse à la rubrique 2 du registre d'évolution (« zéro au centre de chaque carré comme point de référence », valeurs qui se déplacent les unes par rapport aux autres).

| Élément | Comportement |
|---|---|
| Jauge dans chaque case | Le zéro au centre ; le point se place de −1 (à gauche : la devise de la ligne faiblit face à celle de la colonne) à +1 (à droite : elle se renforce) ; une barre relie le zéro au point (bleu au-dessus de zéro, rouge en dessous) |
| Mouvement | À chaque mise à jour de la force des devises (variation réelle sur 24 h), le point glisse vers sa nouvelle position ; un trait violet garde la position précédente et une flèche ▲▼ donne le sens du mouvement |
| Donnée manquante | Si une des deux devises n'a pas de force mesurée, la case affiche « n.d. » et une jauge hachurée, au lieu d'un faux « NEUTRE » à zéro |
| Lecture | Infobulle de chaque case (valeur, sens de lecture) et légende sous la matrice ; animation coupée si l'appareil demande moins de mouvements |

Coût : aucun appel serveur supplémentaire ; la jauge réutilise la force des devises déjà chargée.

Vérifications : 6 tests de rendu (zéro au centre et bornes, valeur positive et négative, trace de la position précédente, mouvement négligeable ignoré, donnée indisponible, sens de la flèche), typage strict sans erreur, points d'ancrage vérifiés uniques dans le code en ligne.

État du registre d'évolution : R1, R2, R3, R4 et R6 en ligne ; R5 (caméra) mis de côté.

---

## 22. Onglet Agents réorganisé (dispositions B et C) — mis en ligne le 16/10/2026

Demande : graphiques moins hauts mais pleine largeur, drawdown réduit, et tous les réglages serrés dans un petit tableau quadrillé juste sous les graphiques. Trois maquettes ont été comparées (grille complète type MetaTrader 5, onglets + grille, tiroir de réglage type cTrader) ; le porteur a retenu B et C.

| Élément | Avant | Après |
|---|---|---|
| Graphiques | Équité 220 px, titre « Drawdown » puis drawdown 110 px | Équité 150 px et drawdown 64 px collés dans un même cadre, même échelle de dates |
| Effet d'un changement | — | Courbe du test précédent en pointillé gris quand les réglages viennent de changer |
| Libellés des périodes | « Validation » et « Test final » se chevauchaient sur téléphone | Libellé complet s'il tient, sinon court (« Valid. », « Test », « Échauf. »), sinon aucun |
| Réglages (B) | En bas de la page, 6 grands blocs d'une colonne | Juste sous les graphiques : 6 onglets (Tendance 6, Pullback 3, Déclencheur 5, Filtres 15, Sorties 9, Risque 7) et un quadrillage serré (3 colonnes sur téléphone, plus sur ordinateur) ; point bleu sur l'onglet et la case modifiés ; onglet retenu sur l'appareil |
| Mode réglage (C) | — | Bouton « Mode réglage » : écran plein avec indicateurs (net, drawdown, trades, espérance et leur écart), graphiques compacts et courbe « avant le réglage » en pointillé en haut ; réglages pas à pas (− / +) dans un tiroir en bas ; test automatique ; « Garder ce réglage » ou « Annuler les changements » (retour aux réglages d'ouverture) |

Vérifications : 6 tests (libellés sans chevauchement sur la configuration de la capture, bandes larges, bande trop étroite, pas à pas : voisin, bornes, valeur hors liste) ; parcours de l'interface (ordre graphiques puis réglages, hauteurs 150 / 64 px, 6 onglets, point bleu, mode réglage : + sur le stop ATR 1,3 → 1,5, test automatique, écarts affichés, annulation qui remet 1,3, conservation qui garde 1,5) ; tous les parcours précédents réussis, typage strict sans erreur.

---

## 23. Lots R9 et R11 — archive hebdomadaire des barres et rapport de la semaine (Labo V12) — mis en ligne le 16/10/2026

### R9 — historique au-delà des 59 jours de Yahoo

Yahoo ne fournit qu'environ 59 jours de barres M5. Désormais, chaque samedi (marchés fermés), une tâche planifiée copie côté serveur les semaines terminées de chacun des 46 marchés suivis ; elles sont ensuite recollées devant les 59 jours récents.

| Élément | Comportement |
|---|---|
| Semaine archivée | Du samedi 00:00 au samedi suivant (heure UTC) : aucune séance n'est coupée en deux. Seules les semaines terminées et complètes sont copiées ; la première semaine de la fenêtre Yahoo (début manquant) est écartée |
| Prix stockés | Prix bruts de la source, sans raccord de contrat. Pour l'or (GC=F), les raccords d'échéance sont recalculés sur la série longue complète après collage, pour que l'ajustement reste cohérent d'un bout à l'autre |
| Écriture | Une semaine déjà archivée n'est jamais réécrite. 3 marchés par passage, un passage par heure le samedi de 04:20 à 23:20 (heure de Paris) ; un curseur reprend où le passage précédent s'est arrêté. Un marché en échec est noté et repris la semaine suivante (la fenêtre de 59 jours couvre encore la semaine manquée) |
| Premier samedi | Environ 8 semaines par marché (tout ce que contient la fenêtre de 59 jours), puis une nouvelle semaine chaque samedi |
| Nouvelle source « Yahoo long (archive) » | Bouton dans la barre des données : semaines archivées (jusqu'à 26) + 59 jours récents. Le libellé indique « Yahoo Finance + archive » et la note précise le nombre de semaines et la date de départ. Tant que l'archive est vide, la source le dit et ne charge que les 59 jours |
| Inchangé | La source « Yahoo » classique, la Chasse et l'auto-évolution restent sur 59 jours |

Ordre de grandeur : environ 120 Ko par semaine et par marché ; 26 semaines + 59 jours d'or ≈ 47 000 barres (≈ 2,8 Mo transférés au chargement).

### R11 — rapport hebdomadaire de l'auto-évolution

Nouvelle section « Rapport de la semaine » dans l'onglet Auto-évolution.

| Colonne / élément | Contenu |
|---|---|
| Semaine | Semaine en cours (calculée à la lecture) ou une des 12 semaines précédentes (figées chaque samedi matin) |
| Synthèse | Challengers testés, adoptions, propositions, retours arrière, confirmations ; nombre d'évolués devant ou derrière leur base en avant, et à l'essai |
| Par agent | Version au début et à la fin de la semaine (ex. « Base → v1 »), challengers testés, événements de la semaine, espérance en avant de l'évolué et de la base, bilan (« Trop tôt pour juger » sous 8 trades en avant, « Identique à la base », meilleur, à égalité, moins bon) |
| Honnêteté des comptes | Les challengers testés se comptent par différence avec la photo de la semaine précédente : « — » tant qu'aucune photo n'existe (le premier rapport figé, samedi 17/10, n'en aura pas). Si le journal d'un agent (12 derniers événements) est plein, les comptes sont marqués « ≥ » |

Vérifications : 37 tests serveur (découpage des semaines, collage trié sans doublon, curseur 3 marchés par passage, une seule lecture Yahoo par marché et par semaine, semaine jamais réécrite, marché en panne isolé, taille d'une semaine < 256 Ko, série longue identique à la série d'origine, raccord d'or antérieur aux 59 jours détecté et neutralisé, route réservée au propriétaire, comptes du rapport, photo figée une seule fois par semaine) ; parcours de l'interface (bouton Yahoo long, rapport en cours et figé) ; parcours précédents réussis ; typage strict sans erreur côté écran et côté serveur.

État du registre d'évolution : R1, R2, R3, R4, R6, R9 et R11 en ligne ; R5 (caméra) mis de côté ; R7, R8, R10 et R12 proposés.

---

## 24. Chantier 1 — santé du système, pause générale et contrôle de robustesse (Labo V12) — mis en ligne le 16/10/2026

Décision du porteur : options 1, 2 et 3 du chantier 1, sans notification sur téléphone. Codé et testé avant déploiement, déployé après accord explicite.

### Santé du système (onglet Diagnostic)

| Élément | Comportement |
|---|---|
| Suivi des tâches planifiées | Chasse, auto-évolution et archive enregistrent chaque passage : début, durée, succès ou échec, lectures de données réussies ou non |
| Statut affiché | OK, en retard (pas de passage à l'heure prévue, avec 20 min de marge), échec (erreur ou aucune donnée lue), en pause, en attente (jamais exécutée) |
| Alerte active | Bandeau en haut de l'écran dès qu'une tâche est en échec ou en retard, ou que la pause générale est active, avec un bouton vers le détail. Lecture toutes les minutes tant que la page est ouverte |
| Temps de réponse | Temps de réponse du serveur à la dernière lecture, durée de chaque tâche et durée maximale récente |

### Pause générale et coupe-circuit

| Élément | Comportement |
|---|---|
| Pause manuelle | Un bouton suspend la Chasse, l'auto-évolution et l'archive ; le lancement manuel d'un cycle ou de la Chasse est refusé pendant la pause. Aucun paramètre n'est modifié |
| Déclenchement automatique (mode sûr) | 3 échecs d'exécution de suite d'une tâche ; 4 passages de suite sans aucune donnée lue (1 heure pour une tâche de 15 minutes) ; 4 retours arrière de l'auto-évolution en 24 heures |
| Reprise | Uniquement manuelle ; les compteurs repartent de zéro, et les retours arrière antérieurs à la reprise ne comptent plus |
| Traçabilité | Historique des 20 dernières pauses et reprises (manuelle ou automatique, raison) |
| Exécution future | Le labo n'envoie aucun ordre ; un futur pont d'exécution devra lire ce même interrupteur avant tout ordre |

### Contrôle de robustesse (discipline anti-surapprentissage)

Quatre contrôles, mesurés sur recherche + validation (le test final masqué n'est jamais utilisé) :

| Contrôle | Seuil pour passer |
|---|---|
| Walk-forward : le choix parmi les configurations, refait sur le passé, tient sur la période suivante | Verdict « stable » (au moins 3 fenêtres sur 4 positives, espérance hors échantillon > 0, au moins 20 trades) |
| Réglages voisins : un cran de part et d'autre sur les EMA H1 / M15 / M5, le stop ATR et le R:R | Au moins 75 % des voisins gardent une espérance > 0 et au moins la moitié de celle du candidat |
| Probabilité de sur-ajustement (PBO, méthode CSCV, 8 blocs de temps, 70 découpages) | Au plus 50 % |
| Sharpe dégonflé du nombre d'essais (asymétrie et queues épaisses comprises) | Au moins 95 % de confiance, avec au moins 20 trades |

- **StrategyTune** : bouton « Robustesse » sur chaque ligne ; une variante n'est « validée (robuste) » que si les quatre contrôles passent. La conclusion apparaît aussi dans la confirmation avant « Appliquer », et chaque contrôle est inscrit au journal.
- **Auto-évolution** : contrôle du champion une fois par version et par jour (16 backtests de voisins environ) ; le Sharpe dégonflé tient compte de tous les challengers testés depuis le début. « Validé » = confirmé en avant (20 trades) **et** robuste. Étiquette seulement : adoption et retour arrière inchangés. Le rapport de la semaine compte les agents validés.
- Choix assumé : PBO **et** Sharpe dégonflé sont tous deux exigés (plus strict que « l'un ou l'autre »). Avec 59 jours de données, peu de candidats passeront au début ; l'archive R9 allongera l'historique.

Vérifications : 42 tests serveur (loi normale, voisins, PBO sur du bruit, sur une configuration dominante et sur un choix qui ne tient pas, Sharpe dégonflé selon le nombre d'essais, test final jamais utilisé, statuts des tâches dont les créneaux du samedi, chaque déclenchement du coupe-circuit et la reprise, routes réservées au propriétaire, refus des lancements pendant la pause, robustesse du champion évolué mesurée sans changer ses paramètres) ; 37 tests R9 inchangés ; parcours de l'interface (bandeau, pause, reprise, bouton Robustesse, étiquette « validé », rapport) ; parcours précédents réussis ; typage strict sans erreur. Tests sur données synthétiques : aucun résultat de marché n'est annoncé.

État du chantier 1 : observabilité minimale, coupe-circuit et discipline walk-forward en ligne dans le labo. Reste hors du labo : le coupe-circuit côté MT5 (script Python, à vérifier sur le poste du porteur).

---

## 25. Décisions du porteur — socle d'entreprise et « l'Œil » — 16/10/2026

| Sujet | Décision |
|---|---|
| Ordre des travaux | D'abord le socle risque (profil de risque central séparé des agents, numéros de version), puis « l'Œil » |
| L'Œil | Premier agent de la chaîne : il voit tout le marché, croise toutes les données et propose toujours « le contre » (qui est fort contre qui est faible : position d'achat, position de vente, position croisée), ainsi que les plus hauts et plus bas, les informations et les positions des grands portefeuilles (rapport COT) |
| Grilles de l'Œil | Forex (8 devises, 28 paires) · Symboles (pétrole, indices, agricoles) · Or et métaux, à part car l'or est le marché prioritaire. Grille crypto prévue mais reportée |
| Crypto | Reportée : reste exclue de la version actuelle, conformément au prompt maître |
| Investisseurs tiers | Pas maintenant. La structure nécessaire est préparée dès la conception (séparation des comptes, rapports, traçabilité), mais rien n'est ouvert sans agrément réglementaire (gestion pour compte de tiers) ni sans avis juridique. Aucune promesse de gain |
| Rentabilité | Aucune stratégie n'est déclarée ni passée en réel sans rentabilité nette mesurée hors échantillon puis sur des barres nouvelles ; le système refuse lui-même ce qui ne l'est pas. Aucun résultat n'est garanti |

**Concept de la toile (précision du porteur) :** chaque petit carré de la toile est un marché ou une paire, avec son centre = le zéro. Chaque araignée est une source de données (prix et force relative, positions des institutions, calendrier, plus hauts et plus bas…) qui se déplace sur la toile ; sa position par rapport au centre dit qui est fort ou faible. Les positions se choisissent en croisant toutes les araignées, avec les données de marché en premier.

---

## 26. Socle risque — profil de risque central et numéros de version (Labo V12, version 12.35.0) — mis en ligne le 16/10/2026

Réponse au point 8 du registre v13 (séparation des rôles : le moteur de risque ne doit pas pouvoir être configuré ou contourné par l'agent qui génère le signal) et au point 11 (versionnage et journal des versions séparé).

| Élément | Comportement |
|---|---|
| Constat de départ | Les limites de risque étaient rangées dans les réglages de chaque agent : rien n'empêchait, dans la structure, qu'une évolution de l'agent les desserre |
| Profil de risque central | Plafonds communs : risque max par trade, perte max par jour, pertes de suite max, trades max par jour, arrêt imposé au drawdown, pause minimale après perte |
| Où il s'applique | Dans le moteur de backtest lui-même, à chaque calcul : labo, StrategyTune, auto-évolution, Chasse, Arène, Live, multi-marchés, comparaison des sources |
| Agents | Un agent peut être plus prudent que le profil, jamais moins ; une valeur plus risquée est ramenée au plafond et le résultat l'indique |
| Réglage | Par le propriétaire seul (onglet Diagnostic, route protégée), avec confirmation ; chaque changement est numéroté et gardé en historique ; valeurs limitées aux listes proposées |
| Sécurité par défaut | Profil illisible ou invalide : plafonds d'origine, jamais plus larges |
| Valeurs de départ | 0,5 % par trade, 1 % par jour, 4 pertes de suite, 5 trades par jour, pas d'arrêt imposé au drawdown, pas de pause minimale : les valeurs les plus larges des 8 agents, donc aucun résultat ne change |
| Versions | Numéro 12.35.0 affiché dans l'en-tête et renvoyé par la santé du système ; journal des versions publiées : [`CHANGELOG.md`](CHANGELOG.md) |

Vérifications : 8 agents × or et EUR/USD, trades identiques à la version précédente avec les plafonds d'origine ; 21 tests (plafonds appliqués : 2 → 1 trade par jour, lots 0,10 → 0,06 avec 0,25 % de risque ; arrêt au drawdown imposé ; agent plus prudent conservé ; réglage d'agent desserré ramené au plafond ; valeurs hors liste refusées ; versions et historique ; routes réservées au propriétaire ; comparaison des sources et auto-évolution appliquant le profil côté serveur) ; 37 tests R9 et 42 tests du chantier 1 inchangés ; parcours de l'interface (réglage du profil, avis « Profil de risque appliqué » sur le résultat) ; typage strict sans erreur. Tests sur données synthétiques.

Mise à jour du point 12 du registre v13 : la limite « 125/125 » n'est plus d'actualité ; les déploiements passent. La limite connue de la plateforme AppDeploy est un plafond de crédits par jour (UTC).

Prochaine étape décidée : « l'Œil », phase 1 (grilles Forex, Symboles, Or et métaux ; fort contre faible ; le contre ; plus hauts et plus bas).

---

## 27. Chantier 2, étape 1 — outils de contrôle du robot MT5 sans ordre — publiés le 16/10/2026

Décision du porteur : vérifier le robot `spider_v12_mt5.py` avant tout ordre, même en démo ; aucune modification du robot ni aucun ordre sans accord explicite. Le robot reste sur le poste du porteur et n'entre jamais dans le dépôt public (`.gitignore` : robot, `.env`, journaux, fichiers d'arrêt, rapport de contrôle).

Constat : le robot n'est pas accessible depuis la session de travail (conteneur distant, sans accès au PC). Des outils de contrôle ont donc été écrits pour être lancés sur le poste, dans [`outils/mt5`](../outils/mt5/LISEZMOI.md).

| Outil | Rôle |
|---|---|
| `audit_statique.py` | Lit le robot sans l'exécuter. Dit si la commande `check` peut atteindre `order_send`, `Buy`, `Sell` ou `Close` (avec le chemin d'appel), et donne les indices sur : démo / réel, arrêt d'urgence par fichier (au démarrage, dans la boucle, action), les 11 limites de référence, les doublons d'ordre (magic, commentaire, lecture des positions avant envoi, envoi dans une boucle), les secrets (valeur jamais affichée) |
| `check_sans_ordre.py` | Lance `check` avec `order_send`, `Buy`, `Sell` et `Close` neutralisés : chaque tentative est bloquée et comptée. Compte, serveur, titulaire et secrets lus dans l'environnement sont masqués dans la sortie |
| `controle_complet.py` | Les deux à la suite. `check` n'est **pas lancé** si l'audit trouve un ordre atteignable depuis `check` ou ne trouve pas la commande `check`. Rapport dans `rapport_controle.txt`, prêt à coller |

Limites de référence contrôlées : risque 0,25 % par trade (décision C1, confirmée par le porteur le 16/10/2026), R:R 1,50, perte journalière max 1 %, 2 trades par jour, 3 pertes consécutives max, lot max 0,10, stop ATR × 1,30, break-even à 1 R + 2 points, spread max 20 points, déviation 10.

Vérifications : 11 tests sous Linux avec un faux module MetaTrader5 et quatre robots fictifs (conforme, fautif, secret en clair, sans commande `check`) : chemins d'appel trouvés, secrets jamais affichés, toutes les tentatives d'ordre bloquées (un fichier témoin prouve qu'aucune n'a traversé), `check` non lancé quand l'audit l'interdit, compte et mot de passe masqués. **Pas encore testé** sur le vrai robot, ni sous Windows, ni avec Python 3.14, ni avec un terminal MT5.

Décision du porteur (16/10/2026) : le robot MT5 applique **0,25 % de risque par trade**, en démo comme en réel, conformément à C1 (0,50 % reste le plafond absolu et la valeur de la recherche V12). L'audit compare désormais le robot à 0,25 %. Le robot lui-même n'est pas modifié : si sa valeur diffère, la correction sera proposée et soumise à accord.

Prochaine étape : le porteur lance `controle_complet.py` sur son poste et transmet le rapport ; rapport A–F sur le vrai robot, puis propositions de modification soumises à accord.

---

## 28. Conformité — tableau du Hub confronté au code du Labo V12 (lecture seule) — 16/10/2026

Vérification faite en lisant le code source déployé du Labo V12 (version du 16/10/2026), sans rien modifier ni redéployer. Elle porte sur les trois lignes affichées « ACTIF ». Ce constat technique n'est pas un avis juridique.

| Ligne du Hub | Affiché | Constat dans le code | Verdict |
|---|---|---|---|
| Sécurité opérationnelle | ACTIF | Aucun secret côté navigateur ; jeton OANDA lu dans les secrets du serveur et jamais renvoyé dans les messages d'erreur ; seul l'hôte OANDA **Practice** est appelé, aucune route d'ordre, de trade ou de position vers le courtier ; routes sensibles réservées au propriétaire (connexion + liste blanche) | **Confirmé** |
| MAR — abus de marché | ACTIF | Journal d'audit : une fiche par signal ou signal bloqué, identifiant unique (marché, source, agent, bougie, état), doublons refusés par le serveur, jamais modifiée ni supprimée ; chaque fiche dit « aucun ordre envoyé ; validation humaine requise » | **Confirmé** |
| RGPD / CNIL | ACTIF | Journal des essais et d'audit sans pièce d'identité, clé ni secret : confirmé. Mais : (1) la liste d'attente garde l'e-mail, l'identifiant et une note libre (300 caractères) **sans durée de conservation** ; (2) **aucune route** pour qu'un utilisateur consulte, exporte ou efface ses données ; (3) **aucune notice de confidentialité** dans l'application ; (4) l'e-mail est transmis à Stripe au paiement (sous-traitant à déclarer) | **Partiel** : minimisation et sécurité oui ; transparence, droits et conservation limitée non implémentés |

Précision sur MiFID II (à faire confirmer par un juriste) : le verrou vise les services rendus à des tiers (conseil, gestion, transmission d'ordres, signaux). Un robot qui passe des ordres sur le compte du porteur, chez un courtier agréé, ne relève pas de ce verrou ; c'est la règle interne « démo d'abord, réel sur accord explicite » qui s'applique (chantier 2).

Propositions soumises au porteur (rien n'est codé ni déployé sans accord) :

| # | Proposition | Bénéfice | Risque |
|---|---|---|---|
| P1 | Afficher « RGPD : PARTIEL » dans le Hub tant que P2 à P4 ne sont pas faits | Tableau fidèle au code | Aucun |
| P2 | Notice de confidentialité : responsable, finalités, données (e-mail, identifiant, note, journaux), durées, sous-traitants (hébergeur, Stripe), droits, contact, réclamation CNIL | Transparence (articles 12 à 14) | Texte à faire relire |
| P3 | « Mes données » : consulter, exporter (JSON) et effacer ses données (liste d'attente, essais, jeux de réglages) | Droits d'accès, de portabilité et d'effacement | Effacement irréversible : confirmation demandée |
| P4 | Durées de conservation : liste d'attente purgée 12 mois après l'inscription par la tâche planifiée ; journal d'audit conservé 5 ans puis purgé (durée à choisir par le porteur) | Conservation limitée | Une purge mal réglée efface trop : tests sur données fictives |
| P5 | Ajouter au Hub une ligne « Robot MT5 (poste du porteur) : CONDITIONNEL — démo uniquement, contrôles du chantier 2 » | Le robot, hors labo, apparaît dans la conformité | Aucun |
