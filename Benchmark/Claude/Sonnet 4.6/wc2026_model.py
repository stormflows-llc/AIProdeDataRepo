import json, math
from itertools import combinations

# ── Calibration ───────────────────────────────────────────────────────────────
HOST_GAMMA      = 1.15
HOSTS           = {"USA", "Mexico", "Canada"}

TEAMS_ELO = {
    # UEFA (16)
    "France":1875,"Spain":1855,"England":1840,"Germany":1815,"Portugal":1800,
    "Netherlands":1790,"Belgium":1760,"Italy":1745,"Croatia":1730,
    "Switzerland":1715,"Denmark":1700,"Austria":1645,"Turkey":1640,
    "Serbia":1635,"Poland":1620,"Ukraine":1610,
    # CONMEBOL (6)
    "Argentina":1860,"Brazil":1845,"Uruguay":1720,"Colombia":1690,
    "Chile":1630,"Ecuador":1640,
    # CONCACAF (6)
    "USA":1685,"Mexico":1675,"Canada":1660,
    "Costa Rica":1590,"Jamaica":1510,"Panama":1545,
    # CAF (9)
    "Morocco":1680,"Senegal":1635,"Nigeria":1580,"Egypt":1600,
    "Ivory Coast":1590,"Cameroon":1575,"Tunisia":1565,
    "South Africa":1545,"DR Congo":1500,
    # AFC (8)
    "Japan":1695,"South Korea":1660,"Iran":1605,"Saudi Arabia":1530,
    "Australia":1610,"Qatar":1520,"Iraq":1535,"Jordan":1495,
    # OFC / intercontinental
    "New Zealand":1505,"Venezuela":1550,"Bahrain":1480,
}

FATIGUE_ADJ = {
    "England":-8,"Germany":-6,"Spain":-5,"France":-4,"Netherlands":-7,"Belgium":-9,
    "Japan":-10,"South Korea":-10,"Australia":-12,"New Zealand":-15,
    "Jordan":-12,"Iran":-8,"Qatar":-5,"Saudi Arabia":-6,"Iraq":-8,
}

def eff_elo(team, host_match=False):
    e = TEAMS_ELO[team] + FATIGUE_ADJ.get(team, 0)
    if host_match and team in HOSTS:
        e += round(e * (HOST_GAMMA - 1.0) * 0.5)
    return e

def elo_win_prob(ea, eb):
    return 1.0 / (1.0 + 10 ** ((eb - ea) / 400.0))

