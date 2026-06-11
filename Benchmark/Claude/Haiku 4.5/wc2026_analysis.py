import json
import math
from collections import defaultdict

# ============================================================================
# 2026 FIFA WORLD CUP PREDICTIVE MODEL
# AI Model: Claude (Anthropic) - Haiku 4.5
# Calibration: 70% Recent Form | 30% Historical | Moderate Home Advantage (1.12x) | Club Fatigue Included
# ============================================================================

# Team Strength Ratings (0-100 scale)
TEAM_RATINGS = {
    'Argentina': 89, 'Brazil': 91, 'France': 88, 'England': 85, 'Germany': 87, 'Spain': 86,
    'Belgium': 81, 'Netherlands': 84, 'Portugal': 82, 'Denmark': 79, 'Sweden': 75, 'Poland': 76,
    'Mexico': 74, 'USA': 73, 'Canada': 68, 'Uruguay': 80, 'Chile': 72, 'Colombia': 75,
    'Peru': 70, 'Ecuador': 68, 'Venezuela': 62, 'Paraguay': 66, 'Bolivia': 58, 'Costa Rica': 65,
    'Jamaica': 61, 'Guatemala': 56, 'New Zealand': 60, 'Australia': 71, 'Japan': 74, 'South Korea': 76,
    'Saudi Arabia': 62, 'Iran': 64, 'Iraq': 59, 'UAE': 63, 'Uzbekistan': 61, 'Thailand': 57,
    'Italy': 85, 'Croatia': 78, 'Serbia': 77, 'Romania': 71, 'Hungary': 68, 'Greece': 66,
    'Senegal': 72, 'Ghana': 68, 'Egypt': 70, 'Morocco': 79, 'Tunisia': 67, 'Cameroon': 65,
    'South Africa': 69, 'Iceland': 60, 'Botswana': 52, 'Bulgaria': 64, 'Norway': 70, 'Tajikistan': 55,
    'Bangladesh': 48
}

# Groups
GROUPS = {
    'A': ['Mexico', 'South Africa', 'Iceland', 'Botswana'],
    'B': ['Japan', 'Spain', 'Germany', 'Chile'],
    'C': ['Argentina', 'France', 'Morocco', 'Uzbekistan'],
    'D': ['Brazil', 'Belgium', 'Serbia', 'Canada'],
    'E': ['England', 'Portugal', 'Netherlands', 'Iran'],
    'F': ['Italy', 'Uruguay', 'Bulgaria', 'Ecuador'],
    'G': ['Denmark', 'Sweden', 'Australia', 'Tunisia'],
    'H': ['Croatia', 'Poland', 'Romania', 'Peru'],
    'I': ['South Korea', 'Hungary', 'Greece', 'Paraguay'],
    'J': ['Egypt', 'Ghana', 'Costa Rica', 'New Zealand'],
    'K': ['Cameroon', 'Venezuela', 'Guatemala', 'Jamaica'],
    'L': ['Senegal', 'Norway', 'Colombia', 'Saudi Arabia']
}

HOST_ADJUSTMENT = {
    'USA': 1.12,
    'Mexico': 1.12,
    'Canada': 1.12
}

FATIGUE_MULTIPLIER = {
    'France': 0.96, 'Spain': 0.96, 'England': 0.95, 'Germany': 0.96,
    'Argentina': 0.94, 'Brazil': 0.95, 'Uruguay': 0.93, 'Belgium': 0.94,
    'Netherlands': 0.95, 'Portugal': 0.94
}

def poisson_probability(lambda_param, k):
    """Poisson probability mass function"""
    if lambda_param == 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lambda_param) * (lambda_param ** k)) / math.factorial(k)

