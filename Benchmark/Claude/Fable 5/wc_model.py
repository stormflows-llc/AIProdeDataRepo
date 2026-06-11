#!/usr/bin/env python3
"""
2026 FIFA World Cup end-to-end predictive model.
Calibration (user interview):
  - 70/30 recent-continental vs historical-WC weighting (baked into ratings)
  - Tiered home gamma: MEX 1.25, USA 1.15, CAN 1.10 (group stage), decaying in KO
  - Club fatigue (phi) and travel/climate friction (tau) included
Independent Poisson goals model with exponential strength link.
"""
import json, math
from math import exp, factorial

MU = 1.28          # base goals per team per match (neutral, equal strength)
KAPPA = 2.3        # sensitivity of scoring rate to strength differential
MAXG = 10          # truncation for Poisson grid

# team: (off, dfn, recent R_rec, hist R_hist, fatigue phi, travel tau)
# Overall = 0.7*R_rec + 0.3*R_hist (off/dfn are the decomposition used by the engine)
T = {
 # name              off   dfn   rec   hist  phi    tau
 "Mexico":          (78,   79,   77,   80,   1.000, 1.000),
 "South Africa":    (68,   70,   70,   66,   1.000, 0.990),
 "South Korea":     (76,   74,   76,   73,   0.990, 0.990),
 "Czechia":         (74,   73,   74,   72,   0.990, 0.985),
 "Canada":          (75,   74,   76,   71,   1.000, 1.000),
 "Bosnia and Herzegovina": (71, 69, 71, 68,  0.995, 0.985),
 "Qatar":           (66,   65,   66,   64,   1.000, 0.990),
 "Switzerland":     (78,   81,   80,   78,   0.990, 0.985),
 "Brazil":          (89,   87,   87,   90,   0.985, 0.995),
 "Morocco":         (81,   85,   84,   80,   0.990, 0.990),
 "Haiti":           (62,   61,   62,   60,   1.000, 1.000),
 "Scotland":        (72,   72,   73,   70,   0.990, 0.985),
 "United States":   (78,   78,   78,   77,   0.995, 1.000),
 "Paraguay":        (71,   76,   74,   72,   1.000, 0.995),
 "Australia":       (72,   73,   73,   71,   0.995, 0.980),
 "Türkiye":    (79,   75,   78,   74,   0.990, 0.985),
 "Germany":         (87,   84,   85,   88,   0.985, 0.985),
 "Curaçao":    (60,   62,   62,   58,   1.000, 1.000),
 "Ivory Coast":     (73,   71,   73,   70,   0.995, 0.990),
 "Ecuador":         (74,   79,   77,   74,   1.000, 0.995),
 "Netherlands":     (86,   87,   87,   85,   0.985, 0.985),
 "Japan":           (81,   80,   82,   78,   0.990, 0.980),
 "Sweden":          (75,   71,   73,   73,   0.990, 0.985),
 "Tunisia":         (69,   72,   71,   68,   1.000, 0.990),
 "Belgium":         (84,   82,   83,   83,   0.985, 0.985),
 "Egypt":           (74,   76,   76,   72,   0.995, 0.990),
 "Iran":            (72,   74,   74,   71,   1.000, 0.985),
 "New Zealand":     (61,   63,   62,   61,   1.000, 0.985),
 "Spain":           (95,   93,   96,   89,   0.980, 0.985),
 "Cape Verde":      (62,   64,   64,   60,   1.000, 0.990),
 "Saudi Arabia":    (67,   68,   68,   66,   1.000, 0.990),
 "Uruguay":         (80,   84,   82,   81,   0.995, 0.995),
 "France":          (93,   93,   93,   93,   0.980, 0.985),
 "Senegal":         (77,   79,   79,   75,   0.995, 0.990),
 "Iraq":            (63,   66,   65,   62,   1.000, 0.985),
 "Norway":          (84,   76,   83,   72,   0.990, 0.985),
 "Argentina":       (92,   92,   93,   90,   0.985, 0.995),
 "Algeria":         (75,   73,   75,   72,   0.995, 0.990),
 "Austria":         (77,   76,   78,   72,   0.990, 0.985),
 "Jordan":          (64,   64,   65,   61,   1.000, 0.985),
 "Portugal":        (90,   88,   90,   86,   0.980, 0.985),
 "DR Congo":        (67,   66,   68,   63,   1.000, 0.990),
 "Uzbekistan":      (66,   67,   67,   64,   1.000, 0.985),
 "Colombia":        (82,   81,   82,   80,   0.995, 0.995),
 "England":         (89,   91,   91,   87,   0.980, 0.985),
 "Croatia":         (82,   83,   81,   86,   0.985, 0.985),
 "Ghana":           (72,   70,   71,   72,   0.995, 0.990),
 "Panama":          (63,   65,   65,   61,   1.000, 1.000),
}
OFF = {k: v[0] for k, v in T.items()}
DEF = {k: v[1] for k, v in T.items()}
PHI = {k: v[4] for k, v in T.items()}
TAU = {k: v[5] for k, v in T.items()}
OVR = {k: round(0.7*v[2] + 0.3*v[3], 1) for k, v in T.items()}

