# A Posteriori Prediction — Round of 16 (follow-up: match 95)

## Context

You are Claude Opus 4.8. You have already predicted the Round of 32 a posteriori (with knowledge of
actual group stage qualifiers), and you have already predicted 6 of the 8 Round of 16 matches
(89–94) in an earlier prompt — those are already recorded. Round of 32 match 87 (Argentina vs Cape
Verde) has now been played, which resolves Round of 16 match 95. Apply your methodology to predict
this one additional match.

Match 96 (Switzerland vs winner of Colombia-Ghana) is still pending — Round of 32 match 88 has not
been played yet. Do not predict match 96 in this prompt.

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
Match 88 winner: PENDING — Colombia vs Ghana not yet played
```

## Round of 16 bracket

7 of the 8 matches are now fully determined. Match 96 still has one confirmed team and one pending
(Round of 32 match 88 has not been played yet).

| Match ID | Home Team | Away Team | Date | Status |
|---|---|---|---|---|
| 89 | Paraguay | France | 2026-07-04 | already predicted |
| 90 | Canada | Morocco | 2026-07-04 | already predicted |
| 91 | Brazil | Norway | 2026-07-05 | already predicted |
| 92 | Mexico | England | 2026-07-05 | already predicted |
| 93 | Spain | Portugal | 2026-07-06 | already predicted |
| 94 | Belgium | United States | 2026-07-06 | already predicted |
| 95 | Egypt | Argentina | 2026-07-07 | **predict now** |
| 96 | Switzerland | TBD (winner of Colombia vs Ghana) | 2026-07-07 | pending |

## IMPORTANT — partial run

Match 88 (Round of 32, Colombia vs Ghana) has not been played yet, so the away team for match 96 is
unknown. **Do not guess a team or invent an opponent for match 96.**

- Predict only match **95** (Egypt vs Argentina). Matches 89–94 are already recorded — do not
  re-predict them.
- Do NOT include match_id 96 in the output.
- Once match 88 is played, a follow-up prompt will be sent with the resolved match 96 matchup.

## Your task

Predict match 95. Factor in:
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
    }
  ]
}
```

**Rules:**
- Include only match_id 95. Do NOT include 89–94 (already recorded) or 96 (opponent not yet
  determined — Round of 32 match 88 is still pending).
- `stage` = `"round_of_16"`
- `group` = `"none"`
- Probabilities must sum to exactly `1.00` (tolerance ±0.01)
- `model_confidence`: `"high"`, `"medium"`, or `"low"`
- Output ONLY the JSON object
