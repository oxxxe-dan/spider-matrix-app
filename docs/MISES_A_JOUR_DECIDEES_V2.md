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
| Arène live « 7 modes » | 🟡 | **6 modes** codés : Battle Royale, Tournoi, 1V1, Équipe, Domination, Arena. Le libellé « 7 modes » est inexact |
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

## 7. Décisions contradictoires à trancher

| # | Sujet | Valeurs en conflit | Recommandation |
|---|---|---|---|
| **C1** | Risque par trade | 0,25 % (V10, règles du labo éducatif) · 0,5 % (agents V12) · 1 % (agents de la Battle du labo éducatif) · 0,05 % (profil 100 €) | Fixer une valeur unique dans un registre d'agents partagé |
| **C2** | R:R de référence | 1,5 (robot MT5, agents V12, profil 100 €) · 2,0 (baseline V12, Battle du labo éducatif) | Trancher, puis l'écrire dans la Référence V12 |
| **C3** | Crypto | Exclue (V12, MiCA bloqué) · présente (BTC visuels, Binance, vision globale V10) | Exclure partout tant que MiCA est bloqué |
| **C4** | Broker démo / exécution | OANDA MT5 · Axi MT5 · IBKR (le Sentinel exige un « pont IBKR ») · Saxo (refusé) · cTrader | Choisir une seule cible démo pour la V3 |
| **C5** | Fuseau des sessions | Paris · heure serveur MT5 | Paris (déjà utilisé par le moteur) sauf si le robot MT5 doit être reproduit à l'identique |
| **C6** | Paramètres des agents | Deux registres différents (V12 vs labo éducatif) | Le registre V12 fait foi |

---

## 8. Ce qu'il reste à lancer pour boucler la V2

Dans l'ordre :
1. **Trancher C1 à C6** (aucun développement nécessaire, seulement des choix).
2. **Walk-forward dans le moteur V12** (dernier engagement V2 non tenu) — plan, Lot 2.4.
3. **Vérité des données du labo éducatif** : force des 8 devises, Spider Intelligence Score et Battle calculés sur données réelles, ou marqués fictifs — plan, Lot 1.
4. **Risk Engine global** (risque total 1 %, 3 positions max, DD jour 2 %, DD total 10 %, kill switch) — décision V10 + dossier S2.
5. **Libellés exacts** : « 6 modes », statut des brokers (Saxo refusé), retrait du « LIVE-READY ».
6. **Dossier de présentation ACPR** (demandé le 18/09) puis démarche AMF.
7. Fournir les éléments « En attente de ta part » (robot .mq5, exports MT5) pour préparer la V3.
