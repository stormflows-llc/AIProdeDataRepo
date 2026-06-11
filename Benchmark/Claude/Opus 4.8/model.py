import math, itertools, json

# ---------------- TEAM RATINGS (0-100 overall), favoring RECENT FORM ----------------
# Derived from Nov-2025 FIFA ranking tiers (pots) + recent continental/qualifier form.
# off_lean / def_lean: small style offsets (sum ~0); + = stronger in that phase.
# fatigue: heavy-European-club squads get slight attack drag (user: factor club fatigue)
# heat: southern-US heat/travel adjustment applied contextually (user: factor travel/climate)
T = {
 # team: (overall, off_lean, def_lean, euro_club_fatigue_flag, heat_vulnerable_flag)
 "Mexico":        (76, +1, -1, 0, 0),
 "South Africa":  (70, 0, +1, 0, 0),
 "South Korea":   (74, +1, -1, 0, 1),
 "Czech Republic":(72, 0, 0, 1, 1),
 "Canada":        (74, +1, -1, 0, 0),
 "Bosnia and Herzegovina":(70, +1, -1, 1, 1),
 "Qatar":         (68, 0, +1, 0, 0),
 "Switzerland":   (77, -1, +2, 1, 1),
 "Brazil":        (86, +2, -1, 1, 0),
 "Morocco":       (82, 0, +2, 1, 0),
 "Haiti":         (61, +1, -2, 0, 0),
 "Scotland":      (71, 0, 0, 1, 1),
 "United States": (76, +1, -1, 0, 0),
 "Paraguay":      (70, -1, +2, 0, 0),
 "Australia":     (71, 0, +1, 0, 1),
 "Turkey":        (77, +2, -1, 1, 1),
 "Germany":       (85, +1, 0, 1, 1),
 "Curacao":       (60, 0, -1, 0, 0),
 "Ivory Coast":   (75, +1, 0, 1, 0),
 "Ecuador":       (77, -1, +2, 1, 0),
 "Netherlands":   (85, +2, -1, 1, 1),
 "Japan":         (79, +1, 0, 0, 1),
 "Sweden":        (73, +1, -1, 1, 1),
 "Tunisia":       (70, -1, +1, 0, 0),
 "Belgium":       (80, +1, -1, 1, 1),
 "Egypt":         (75, +1, 0, 0, 0),
 "Iran":          (73, -1, +1, 0, 0),
 "New Zealand":   (64, 0, 0, 0, 1),
 "Spain":         (91, +2, 0, 1, 1),
 "Cape Verde":    (67, +1, -1, 0, 0),
 "Saudi Arabia":  (69, 0, 0, 0, 0),
 "Uruguay":       (82, 0, +2, 1, 0),
 "France":        (90, +2, 0, 1, 1),
 "Senegal":       (79, +1, +1, 1, 0),
 "Iraq":          (67, -1, +1, 0, 0),
 "Norway":        (79, +3, -1, 1, 1),
 "Argentina":     (91, +1, +1, 1, 0),
 "Algeria":       (73, +1, -1, 1, 0),
 "Austria":       (78, +1, 0, 1, 1),
 "Jordan":        (68, 0, +1, 0, 0),
 "Portugal":      (86, +2, 0, 1, 1),
 "DR Congo":      (72, 0, 0, 1, 0),
 "Uzbekistan":    (69, 0, +1, 0, 1),
 "Colombia":      (83, +1, +1, 1, 0),
 "England":       (87, +1, +1, 1, 1),
 "Croatia":       (78, 0, +1, 1, 1),
 "Ghana":         (70, +1, -1, 1, 0),
 "Panama":        (67, 0, 0, 0, 0),
}

HOSTS = {"Mexico","United States","Canada"}

groups = {
 "A":["Mexico","South Africa","South Korea","Czech Republic"],
 "B":["Canada","Bosnia and Herzegovina","Qatar","Switzerland"],
 "C":["Brazil","Morocco","Haiti","Scotland"],
 "D":["United States","Paraguay","Australia","Turkey"],
 "E":["Germany","Curacao","Ivory Coast","Ecuador"],
 "F":["Netherlands","Japan","Sweden","Tunisia"],
 "G":["Belgium","Egypt","Iran","New Zealand"],
 "H":["Spain","Cape Verde","Saudi Arabia","Uruguay"],
 "I":["France","Senegal","Iraq","Norway"],
 "J":["Argentina","Algeria","Austria","Jordan"],
 "K":["Portugal","DR Congo","Uzbekistan","Colombia"],
 "L":["England","Croatia","Ghana","Panama"],
}

# attack / defense rating per team
def att(t): return T[t][0] + T[t][1]
def dfn(t): return T[t][0] + T[t][2]
AVG = sum(T[t][0] for t in T)/len(T)  # ~ average overall

BASE = 1.30  # league-average goals per team
S_ATT = 26.0 # sensitivity scale