def predict_match(home_team, away_team, group_id):
    """Predict match using Poisson distribution"""
    home_strength = TEAM_RATINGS.get(home_team, 60)
    away_strength = TEAM_RATINGS.get(away_team, 60)
    
    if home_team in HOST_ADJUSTMENT:
        home_strength = home_strength * HOST_ADJUSTMENT[home_team]
    
    home_strength = home_strength * FATIGUE_MULTIPLIER.get(home_team, 1.0)
    away_strength = away_strength * FATIGUE_MULTIPLIER.get(away_team, 1.0)
    
    if group_id and group_id in ['A', 'D', 'K']:
        if away_team not in ['Mexico', 'Canada', 'USA']:
            away_strength = away_strength * 0.98
    
    base_lambda_home = 1.5 + (home_strength - away_strength) / 100 * 0.8
    base_lambda_away = 1.5 - (home_strength - away_strength) / 100 * 0.8
    
    lambda_home = max(0.3, base_lambda_home)
    lambda_away = max(0.3, base_lambda_away)
    
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0
    predictions = {}
    
    for h in range(5):
        for a in range(5):
            p_h = poisson_probability(lambda_home, h)
            p_a = poisson_probability(lambda_away, a)
            prob = p_h * p_a
            predictions[(h, a)] = prob
            
            if h > a:
                home_win_prob += prob
            elif h == a:
                draw_prob += prob
            else:
                away_win_prob += prob
    
    total = home_win_prob + draw_prob + away_win_prob
    home_win_prob /= total
    draw_prob /= total
    away_win_prob /= total
    
    max_prob_score = max(predictions.items(), key=lambda x: x[1])
    most_likely_score = max_prob_score[0]
    
    confidence_threshold = max_prob_score[1]
    if confidence_threshold > 0.20:
        confidence = 'high'
    elif confidence_threshold > 0.12:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    return {
        'home_score': most_likely_score[0],
        'away_score': most_likely_score[1],
        'home_win_prob': round(home_win_prob, 3),
        'draw_prob': round(draw_prob, 3),
        'away_win_prob': round(away_win_prob, 3),
        'confidence': confidence
    }

# Generate group stage matches
group_stage_predictions = []
match_id = 1

for group, teams in GROUPS.items():
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            home = teams[i]
            away = teams[j]
            prediction = predict_match(home, away, group)
            
            group_stage_predictions.append({
                'match_id': match_id,
                'stage': 'group_stage',
                'group': group,
                'home_team': home,
                'away_team': away,
                'predicted_home_score': prediction['home_score'],
                'predicted_away_score': prediction['away_score'],
                'home_win_probability': prediction['home_win_prob'],
                'draw_probability': prediction['draw_prob'],
                'away_win_probability': prediction['away_win_prob'],
                'model_confidence': prediction['confidence']
            })
            match_id += 1

# Determine group standings
group_standings = {}
for group in GROUPS.keys():
    group_standings[group] = {}
    for team in GROUPS[group]:
        group_standings[group][team] = {'points': 0, 'gf': 0, 'ga': 0}

for match in group_stage_predictions:
    home = match['home_team']
    away = match['away_team']
    group = match['group']
    h_score = match['predicted_home_score']
    a_score = match['predicted_away_score']
    
    if h_score > a_score:
        group_standings[group][home]['points'] += 3
    elif h_score < a_score:
        group_standings[group][away]['points'] += 3
    else:
        group_standings[group][home]['points'] += 1
        group_standings[group][away]['points'] += 1
    
    group_standings[group][home]['gf'] += h_score
    group_standings[group][home]['ga'] += a_score
    group_standings[group][away]['gf'] += a_score
    group_standings[group][away]['ga'] += h_score

# Get qualifiers
group_winners = {}
group_runners_up = {}
third_places = {}

for group, teams_dict in group_standings.items():
    ranked = sorted(teams_dict.items(), 
                   key=lambda x: (x[1]['points'], x[1]['gf'] - x[1]['ga'], x[1]['gf']), 
                   reverse=True)
    
    group_winners[group] = ranked[0][0]
    group_runners_up[group] = ranked[1][0]
    third_places[group] = (ranked[2][0], ranked[2][1]['points'])

third_sorted = sorted(third_places.items(), key=lambda x: x[1][1], reverse=True)[:8]
best_third_places = [t[1][0] for t in third_sorted]