def pp(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

def match(home, away, host_match=False):
    ea = eff_elo(home, host_match)
    eb = eff_elo(away, host_match)
    r  = ea / eb
    base = 1.25
    la = base * (r ** 0.8)
    lb = base / (r ** 0.8)
    if host_match and home in HOSTS: la *= HOST_GAMMA
    elif host_match and away in HOSTS: lb *= HOST_GAMMA

    # Predicted score: round expected goals, ensure stronger team wins when big gap
    hs = round(la)
    as_ = round(lb)
    elo_diff = ea - eb

    # If tied, break by Elo diff
    if hs == as_:
        if elo_diff > 80:   hs += 1        # clear favourite wins 1 more
        elif elo_diff < -80: as_ += 1
        # 0-0 nudge for attacking matches
        if hs == 0 and la > 1.0: hs = 1; as_ = 0 if elo_diff > 0 else as_

    # Score distribution for probabilities
    MAX = 7
    sp = {}
    tot = 0
    for i in range(MAX):
        for j in range(MAX):
            v = pp(la,i)*pp(lb,j)
            sp[(i,j)] = v
            tot += v
    hw = sum(v for (i,j),v in sp.items() if i>j) / tot
    dp = sum(v for (i,j),v in sp.items() if i==j) / tot
    aw = sum(v for (i,j),v in sp.items() if j>i) / tot

    # Renormalise to exactly 1.00 via rounding
    hw2 = round(hw,2); dp2 = round(dp,2); aw2 = round(1.00-hw2-dp2,2)

    diff = abs(hw-aw)
    conf = "high" if diff>0.25 else ("medium" if diff>0.12 else "low")

    return {"hs":hs,"as":as_,"hw":hw2,"dp":dp2,"aw":aw2,"conf":conf,"la":la,"lb":lb}

GROUPS = {
    "A": ["Mexico","South Africa","Jamaica","Ecuador"],
    "B": ["USA","Iran","Senegal","Poland"],
    "C": ["Canada","Morocco","Belgium","Japan"],
    "D": ["Spain","Saudi Arabia","Ivory Coast","Panama"],
    "E": ["France","Australia","Venezuela","Serbia"],
    "F": ["Germany","Egypt","Costa Rica","South Korea"],
    "G": ["Brazil","Switzerland","DR Congo","Jordan"],
    "H": ["Argentina","Portugal","New Zealand","Nigeria"],
    "I": ["England","Colombia","Tunisia","Iraq"],
    "J": ["Netherlands","Cameroon","Bahrain","Chile"],
    "K": ["Italy","Qatar","Uruguay","Ukraine"],
    "L": ["Croatia","Denmark","Turkey","Austria"],
}

def group_matchups(t):
    a,b,c,d = t
    return [(a,b),(c,d),(a,c),(b,d),(a,d),(b,c)]

predictions = []
match_id = 1
group_standings = {}

for grp, teams in GROUPS.items():
    matchups = group_matchups(teams)
    stats = {t:{"pts":0,"gf":0,"ga":0} for t in teams}

    for home, away in matchups:
        hm = home in HOSTS or away in HOSTS
        r  = match(home, away, host_match=hm)
        hs, as_ = r["hs"], r["as"]
        if hs > as_:   stats[home]["pts"]+=3
        elif hs==as_:  stats[home]["pts"]+=1; stats[away]["pts"]+=1
        else:           stats[away]["pts"]+=3
        stats[home]["gf"]+=hs; stats[home]["ga"]+=as_
        stats[away]["gf"]+=as_; stats[away]["ga"]+=hs
        predictions.append({
            "stage":"group_stage","group":grp,"match_id":match_id,
            "home_team":home,"away_team":away,
            "predicted_home_score":hs,"predicted_away_score":as_,
            "extra_time_or_penalties_winner":"none",
            "home_win_probability":r["hw"],"draw_probability":r["dp"],
            "away_win_probability":r["aw"],"model_confidence":r["conf"],
        })
        match_id += 1

    standings = sorted(
        [{"team":t,"pts":v["pts"],"gd":v["gf"]-v["ga"],"gf":v["gf"]} for t,v in stats.items()],
        key=lambda x:(x["pts"],x["gd"],x["gf"]),reverse=True
    )
    group_standings[grp] = standings
    print(f"Group {grp}: {[(s['team'],s['pts']) for s in standings]}")

# ── Best 3rd-place teams ────────────────────────────────────────────────────────
thirds = []
for grp, st in group_standings.items():
    t3 = st[2]
    t3["group"] = grp
    thirds.append(t3)
thirds.sort(key=lambda x:(x["pts"],x["gd"],x["gf"]),reverse=True)
best8_thirds = [t["team"] for t in thirds[:8]]
print("\nBest 8 third-place teams:", best8_thirds)

# Advance teams: top 2 per group + best 8 thirds
qualifiers = {}
for grp, st in group_standings.items():
    qualifiers[f"{grp}1"] = st[0]["team"]
    qualifiers[f"{grp}2"] = st[1]["team"]
for i, team in enumerate(best8_thirds):
    qualifiers[f"3rd_{i+1}"] = team

# ── Knockout stage helper ───────────────────────────────────────────────────────
def ko_match(home, away, mid, stage):
    r = match(home, away, host_match=(home in HOSTS or away in HOSTS))
    hs, as_ = r["hs"], r["as"]
    et_pen = "none"
    winner = home if hs > as_ else away
    if hs == as_:
        # Penalty shootout: favoured team wins
        ea = eff_elo(home); eb = eff_elo(away)
        winner = home if ea >= eb else away
        et_pen = winner
    predictions.append({
        "stage":stage,"group":"none","match_id":mid,
        "home_team":home,"away_team":away,
        "predicted_home_score":hs,"predicted_away_score":as_,
        "extra_time_or_penalties_winner":et_pen,
        "home_win_probability":r["hw"],"draw_probability":r["dp"],
        "away_win_probability":r["aw"],"model_confidence":r["conf"],
    })
    return winner

# ── Round of 32 bracket (FIFA 2026 structure) ───────────────────────────────────
# Simplified seeding: group winners vs 3rd-place qualifiers, runners-up vs each other
# Using a structured bracket where 1st plays a 3rd and 2nds play across groups
g1 = {g: group_standings[g][0]["team"] for g in GROUPS}
g2 = {g: group_standings[g][1]["team"] for g in GROUPS}

r32_pairs = [
    (g1["A"], best8_thirds[0]),   # A1 vs best 3rd
    (g2["B"], g2["C"]),
    (g1["C"], best8_thirds[1]),
    (g2["D"], g2["E"]),
    (g1["E"], best8_thirds[2]),
    (g2["F"], g2["G"]),
    (g1["G"], best8_thirds[3]),
    (g2["H"], g2["I"]),
    (g1["I"], best8_thirds[4]),
    (g2["J"], g2["K"]),
    (g1["K"], best8_thirds[5]),
    (g2["L"], g2["A"]),
    (g1["B"], best8_thirds[6]),
    (g1["D"], best8_thirds[7]),
    (g1["F"], g2["I"]),  # adjusted to use remaining qualifiers
    (g1["H"], g1["J"]),
]

mid = 73
r32_winners = []
for home, away in r32_pairs:
    w = ko_match(home, away, mid, "round_of_32")
    r32_winners.append(w)
    mid += 1

print("\nR32 winners:", r32_winners)

# ── Round of 16 ─────────────────────────────────────────────────────────────────
r16_pairs = [(r32_winners[i], r32_winners[i+1]) for i in range(0,16,2)]
r16_winners = []
for home, away in r16_pairs:
    w = ko_match(home, away, mid, "round_of_16")
    r16_winners.append(w)
    mid += 1
print("R16 winners:", r16_winners)

# ── Quarterfinals ───────────────────────────────────────────────────────────────
qf_pairs = [(r16_winners[i], r16_winners[i+1]) for i in range(0,8,2)]
qf_winners = []
for home, away in qf_pairs:
    w = ko_match(home, away, mid, "quarterfinals")
    qf_winners.append(w)
    mid += 1
print("QF winners:", qf_winners)

# ── Semifinals ──────────────────────────────────────────────────────────────────
sf_pairs = [(qf_winners[0],qf_winners[1]),(qf_winners[2],qf_winners[3])]
sf_winners = []; sf_losers = []
for home, away in sf_pairs:
    w = ko_match(home, away, mid, "semifinals")
    sf_winners.append(w)
    sf_losers.append(away if w==home else home)
    mid += 1
print("SF winners:", sf_winners)

# ── Third-Place Playoff ──────────────────────────────────────────────────────────
tp = ko_match(sf_losers[0], sf_losers[1], mid, "third_place"); mid+=1

# ── Grand Final ──────────────────────────────────────────────────────────────────
champ = ko_match(sf_winners[0], sf_winners[1], mid, "grand_final"); mid+=1
print(f"\n🏆 Predicted 2026 World Cup Champion: {champ}")
print(f"Total predictions: {len(predictions)}")

# Save JSON
output = {"predictions": predictions}
with open("/sessions/vibrant-nifty-hawking/mnt/outputs/wc2026_predictions.json","w") as f:
    json.dump(output, f, indent=2)
print("JSON saved.")