def lam(team, opp, host=False, knockout=False, neutral_us=False):
    # expected goals for `team` vs `opp`
    a = att(team); d = dfn(opp)
    l = BASE * math.exp((a-AVG)/S_ATT) * math.exp(-(d-AVG)/S_ATT)
    # home-field (moderate ~1.27 attack lift), hosts in own country
    if host:
        l *= 1.27
    elif neutral_us and team=="United States" and knockout:
        l *= 1.08
    # club fatigue: heavy euro-club squads slight attack drag
    if T[team][3]==1:
        l *= 0.975
    # heat/travel: heat-vulnerable teams slight drag (more in group stage south venues)
    if T[team][4]==1:
        l *= 0.985
    return max(0.15, l)

def score_matrix(lh, la, N=9):
    m=[[ (lh**i*math.exp(-lh)/math.factorial(i))*(la**j*math.exp(-la)/math.factorial(j))
         for j in range(N)] for i in range(N)]
    return m

def analyze(home, away, host_home=False, knockout=False, neutral_us=False):
    lh = lam(home, away, host=host_home, knockout=knockout, neutral_us=neutral_us)
    la = lam(away, home, host=False, knockout=knockout, neutral_us=neutral_us)
    m = score_matrix(lh,la)
    # most likely exact scoreline
    best=(0,0); bp=-1
    for i in range(9):
        for j in range(9):
            if m[i][j]>bp: bp=m[i][j]; best=(i,j)
    pH=sum(m[i][j] for i in range(9) for j in range(9) if i>j)
    pD=sum(m[i][j] for i in range(9) for j in range(9) if i==j)
    pA=sum(m[i][j] for i in range(9) for j in range(9) if i<j)
    tot=pH+pD+pA
    return best, lh, la, pH/tot, pD/tot, pA/tot

# ---------------- GROUP STAGE ----------------
results=[]   # match dicts
mid=1
standings={}  # team -> dict
for g,teams in groups.items():
    for t in teams:
        standings[t]={"pts":0,"gf":0,"ga":0,"gd":0,"g":g}
    # round robin order: official matchday pattern 1v2,3v4 / 1v3,4v2 / 4v1,2v3
    pairs=[(0,1),(2,3),(0,2),(3,1),(3,0),(1,2)]
    for (x,y) in pairs:
        h=teams[x]; a=teams[y]
        host_home = h in HOSTS
        (sh,sa),lh,la,pH,pD,pA = analyze(h,a,host_home=host_home)
        results.append({"stage":"group_stage","group":g,"match_id":mid,
            "home_team":h,"away_team":a,"predicted_home_score":sh,"predicted_away_score":sa,
            "extra_time_or_penalties_winner":"none",
            "home_win_probability":round(pH,2),"draw_probability":round(pD,2),
            "away_win_probability":round(pA,2),
            "model_confidence": "high" if abs(pH-pA)>0.35 else ("medium" if abs(pH-pA)>0.15 else "low"),
            "lh":lh,"la":la})
        # points
        if sh>sa: standings[h]["pts"]+=3
        elif sh<sa: standings[a]["pts"]+=3
        else: standings[h]["pts"]+=1; standings[a]["pts"]+=1
        standings[h]["gf"]+=sh; standings[h]["ga"]+=sa
        standings[a]["gf"]+=sa; standings[a]["ga"]+=sh
        mid+=1

for t in standings:
    standings[t]["gd"]=standings[t]["gf"]-standings[t]["ga"]

def rank_key(t):
    s=standings[t]
    return (s["pts"], s["gd"], s["gf"], T[t][0])

group_rank={}
thirds=[]
for g,teams in groups.items():
    order=sorted(teams,key=rank_key,reverse=True)
    group_rank[g]=order
    thirds.append((g,order[2]))

# rank thirds, take best 8
thirds_sorted=sorted(thirds,key=lambda gt:(standings[gt[1]]["pts"],standings[gt[1]]["gd"],standings[gt[1]]["gf"],T[gt[1]][0]),reverse=True)
best8=thirds_sorted[:8]
best8_groups=sorted([g for g,_ in best8])

print("=== GROUP RESULTS ===")
for g,teams in groups.items():
    print(f"Group {g}:")
    for i,t in enumerate(group_rank[g]):
        s=standings[t]
        print(f"  {i+1}. {t:24s} pts={s['pts']} gd={s['gd']:+d} gf={s['gf']}")
print("\n=== 8 BEST THIRDS (groups) ===")
print(best8_groups)
for g,t in thirds_sorted:
    s=standings[t]
    mark="QUALIFY" if g in best8_groups else "out"
    print(f"  3rd Group {g}: {t:22s} pts={s['pts']} gd={s['gd']:+d} gf={s['gf']}  {mark}")

import pickle
pickle.dump({"results":results,"standings":standings,"group_rank":group_rank,
             "best8_groups":best8_groups,"mid":mid}, open("/sessions/happy-jolly-dijkstra/mnt/outputs/state.pkl","wb"))