# Round of 32 matchups
r32_matchups = [
    (group_winners['A'], group_runners_up['B']),
    (group_winners['B'], group_runners_up['A']),
    (group_winners['C'], group_runners_up['D']),
    (group_winners['D'], group_runners_up['C']),
    (group_winners['E'], group_runners_up['F']),
    (group_winners['F'], group_runners_up['E']),
    (group_winners['G'], group_runners_up['H']),
    (group_winners['H'], group_runners_up['G']),
    (group_winners['I'], group_runners_up['J']),
    (group_winners['J'], group_runners_up['I']),
    (group_winners['K'], group_runners_up['L']),
    (group_winners['L'], group_runners_up['K']),
    (best_third_places[0], best_third_places[1]),
    (best_third_places[2], best_third_places[3]),
    (best_third_places[4], best_third_places[5]),
    (best_third_places[6], best_third_places[7]),
]

# Generate knockout matches
knockout_predictions = []

# Round of 32
r32_winners = []
for idx, (home, away) in enumerate(r32_matchups):
    prediction = predict_match(home, away, None)
    
    if prediction['home_score'] > prediction['away_score']:
        winner = home
        penalties = 'none'
    elif prediction['away_score'] > prediction['home_score']:
        winner = away
        penalties = 'none'
    else:
        if TEAM_RATINGS.get(home, 60) >= TEAM_RATINGS.get(away, 60):
            winner = home
            penalties = home
        else:
            winner = away
            penalties = away
    
    r32_winners.append(winner)
    
    knockout_predictions.append({
        'match_id': 72 + idx + 1,
        'stage': 'round_of_32',
        'home_team': home,
        'away_team': away,
        'predicted_home_score': prediction['home_score'],
        'predicted_away_score': prediction['away_score'],
        'extra_time_or_penalties_winner': penalties,
        'home_win_probability': prediction['home_win_prob'],
        'draw_probability': prediction['draw_prob'],
        'away_win_probability': prediction['away_win_prob'],
        'model_confidence': prediction['confidence']
    })

# Round of 16
r16_matchups = [(r32_winners[i], r32_winners[i+1]) for i in range(0, 16, 2)]
r16_winners = []
for idx, (home, away) in enumerate(r16_matchups):
    prediction = predict_match(home, away, None)
    
    if prediction['home_score'] > prediction['away_score']:
        winner = home
        penalties = 'none'
    elif prediction['away_score'] > prediction['home_score']:
        winner = away
        penalties = 'none'
    else:
        if TEAM_RATINGS.get(home, 60) >= TEAM_RATINGS.get(away, 60):
            winner = home
            penalties = home
        else:
            winner = away
            penalties = away
    
    r16_winners.append(winner)
    
    knockout_predictions.append({
        'match_id': 88 + idx + 1,
        'stage': 'round_of_16',
        'home_team': home,
        'away_team': away,
        'predicted_home_score': prediction['home_score'],
        'predicted_away_score': prediction['away_score'],
        'extra_time_or_penalties_winner': penalties,
        'home_win_probability': prediction['home_win_prob'],
        'draw_probability': prediction['draw_prob'],
        'away_win_probability': prediction['away_win_prob'],
        'model_confidence': prediction['confidence']
    })

# Quarterfinals
qf_matchups = [(r16_winners[i], r16_winners[i+1]) for i in range(0, 8, 2)]
qf_winners = []
for idx, (home, away) in enumerate(qf_matchups):
    prediction = predict_match(home, away, None)
    
    if prediction['home_score'] > prediction['away_score']:
        winner = home
        penalties = 'none'
    elif prediction['away_score'] > prediction['home_score']:
        winner = away
        penalties = 'none'
    else:
        if TEAM_RATINGS.get(home, 60) >= TEAM_RATINGS.get(away, 60):
            winner = home
            penalties = home
        else:
            winner = away
            penalties = away
    
    qf_winners.append(winner)
    
    knockout_predictions.append({
        'match_id': 96 + idx + 1,
        'stage': 'quarterfinals',
        'home_team': home,
        'away_team': away,
        'predicted_home_score': prediction['home_score'],
        'predicted_away_score': prediction['away_score'],
        'extra_time_or_penalties_winner': penalties,
        'home_win_probability': prediction['home_win_prob'],
        'draw_probability': prediction['draw_prob'],
        'away_win_probability': prediction['away_win_prob'],
        'model_confidence': prediction['confidence']
    })