HOST_GAMMA_GROUP = {"Mexico": 1.25, "United States": 1.15, "Canada": 1.10}
HOST_GAMMA_R32   = {"Mexico": 1.20, "United States": 1.15, "Canada": 1.08}
HOST_GAMMA_R16   = {"Mexico": 1.15, "United States": 1.15, "Canada": 1.04}
HOST_GAMMA_LATE  = {"Mexico": 1.05, "United States": 1.15, "Canada": 1.04}

# draw positions 1-4 per group
G = {
 "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
 "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
 "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
 "D": ["United States", "Paraguay", "Australia", "Türkiye"],
 "E": ["Germany", "Curaçao", "Ivory Coast", "Ecuador"],
 "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
 "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
 "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
 "I": ["France", "Senegal", "Iraq", "Norway"],
 "J": ["Argentina", "Algeria", "Austria", "Jordan"],
 "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
 "L": ["England", "Croatia", "Ghana", "Panama"],
}

def pois(lmbda, k):
    return lmbda**k * exp(-lmbda) / factorial(k)

def lambdas(home, away, gamma_h=1.0, gamma_a=1.0):
    lh = MU * exp(KAPPA*(OFF[home]-DEF[away])/100.0) * gamma_h * PHI[home] * TAU[home]
    la = MU * exp(KAPPA*(OFF[away]-DEF[home])/100.0) * gamma_a * PHI[away] * TAU[away]
    return lh, la

def score_matrix(lh, la):
    return [[pois(lh,i)*pois(la,j) for j in range(MAXG)] for i in range(MAXG)]

def outcome_probs(M):
    pw = sum(M[i][j] for i in range(MAXG) for j in range(MAXG) if i > j)
    pd = sum(M[i][i] for i in range(MAXG))
    pl = sum(M[i][j] for i in range(MAXG) for j in range(MAXG) if i < j)
    s = pw+pd+pl
    return pw/s, pd/s, pl/s

def modal_score(M, region):
    best, bi, bj = -1, 0, 0
    for i in range(MAXG):
        for j in range(MAXG):
            ok = (region=="H" and i>j) or (region=="D" and i==j) or (region=="A" and i<j)
            if ok and M[i][j] > best:
                best, bi, bj = M[i][j], i, j
    return bi, bj

def round_probs(pw, pd, pl):
    r = [round(pw,2), round(pd,2), round(pl,2)]
    diff = round(1.00 - sum(r), 2)
    # add residual to largest component
    idx = max(range(3), key=lambda i: r[i])
    r[idx] = round(r[idx] + diff, 2)
    return r

def host_gamma(team, country_ok, table):
    return table.get(team, 1.0) if country_ok else 1.0

def predict_group_match(home, away):
    gh = HOST_GAMMA_GROUP.get(home, 1.0)
    ga = HOST_GAMMA_GROUP.get(away, 1.0)
    lh, la = lambdas(home, away, gh, ga)
    M = score_matrix(lh, la)
    pw, pd, pl = outcome_probs(M)
    region = "H" if pw >= max(pd, pl) else ("D" if pd >= pl else "A")
    hs, as_ = modal_score(M, region)
    return dict(lh=lh, la=la, M=M, pw=pw, pd=pd, pl=pl, hs=hs, as_=as_)

