# A Posteriori Prediction — Quarterfinals

## Context

You are Claude Opus 4.8. You have predicted the Round of 32 and Round of 16 a posteriori. The Round
of 16 is now complete. Predict all 4 quarterfinal matches.

## Your methodology

- **Predictive weights:** Ensemble of Elo, Dixon-Coles, and historical WC; recent tournaments weighted 50%, WC history 35%, current squad depth 15%.
- **Home-field coefficient:** USA +18%, Mexico +22%, Canada +10%.
- **Exogenous variables:** Squad fatigue, altitude, travel time, injury probability.

## Round of 16 results — teams advancing

```
Match 89 winner: France
Match 90 winner: Morocco
Match 91 winner: Norway
Match 92 winner: England
Match 93 winner: Spain
Match 94 winner: Belgium
Match 95 winner: Argentina
Match 96 winner: Switzerland
```

## Quarterfinal bracket

| Match ID | Home Team | Away Team | Date |
|---|---|---|---|
| 97 | France | Morocco | 2026-07-09 |
| 98 | Spain | Belgium | 2026-07-10 |
| 99 | Norway | England | 2026-07-11 |
| 100 | Argentina | Switzerland | 2026-07-11 |

## Your task

Predict all 4 matches. At this stage factor in heavily:
- Big-game experience and historical QF records
- Which teams have been peaking vs. accumulating fatigue
- Key player availability (suspension/injury after 4+ matches)
- Tactical matchup dynamics (pressing, counterattack, set pieces)

## Required output format

Output ONLY the following JSON — no preamble, no explanation.

```json
{
  "predictions": [
    {
      "stage": "quarterfinals",
      "group": "none",
      "match_id": 97,
      "home_team": "ACTUAL_HOME_TEAM",
      "away_team": "ACTUAL_AWAY_TEAM",
      "predicted_home_score": 0,
      "predicted_away_score": 0,
      "extra_time_or_penalties_winner": "none",
      "home_win_probability": 0.00,
      "draw_probability": 0.00,
      "away_win_probability": 0.00,
      "model_confidence": "high"
    }
  ]
}
```

**Rules:**
- Include all 4 matches (IDs 97–100)
- `home_team`/`away_team` must exactly match the Quarterfinal bracket table above — do not swap or reorder them
- `stage` = `"quarterfinals"` for all
- `group` = `"none"` for all knockout matches
- Probabilities must sum to exactly `1.00` (tolerance ±0.01)
- `model_confidence`: `"high"`, `"medium"`, or `"low"`
- Output ONLY the JSON object
