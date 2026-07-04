# A Posteriori Prediction — Round of 16 (follow-up: matches 95 and 96)

## Context

You are Claude Opus 4.8. You have already predicted the Round of 32 a posteriori (with knowledge of
actual group stage qualifiers), and you have already predicted 6 of the 8 Round of 16 matches
(89–94) in an earlier prompt — those are already recorded. Round of 32 matches 87 (Argentina vs Cape
Verde) and 88 (Colombia vs Ghana) have now both been played, which resolves the remaining two Round
of 16 matches: 95 and 96. Apply your methodology to predict these two additional matches.

The full Round of 16 bracket is now determined — this is the last follow-up needed for this round.

## Your methodology

- **Predictive weights:** Ensemble of Elo, Dixon-Coles, and historical WC; recent tournaments weighted 50%, WC history 35%, current squad depth 15%.
- **Home-field coefficient:** USA +18%, Mexico +22%, Canada +10%.
- **Exogenous variables:** Squad fatigue, altitude, travel time, injury probability.

## Round of 32 results — teams advancing

```
Match 73 winner: Canada
Match 74 winner: Brazil
Match 75 winner: Paraguay
Match 76 winner: Morocco
Match 77 winner: Norway
Match 78 winner: France
Match 79 winner: Mexico
Match 80 winner: England
Match 81 winner: Belgium
Match 82 winner: United States
Match 83 winner: Spain
Match 84 winner: Switzerland
Match 85 winner: Portugal
Match 86 winner: Egypt
Match 87 winner: Argentina
Match 88 winner: Colombia
```

## Round of 16 bracket

All 8 matches are now fully determined.

| Match ID | Home Team | Away Team | Date | Status |
|---|---|---|---|---|
| 89 | Paraguay | France | 2026-07-04 | already predicted |
| 90 | Canada | Morocco | 2026-07-04 | already predicted |
| 91 | Brazil | Norway | 2026-07-05 | already predicted |
| 92 | Mexico | England | 2026-07-05 | already predicted |
| 93 | Spain | Portugal | 2026-07-06 | already predicted |
| 94 | Belgium | United States | 2026-07-06 | already predicted |
| 95 | Egypt | Argentina | 2026-07-07 | **predict now** |
| 96 | Switzerland | Colombia | 2026-07-07 | **predict now** |

## IMPORTANT

- Predict only matches **95** (Egypt vs Argentina) and **96** (Switzerland vs Colombia). Matches
  89–94 are already recorded — do not re-predict them.

## Your task

Predict matches 95 and 96. Factor in:
- Round of 32 performance (margin of victory, penalty shootouts, fatigue)
- Cumulative squad fatigue and any new injuries/suspensions
- Momentum — which teams look sharp vs. which survived on luck
- Venue and travel considerations

## Required output format

Output ONLY the following JSON — no preamble, no explanation. The output will be appended to the
`predictions` array in `data/aposteriori/claude-opus-4-8.json`.

```json
{
  "predictions": [
    {
      "stage": "round_of_16",
      "group": "none",
      "match_id": 95,
      "home_team": "Egypt",
      "away_team": "Argentina",
      "predicted_home_score": 0,
      "predicted_away_score": 0,
      "extra_time_or_penalties_winner": "none",
      "home_win_probability": 0.00,
      "draw_probability": 0.00,
      "away_win_probability": 0.00,
      "model_confidence": "high"
    },
    {
      "stage": "round_of_16",
      "group": "none",
      "match_id": 96,
      "home_team": "Switzerland",
      "away_team": "Colombia",
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
- Include only match_ids 95 and 96. Do NOT include 89–94 — already recorded.
- `stage` = `"round_of_16"` for both
- `group` = `"none"` for both
- Probabilities must sum to exactly `1.00` (tolerance ±0.01)
- `model_confidence`: `"high"`, `"medium"`, or `"low"`
- Output ONLY the JSON object
