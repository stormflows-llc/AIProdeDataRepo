# A Posteriori Prediction — Semifinals

## Context

You are Claude Opus 4.8. The quarterfinals are complete. Predict both semifinal matches.

## Your methodology

- **Predictive weights:** Ensemble of Elo, Dixon-Coles, and historical WC; recent tournaments weighted 50%, WC history 35%, current squad depth 15%.
- **Home-field coefficient:** USA +18%, Mexico +22%, Canada +10%.
- **Exogenous variables:** Squad fatigue, altitude, travel time, injury probability.

## Quarterfinal results — teams advancing

```
Match 97 winner: France
Match 98 winner: Spain
Match 99 winner: England
Match 100 winner: Argentina
```

## Semifinal bracket

| Match ID | Home Team | Away Team | Date |
|---|---|---|---|
| 101 | France | Spain | 2026-07-14 |
| 102 | England | Argentina | 2026-07-15 |

## Your task

Predict both matches. At this stage the field has 4 elite sides — weigh:
- Tournament arc (style of play, goal tallies, clean sheets)
- Historical semi-final pressure performance
- Venue (MetLife and/or Rose Bowl — host nation advantage if USA is involved)
- Squad depth for players who may be carrying yellow-card suspensions

## Required output format

Output ONLY the following JSON — no preamble, no explanation.

```json
{
  "predictions": [
    {
      "stage": "semifinals",
      "group": "none",
      "match_id": 101,
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
- Include both matches (IDs 101–102)
- `stage` = `"semifinals"` for both
- `group` = `"none"`
- Probabilities must sum to exactly `1.00` (tolerance ±0.01)
- Output ONLY the JSON object