# Semifinals
sf_matchups = [(qf_winners[0], qf_winners[1]), (qf_winners[2], qf_winners[3])]
sf_winners = []
finalists = []
for idx, (home, away) in enumerate(sf_matchups):
    prediction = predict_match(home, away, None)
    
    if prediction['home_score'] > prediction['away_score']:
        winner = home
        penalties = 'none'
    elif prediction['away_score'] > prediction['home_score']:
        winner = away
        penalties = 'none'
    else:
        if TEAM_RATINGS.get(home, 60) >= TEAM_RATINGS.get(away, 60):
            winner = home
            penalties = home
        else:
            winner = away
            penalties = away
    
    sf_winners.append(winner)
    finalists.append((home, away, winner))
    
    knockout_predictions.append({
        'match_id': 100 + idx + 1,
        'stage': 'semifinals',
        'home_team': home,
        'away_team': away,
        'predicted_home_score': prediction['home_score'],
        'predicted_away_score': prediction['away_score'],
        'extra_time_or_penalties_winner': penalties,
        'home_win_probability': prediction['home_win_prob'],
        'draw_probability': prediction['draw_prob'],
        'away_win_probability': prediction['away_win_prob'],
        'model_confidence': prediction['confidence']
    })

# Third Place Playoff
third_place_loser1 = finalists[0][0] if finalists[0][2] != finalists[0][0] else finalists[0][1]
third_place_loser2 = finalists[1][0] if finalists[1][2] != finalists[1][0] else finalists[1][1]

prediction_3p = predict_match(third_place_loser1, third_place_loser2, None)

if prediction_3p['home_score'] > prediction_3p['away_score']:
    third_winner = third_place_loser1
else:
    third_winner = third_place_loser2

knockout_predictions.append({
    'match_id': 103,
    'stage': 'third_place',
    'home_team': third_place_loser1,
    'away_team': third_place_loser2,
    'predicted_home_score': prediction_3p['home_score'],
    'predicted_away_score': prediction_3p['away_score'],
    'extra_time_or_penalties_winner': 'none',
    'home_win_probability': prediction_3p['home_win_prob'],
    'draw_probability': prediction_3p['draw_prob'],
    'away_win_probability': prediction_3p['away_win_prob'],
    'model_confidence': prediction_3p['confidence']
})

# Grand Final
prediction_final = predict_match(sf_winners[0], sf_winners[1], None)

if prediction_final['home_score'] > prediction_final['away_score']:
    champion = sf_winners[0]
    penalties_final = 'none'
elif prediction_final['away_score'] > prediction_final['home_score']:
    champion = sf_winners[1]
    penalties_final = 'none'
else:
    if TEAM_RATINGS.get(sf_winners[0], 60) >= TEAM_RATINGS.get(sf_winners[1], 60):
        champion = sf_winners[0]
        penalties_final = sf_winners[0]
    else:
        champion = sf_winners[1]
        penalties_final = sf_winners[1]

knockout_predictions.append({
    'match_id': 104,
    'stage': 'grand_final',
    'home_team': sf_winners[0],
    'away_team': sf_winners[1],
    'predicted_home_score': prediction_final['home_score'],
    'predicted_away_score': prediction_final['away_score'],
    'extra_time_or_penalties_winner': penalties_final,
    'home_win_probability': prediction_final['home_win_prob'],
    'draw_probability': prediction_final['draw_prob'],
    'away_win_probability': prediction_final['away_win_prob'],
    'model_confidence': prediction_final['confidence']
})

all_predictions = group_stage_predictions + knockout_predictions

output = {
    'predictions': all_predictions,
    'metadata': {
        'model': 'Claude (Anthropic) Haiku 4.5',
        'tournament': '2026 FIFA World Cup',
        'total_matches': len(all_predictions),
        'group_stage_matches': len(group_stage_predictions),
        'knockout_matches': len(knockout_predictions),
        'predicted_champion': champion,
        'predicted_runner_up': sf_winners[1] if champion == sf_winners[0] else sf_winners[0],
        'predicted_third_place': third_winner
    }
}

with open('/sessions/practical-cool-gauss/mnt/outputs/predictions.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Predictions generated successfully!")
print(f"Total matches: {len(all_predictions)}")
print(f"Group stage: {len(group_stage_predictions)}")
print(f"Knockout: {len(knockout_predictions)}")
print(f"Predicted Champion: {champion}")
