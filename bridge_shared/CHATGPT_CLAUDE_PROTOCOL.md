# Spider Matrix — ChatGPT / Claude shared protocol

## Project constraints
1. Spider Matrix V12 is the protected reference version.
2. No deployment, app update, parameter change, broker action, or live order is permitted through this bridge.
3. Research and test results are proposals until explicitly reviewed.
4. Keep StrategyTune research/backtesting separate from V12 orchestration and live parameters.
5. Never store API keys, account secrets, or personal data in GitHub notes or research reports.

## Roles
- ChatGPT: requirements, research synthesis, review of evidence, acceptance criteria.
- Claude: independent analysis, code review, implementation proposals and test design.
- GitHub: versioned shared source of truth for approved project documents and code.
- StrategyTune: research/backtesting laboratory. Reports must include instrument, timeframe, date range, script/version, inputs, account currency, warnings, metrics and run ID when available.
- Spider Jarvis Alpha: intended decision agent inside the product; it is not implemented or controlled by this bridge.
- Spider Sentinel / Risk Engine: independent security and risk gates; they must not be bypassed.

## Handoff format
Each assistant should submit a note containing:
- title
- summary and hypothesis
- evidence / report references
- test method and date range
- limitations and warnings
- proposed next step
- confidence: unverified, hypothesis, tested, or validated

## Validation states
- unverified: idea only
- hypothesis: testable claim, not yet tested
- tested: a reproducible test was run; attach the report
- validated: independently reviewed against agreed criteria, including out-of-sample results where appropriate

## Conflict handling
If the assistants disagree, preserve both analyses and list the evidence needed to resolve the disagreement. Do not average contradictory claims or silently change the live strategy.

## StrategyTune handoff
StrategyTune has no direct external API configured in this scaffold. Use supported exports to JSON, then import the report into the bridge's report directory. Do not claim a backtest ran unless a real StrategyTune run ID and result are available.

## Minimum acceptance checks before any future proposal can be promoted
- No look-ahead or data leakage.
- Train/test or walk-forward separation.
- Net performance with realistic bid/ask and known fees/limitations.
- Drawdown and risk-of-ruin review.
- Results stable across multiple market regimes.
- No modification to existing V12 parameters without explicit, separate approval.