def confidence(maxp, ko=False, padv=None):
    if ko:
        m = max(padv, 1-padv)
        return "high" if m >= 0.70 else ("medium" if m >= 0.58 else "low")
    return "high" if maxp >= 0.55 else ("medium" if maxp >= 0.40 else "low")

# ---------- build group fixtures with chronological match ids ----------
def md_pairs(md):
    if md == 1: return [(0,1),(2,3)]
    if md == 2: return [(0,2),(3,1)]
    return [(3,0),(1,2)]

schedule = []  # (match_id, group, home, away)
mid = 0
def add(g, pair):
    global mid
    mid += 1
    schedule.append((mid, g, G[g][pair[0]], G[g][pair[1]]))

# MD1
add("A", (0,1)); add("A", (2,3))                      # Jun 11
add("B", (0,1)); add("D", (0,1))                      # Jun 12
add("B", (2,3)); add("C", (0,1)); add("C", (2,3)); add("D", (2,3))  # Jun 13
for g in ["E","F"]: [add(g,p) for p in md_pairs(1)]   # Jun 14
for g in ["G","H"]: [add(g,p) for p in md_pairs(1)]   # Jun 15
for g in ["I","J"]: [add(g,p) for p in md_pairs(1)]   # Jun 16
for g in ["K","L"]: [add(g,p) for p in md_pairs(1)]   # Jun 17
# MD2
for day in [["A","B"],["C","D"],["E","F"],["G","H"],["I","J"],["K","L"]]:
    for g in day: [add(g,p) for p in md_pairs(2)]
# MD3
for day in [["A","B","C"],["D","E","F"],["G","H","I"],["J","K","L"]]:
    for g in day: [add(g,p) for p in md_pairs(3)]

assert mid == 72

# ---------- simulate group stage ----------
results = {}
table = {g: {t: dict(P=0,W=0,D=0,L=0,GF=0,GA=0) for t in G[g]} for g in G}
for (m, g, h, a) in schedule:
    r = predict_group_match(h, a)
    results[m] = (g, h, a, r)
    hs, as_ = r["hs"], r["as_"]
    th, ta = table[g][h], table[g][a]
    th["GF"] += hs; th["GA"] += as_; ta["GF"] += as_; ta["GA"] += hs
    if hs > as_: th["P"] += 3; th["W"] += 1; ta["L"] += 1
    elif hs < as_: ta["P"] += 3; ta["W"] += 1; th["L"] += 1
    else: th["P"] += 1; ta["P"] += 1; th["D"] += 1; ta["D"] += 1

def rank_key(g):
    def k(t):
        s = table[g][t]
        return (-s["P"], -(s["GF"]-s["GA"]), -s["GF"], -OVR[t])
    return k

standings = {g: sorted(G[g], key=rank_key(g)) for g in G}
print("=== GROUP TABLES ===")
for g in G:
    for t in standings[g]:
        s = table[g][t]
        print(f"{g} {t:25s} P{s['P']} W{s['W']} D{s['D']} L{s['L']} GF{s['GF']} GA{s['GA']} GD{s['GF']-s['GA']}")
    print()

thirds = [(g, standings[g][2]) for g in G]
def third_key(item):
    g, t = item
    s = table[g][t]
    return (-s["P"], -(s["GF"]-s["GA"]), -s["GF"], -OVR[t])
thirds_sorted = sorted(thirds, key=third_key)
advancing = thirds_sorted[:8]
adv_groups = sorted(g for g, _ in advancing)
print("=== THIRD PLACE RANKING ===")
for g, t in thirds_sorted:
    s = table[g][t]
    print(f"{g} {t:25s} P{s['P']} GD{s['GF']-s['GA']} GF{s['GF']}")
print("Advancing third-place groups:", adv_groups)

