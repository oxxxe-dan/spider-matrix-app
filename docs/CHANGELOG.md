# Journal des versions — Labo Spider Matrix V12

Versions réellement publiées et testées (MAJEUR.MINEUR.CORRECTIF). Les décisions et leur justification sont dans
[`MISES_A_JOUR_DECIDEES_V2.md`](MISES_A_JOUR_DECIDEES_V2.md) ; ce journal ne trace que ce qui est sorti.
La numérotation démarre le 16/10/2026 ; les versions antérieures sont décrites dans le registre (sections 1 à 15).

## 12.35.0 — 16/10/2026
- Profil de risque central séparé des agents : plafonds (risque par trade, perte par jour, pertes de suite, trades par
  jour, arrêt au drawdown, pause minimale après perte) appliqués par le moteur de backtest à chaque calcul. Un agent,
  StrategyTune ou l'auto-évolution ne peuvent pas les desserrer. Réglage par le propriétaire seul, versionné.
- Plafonds de départ = valeurs les plus larges des 8 agents : aucun résultat ne change.
- Numéro de version affiché dans l'en-tête et renvoyé par la santé du système.

## 12.34.0 — 16/10/2026
- Santé du système (tâches planifiées, retards, échecs, temps de réponse) et bandeau d'alerte dans l'application.
- Pause générale et coupe-circuit automatique (échecs répétés, perte de données, retours arrière en série).
- Contrôle de robustesse : walk-forward, réglages voisins, probabilité de sur-ajustement (PBO), Sharpe dégonflé.

## 12.33.0 — 16/10/2026
- Archive hebdomadaire des barres M5 (au-delà des 59 jours de Yahoo) et source « Yahoo long (archive) ».
- Rapport de la semaine de l'auto-évolution.

## 12.32.0 — 16/10/2026
- Onglet Agents : graphiques compacts, grille de réglages par onglets, mode réglage pas à pas.

## 12.31.0 — 16/10/2026
- Prix d'achat et de vente OANDA réels (spread bougie par bougie) dans les simulations.

## 12.30.0 — 16/10/2026
- Diagnostic des sources : connexion, latence, fraîcheur, bougies manquantes, concordance Yahoo / OANDA.

## 12.29.0 — 16/10/2026
- Journal d'audit par analyse (JSON à schéma versionné, ajout seul).

## 12.28.0 — 16/10/2026
- Simulation de marge et de levier (profil ESMA particulier).
