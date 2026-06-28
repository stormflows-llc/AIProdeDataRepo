# A Posteriori Prediction — Round of 32

## Context

You are Claude Opus 4.8. Before the 2026 FIFA World Cup began, you predicted all 104 matches using your
ensemble methodology. The group stage is now complete (all 72 matches played). This is your first a
posteriori prediction session: you now know the exact 32 qualifiers and their full group stage form.

Apply your full methodology with this real-world knowledge to predict all 16 Round of 32 matches.

## Your methodology

- **Predictive weights:** Ensemble of Elo, Dixon-Coles, and historical WC; recent tournaments weighted 50%, WC history 35%, current squad depth 15%.
- **Home-field coefficient:** USA +18% (massive home crowd factor), Mexico +22% (Azteca effect), Canada +10%.
- **Exogenous variables:** Full model — squad fatigue (club season minutes), altitude (Mexico City), travel time, and injury probability.

## How 32 teams qualified

The 2026 FIFA World Cup has 12 groups of 4. From each group:
- **1st place** (12 teams) and **2nd place** (12 teams) automatically advance = 24 teams.
- The **8 best 3rd-place teams** (out of 12) also advance = 8 more teams.
- **3rd-place ranking criteria** (in order): Points → Goal difference → Goals scored → Disciplinary record.

### All 32 qualified teams

**Group winners (12):**
| Group | 1st | Pts | GD |
|---|---|---|---|
| A | Mexico | 9 | +6 |
| B | Switzerland | 7 | +4 |
| C | Brazil | 7 | +6 |
| D | United States | 6 | +4 |
| E | Germany | 6 | +6 |
| F | Netherlands | 7 | +6 |
| G | Belgium | 5 | +4 |
| H | Spain | 7 | +5 |
| I | France | 9 | +8 |
| J | Argentina | 9 | +7 |
| K | Colombia | 7 | +3 |
| L | England | 7 | +4 |

**Group runners-up (12):**
| Group | 2nd | Pts | GD |
|---|---|---|---|
| A | South Africa | 4 | -1 |
| B | Canada | 4 | +5 |
| C | Morocco | 7 | +3 |
| D | Australia | 4 | 0 |
| E | Ivory Coast | 6 | +2 |
| F | Japan | 5 | +4 |
| G | Egypt | 5 | +2 |
| H | Cape Verde | 3 | 0 |
| I | Norway | 6 | +1 |
| J | Austria | 4 | 0 |
| K | Portugal | 5 | +5 |
| L | Croatia | 6 | 0 |

**Best 8 third-place teams (ranked):**
| Rank | Group | Team | Pts | GD | GF |
|---|---|---|---|---|---|
| 1 | K | DR Congo | 4 | +1 | 4 |
| 2 | F | Sweden | 4 | 0 | 7 |
| 3 | E | Ecuador | 4 | 0 | 2 |
| 4 | L | Ghana | 4 | 0 | 2 |
| 5 | B | Bosnia and Herzegovina | 4 | -1 | 5 |
| 6 | J | Algeria | 4 | -2 | 5 |
| 7 | D | Paraguay | 4 | -2 | 2 |
| 8 | I | Senegal | 3 | +2 | 8 |

**Eliminated 3rd-place teams (did not qualify):** Iran (G3, 3pts GD0), South Korea (A3, 3pts GD-1), Scotland (C3, 3pts GD-3), Uruguay (H3, 2pts).

## Round of 32 bracket — actual matchups

All 16 matches confirmed. These are the actual fixtures:

| Match ID | Home Team | Away Team | Date | Venue |
|---|---|---|---|---|
| 73 | South Africa | Canada | 2026-06-28 | Gillette Stadium, Boston |
| 74 | Brazil | Japan | 2026-06-29 | Allegiant Stadium, Las Vegas |
| 75 | Germany | Paraguay | 2026-06-29 | Estadio Akron, Guadalajara |
| 76 | Netherlands | Morocco | 2026-06-29 | MetLife Stadium, East Rutherford |
| 77 | Ivory Coast | Norway | 2026-06-30 | AT&T Stadium, Dallas |
| 78 | France | Sweden | 2026-06-30 | SoFi Stadium, Los Angeles |
| 79 | Mexico | Ecuador | 2026-06-30 | Estadio Azteca, Mexico City |
| 80 | England | DR Congo | 2026-07-01 | Levi's Stadium, San Jose |
| 81 | Belgium | Senegal | 2026-07-01 | Arrowhead Stadium, Kansas City |
| 82 | United States | Bosnia and Herzegovina | 2026-07-01 | BC Place, Vancouver |
| 83 | Spain | Austria | 2026-07-02 | BMO Field, Toronto |
| 84 | Switzerland | Algeria | 2026-07-02 | Lincoln Financial Field, Philadelphia |
| 85 | Portugal | Croatia | 2026-07-02 | Estadio BBVA, Monterrey |
| 86 | Australia | Egypt | 2026-07-03 | Lumen Field, Seattle |
| 87 | Argentina | Cape Verde | 2026-07-03 | Hard Rock Stadium, Miami |
| 88 | Colombia | Ghana | 2026-07-03 | Gillette Stadium, Boston |

## Your task

Predict all 16 matches. Factor in:
- Each team's group stage form — goals scored/conceded, defensive solidity, margin of victories
- Which teams peaked vs. coasted through a weak group
- Squad fatigue (some teams played 3 hard matches; others cruised)
- Travel distances to each venue (especially for European teams flying to US/Mexico/Canada)
- Venue altitude/crowd advantage (Azteca for Mexico, US venues for USA)
- Any known injuries or suspensions after the group stage
- 3rd-place qualifiers may carry momentum from a tense late qualification

## Required output format

Output ONLY the following JSON — no preamble, no explanation. The output will be merged into
`data/aposteriori/claude-opus-4-8.json` (the `predictions` array) in the AIProde repository.

**Note:** Do NOT include team names, stage, or group — those come from `data/tournament.json`. Only provide prediction-specific fields.

```json
{
  "predictions": [
    {
      "match_id": 73,
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
- Include all 16 matches (IDs 73–88) in the order shown above
- `extra_time_or_penalties_winner`: exact team name from the bracket table if match goes to ET/penalties, otherwise `"none"`
- Probabilities must sum to exactly `1.00` (tolerance ±0.01)
- `model_confidence`: `"high"`, `"medium"`, or `"low"`
- Output ONLY the JSON object, starting with `{` and ending with `}`