# print all group match predictions
print("\n=== GROUP MATCH PREDICTIONS ===")
for m in range(1, 73):
    g, h, a, r = results[m]
    pr = round_probs(r["pw"], r["pd"], r["pl"])
    print(f"M{m:02d} [{g}] {h} {r['hs']}-{r['as_']} {a}  W/D/L {pr}  lam {r['lh']:.2f}/{r['la']:.2f}")

# ---------- knockout stage ----------
W = {g: standings[g][0] for g in G}   # winners
RU = {g: standings[g][1] for g in G}  # runners-up
TH = {g: standings[g][2] for g in G}  # thirds

# Annex C row 281 for advancing thirds {A,C,D,E,F,G,I,J}
assert adv_groups == ['A','C','D','E','F','G','I','J'], adv_groups
third_slot = {79:"C", 85:"G", 81:"J", 74:"D", 82:"A", 77:"F", 87:"E", 80:"I"}

r32 = {
 73: (RU["A"], RU["B"]), 74: (W["E"], TH[third_slot[74]]),
 75: (W["F"], RU["C"]),  76: (W["C"], RU["F"]),
 77: (W["I"], TH[third_slot[77]]), 78: (RU["E"], RU["I"]),
 79: (W["A"], TH[third_slot[79]]), 80: (W["L"], TH[third_slot[80]]),
 81: (W["D"], TH[third_slot[81]]), 82: (W["G"], TH[third_slot[82]]),
 83: (RU["K"], RU["L"]), 84: (W["H"], RU["J"]),
 85: (W["B"], TH[third_slot[85]]), 86: (W["J"], RU["H"]),
 87: (W["K"], TH[third_slot[87]]), 88: (RU["D"], RU["G"]),
}

GAMMA_BY_ROUND = {
 "round_of_32": HOST_GAMMA_R32, "round_of_16": HOST_GAMMA_R16,
 "quarterfinals": HOST_GAMMA_LATE, "semifinals": HOST_GAMMA_LATE,
 "third_place": HOST_GAMMA_LATE, "grand_final": HOST_GAMMA_LATE,
}

ko_results = {}  # mid -> dict
def predict_ko(mid_, home, away, stage):
    gt = GAMMA_BY_ROUND[stage]
    gh, ga = gt.get(home, 1.0), gt.get(away, 1.0)
    lh, la = lambdas(home, away, gh, ga)
    M = score_matrix(lh, la)
    pw, pd, pl = outcome_probs(M)
    w_et = pw/(pw+pl)
    p_adv = pw + pd*w_et
    winner = home if p_adv >= 0.5 else away
    loser = away if winner == home else home
    # pick the most probable exact scoreline among (winner-win cells) U (draw cells)
    wreg = "H" if winner == home else "A"
    whs, was = modal_score(M, wreg)
    dhs, das = modal_score(M, "D")
    # volatility band: coin-flip ties whose joint modal scoreline is level go to ET/pens
    if abs(p_adv - 0.5) < 0.08 and M[dhs][das] > M[whs][was]:
        hs, as_, et = dhs, das, winner
    else:
        hs, as_, et = whs, was, "none"
    ko_results[mid_] = dict(stage=stage, home=home, away=away, hs=hs, as_=as_,
                            pw=pw, pd=pd, pl=pl, p_adv=p_adv, winner=winner,
                            loser=loser, et=et, M=M, lh=lh, la=la)
    return winner

print("\n=== KNOCKOUT ===")
for m in sorted(r32): predict_ko(m, *r32[m], "round_of_32")
WIN = {m: ko_results[m]["winner"] for m in r32}
r16 = {89:(WIN[74],WIN[77]), 90:(WIN[73],WIN[75]), 91:(WIN[76],WIN[78]), 92:(WIN[79],WIN[80]),
       93:(WIN[83],WIN[84]), 94:(WIN[81],WIN[82]), 95:(WIN[86],WIN[88]), 96:(WIN[85],WIN[87])}
for m in sorted(r16): WIN[m] = predict_ko(m, *r16[m], "round_of_16")
qf = {97:(WIN[89],WIN[90]), 98:(WIN[93],WIN[94]), 99:(WIN[91],WIN[92]), 100:(WIN[95],WIN[96])}
for m in sorted(qf): WIN[m] = predict_ko(m, *qf[m], "quarterfinals")
sf = {101:(WIN[97],WIN[98]), 102:(WIN[99],WIN[100])}
for m in sorted(sf): WIN[m] = predict_ko(m, *sf[m], "semifinals")
L101, L102 = ko_results[101]["loser"], ko_results[102]["loser"]
predict_ko(103, L101, L102, "third_place")
predict_ko(104, WIN[101], WIN[102], "grand_final")

for m in range(73, 105):
    r = ko_results[m]
    pr = round_probs(r["pw"], r["pd"], r["pl"])
    tag = f" -> {r['winner']} via ET/pens" if r["et"] != "none" else ""
    print(f"M{m} [{r['stage']}] {r['home']} {r['hs']}-{r['as_']} {r['away']} adv={r['winner']} Padv={r['p_adv']:.2f} W/D/L {pr}{tag}")

# ---------- JSON ----------
preds = []
for m in range(1, 73):
    g, h, a, r = results[m]
    pr = round_probs(r["pw"], r["pd"], r["pl"])
    preds.append({
      "stage": "group_stage", "group": g, "match_id": m,
      "home_team": h, "away_team": a,
      "predicted_home_score": r["hs"], "predicted_away_score": r["as_"],
      "extra_time_or_penalties_winner": "none",
      "home_win_probability": pr[0], "draw_probability": pr[1], "away_win_probability": pr[2],
      "model_confidence": confidence(max(pr)),
    })
for m in range(73, 105):
    r = ko_results[m]
    pr = round_probs(r["pw"], r["pd"], r["pl"])
    preds.append({
      "stage": r["stage"], "group": "none", "match_id": m,
      "home_team": r["home"], "away_team": r["away"],
      "predicted_home_score": r["hs"], "predicted_away_score": r["as_"],
      "extra_time_or_penalties_winner": r["et"],
      "home_win_probability": pr[0], "draw_probability": pr[1], "away_win_probability": pr[2],
      "model_confidence": confidence(None, ko=True, padv=r["p_adv"]),
    })

with open("predictions.json", "w") as f:
    json.dump({"predictions": preds}, f, ensure_ascii=False, indent=2)
print("\nJSON written:", len(preds), "matches")

# ---------- density grids ----------
def grid(M, ta, tb):
    mx = max(M[i][j] for i in range(4) for j in range(4))
    def ch(p):
        r = p/mx
        return "█" if r >= 0.999 else ("▓" if r >= 0.5 else ("▒" if r >= 0.2 else "░"))
    lines = [f"[{tb} Goals]"]
    for j in range(3, -1, -1):
        lines.append(f"   {j} |  " + "   ".join(ch(M[i][j]) for i in range(4)))
    lines.append("     +---------------")
    lines.append(f"        0   1   2   3  [{ta} Goals]")
    return "\n".join(lines)

print("\n=== GRID M1 Mexico vs South Africa ===")
g1 = results[1][3]["M"]; print(grid(g1, "Mexico", "South Africa"))
print("\n=== GRID M63 Uruguay vs Spain ===")
g2 = results[63][3]["M"]; print(grid(g2, "Uruguay", "Spain"))
print("\n=== GRID M104 Final ===")
rf = ko_results[104]; print(grid(rf["M"], rf["home"], rf["away"]))

# ratings table for paper
print("\n=== RATINGS ===")
for t in sorted(T, key=lambda x: -OVR[x]):
    print(f"{t:26s} Off {OFF[t]:3d}  Def {DEF[t]:3d}  Overall {OVR[t]:5.1f}")

# stats for conclusion
import statistics
maxps = [max(p["home_win_probability"], p["draw_probability"], p["away_win_probability"]) for p in preds]
print("\nExpected hit rate (mean max outcome prob):", round(sum(maxps)/len(maxps), 3))
exact = []
for m in range(1,73):
    r = results[m][3]; exact.append(r["M"][r["hs"]][r["as_"]])
for m in range(73,105):
    r = ko_results[m]; exact.append(r["M"][r["hs"]][r["as_"]])
print("Mean exact-score probability:", round(sum(exact)/len(exact), 3))
