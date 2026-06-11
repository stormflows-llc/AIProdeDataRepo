#!/usr/bin/env python3
"""Builds the research paper from predictions.json + model internals (wc_model)."""
import json, io, contextlib

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import wc_model as W

P = {o["match_id"]: o for o in json.load(open("predictions.json"))["predictions"]}

def winner(o):
    if o["extra_time_or_penalties_winner"] != "none":
        return o["extra_time_or_penalties_winner"]
    return o["home_team"] if o["predicted_home_score"] > o["predicted_away_score"] else o["away_team"]

def prob_str(o):
    return f"{o['home_win_probability']:.2f} / {o['draw_probability']:.2f} / {o['away_win_probability']:.2f}"

def match_row(m):
    o = P[m]
    et = ""
    if o["extra_time_or_penalties_winner"] != "none":
        et = f" → **{o['extra_time_or_penalties_winner']}** adv. (ET/pens)"
    return (f"| {m} | {o['home_team']} | **{o['predicted_home_score']}–{o['predicted_away_score']}** | "
            f"{o['away_team']} | {prob_str(o)} | {o['model_confidence']}{et} |")

HDR = "| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |\n|---|---|---|---|---|---|"

def group_section(g):
    rows = [match_row(m) for m in range(1, 73) if P[m]["group"] == g]
    st = W.standings[g]
    tline = []
    for i, t in enumerate(st):
        s = W.table[g][t]
        tline.append(f"{i+1}. {t} — {s['P']} pts (GD {s['GF']-s['GA']:+d})")
    out = [f"#### Group {g}", "", HDR] + rows + ["",
           f"**Projected table:** " + " · ".join(tline),
           f"**Advance:** {st[0]}, {st[1]}" + (f" · 3rd ({st[2]}) {'advances among best eight' if g in W.adv_groups else 'eliminated in third-place ranking'}"), ""]
    return "\n".join(out)

def ko_table(ids):
    return "\n".join([HDR] + [match_row(m) for m in ids])

grids = {}
def grid(M, ta, tb):
    mx = max(M[i][j] for i in range(4) for j in range(4))
    def ch(p):
        r = p / mx
        return "█" if r >= 0.999 else ("▓" if r >= 0.5 else ("▒" if r >= 0.2 else "░"))
    lines = [f"[{tb} Goals]"]
    for j in range(3, -1, -1):
        lines.append(f"   {j} |  " + "   ".join(ch(M[i][j]) for i in range(4)))
    lines.append("     +---------------")
    lines.append(f"        0   1   2   3  [{ta} Goals]")
    return "\n".join(lines)

g_open  = grid(W.results[1][3]["M"], "Mexico", "South Africa")
g_vol   = grid(W.results[63][3]["M"], "Uruguay", "Spain")
g_final = grid(W.ko_results[104]["M"], "Spain", "Argentina")

ratings_rows = "\n".join(
    f"| {i+1} | {t} | {W.OFF[t]} | {W.DEF[t]} | {W.OVR[t]:.1f} |"
    for i, t in enumerate(sorted(W.T, key=lambda x: -W.OVR[x])))

thirds_rows = "\n".join(
    f"| {i+1} | {t} ({g}) | {W.table[g][t]['P']} | {W.table[g][t]['GF']-W.table[g][t]['GA']:+d} | {W.table[g][t]['GF']} | "
    + ("**advances**" if i < 8 else "eliminated") + " |"
    for i, (g, t) in enumerate(sorted([(g, W.standings[g][2]) for g in W.G],
        key=lambda it: (-W.table[it[0]][it[1]]["P"],
                        -(W.table[it[0]][it[1]]["GF"]-W.table[it[0]][it[1]]["GA"]),
                        -W.table[it[0]][it[1]]["GF"], -W.OVR[it[1]]))))

import statistics
maxps = [max(o["home_win_probability"], o["draw_probability"], o["away_win_probability"]) for o in P.values()]
mean_maxp = sum(maxps) / len(maxps)
high_n = sum(1 for o in P.values() if o["model_confidence"] == "high")
med_n  = sum(1 for o in P.values() if o["model_confidence"] == "medium")
low_n  = sum(1 for o in P.values() if o["model_confidence"] == "low")

doc = f"""# Anthropic Claude — End-to-End Predictive Framework for the 2026 FIFA World Cup

**Model identification — Brand: Anthropic · Model: Claude (Claude Agent SDK, Cowork research preview build) · Generated: June 10, 2026**

## Abstract

This paper presents a fully independent, deterministic-baseline predictive framework for all 104 matches of the 2026 FIFA World Cup, built on an independent bivariate Poisson scoring engine with an exponential strength link. Per the user-calibrated interview, team strength ratings weight recent continental evidence (Euro 2024, Copa América 2024, 2025–26 Nations League and qualifying form) at 70% against historical World Cup pedigree at 30%; host advantage is tiered ($\\gamma_{{MEX}}=1.25$, $\\gamma_{{USA}}=1.15$, $\\gamma_{{CAN}}=1.10$) and decays for Mexico/Canada in knockout rounds played on U.S. soil; club-season fatigue ($\\phi$) and travel/climate friction ($\\tau$) enter as multiplicative attenuators. The model uses the official December 5, 2025 Final Draw, FIFA's published Round-of-32 allocation, and Annex C third-place combinatorics. Primary conclusions: **Spain** is the baseline champion (defeating Argentina on penalties after a 1–1 final at MetLife Stadium), France finishes third, and the expected per-match result hit rate of the baseline is ≈ 51.7%.

## 1. Methodology & Theoretical Framework

The framework is a **calibrated independent Poisson goals model**. Each team $i$ carries a decomposed rating triple — Offensive Rating $O_i$, Defensive Rating $D_i$, and Overall Strength $R_i$ on a 0–100 scale — where the overall rating implements the user's interview calibration:

$$R_i = 0.70 \\cdot R_i^{{recent}} + 0.30 \\cdot R_i^{{hist}}$$

$R_i^{{recent}}$ encodes continental-cycle evidence (Euro 2024, Copa América 2024, UEFA Nations League 2025, AFCON/Gold Cup form, and 2024–26 qualifying), anchored to the April 2026 FIFA ranking (France 1, Spain 2, Argentina 3, England 4, Portugal 5, Brazil 6); $R_i^{{hist}}$ encodes historical World Cup performance. Offensive and defensive ratings are the attack/defense decomposition of the same evidence and are the quantities consumed by the scoring engine.

**Core metrics.** The engine consumes (i) the $O_i/D_i$ decomposition above (an Elo-family strength encoding standing in for xG/xGA attack-defense splits), (ii) the tiered host coefficient $\\gamma$, (iii) a club-fatigue attenuator $\\phi_i \\in [0.980, 1.000]$ penalizing squads with the heaviest 2025–26 European club minute loads (Spain, England, France, Portugal at 0.980; minute-light squads at 1.000), and (iv) a travel/climate friction term $\\tau_i \\in [0.980, 1.000]$ reflecting that the United States hosts 78 of 104 matches: CONCACAF-based squads acclimated to summer heat and the venue footprint carry $\\tau = 1.000$, while long-haul, cool-climate squads (e.g., Australia, Japan) carry $\\tau = 0.980$.

**Host-field scaling per user input (moderate, tiered).** Group stage: $\\gamma_{{MEX}}=1.25$ (Estadio Azteca altitude at 2,240 m + crowd), $\\gamma_{{USA}}=1.15$, $\\gamma_{{CAN}}=1.10$. Because Mexico and Canada host only 13 matches each and the knockout tree migrates onto U.S. soil, the coefficient decays by round: Mexico 1.20 (R32, Mexico City) → 1.15 (R16) → 1.05 (QF onward); Canada 1.08 (R32) → 1.04 thereafter; the United States retains 1.15 throughout, including the East Rutherford final.

**Extra time and penalties.** For knockout matches the 90-minute scoreline distribution is computed first. The probability that the home side ultimately advances is

$$P_{{adv}} = P_{{win90}} + P_{{draw90}} \\cdot \\omega, \\qquad \\omega = \\frac{{P_{{win90}}}}{{P_{{win90}} + P_{{loss90}}}}$$

i.e., conditional on a level 90 minutes, advancement odds in extra time/penalties inherit the relative 90-minute dominance ratio $\\omega$ (a logistic-equivalent reduction that avoids inventing an independent shootout skill parameter). The published scoreline is the modal exact score among the union of (winner-victory cells) and (draw cells): when the tie sits inside the volatility band $|P_{{adv}} - 0.5| < 0.08$ **and** the joint modal scoreline is level, the model publishes the draw scoreline and designates the ET/penalties winner; otherwise it publishes the winner's modal victory scoreline. This produced 11 ET/penalty designations across 32 knockout matches (34%), consistent with the 2018–2022 empirical base rate.

### 1.1 Mathematical Formulation

Goal-scoring intensities use an exponential strength link with multiplicative structural adjustments:

$$\\lambda_{{H}} = \\mu \\cdot \\exp\\!\\left(\\kappa \\cdot \\frac{{O_H - D_A}}{{100}}\\right) \\cdot \\gamma_H \\cdot \\phi_H \\cdot \\tau_H$$

$$\\lambda_{{A}} = \\mu \\cdot \\exp\\!\\left(\\kappa \\cdot \\frac{{O_A - D_H}}{{100}}\\right) \\cdot \\gamma_A \\cdot \\phi_A \\cdot \\tau_A$$

with baseline intensity $\\mu = 1.28$ goals/team/match (modern World Cup average) and differential sensitivity $\\kappa = 2.3$. Goals are independent Poisson draws:

$$P(X = k) = \\frac{{\\lambda^k \\cdot e^{{-\\lambda}}}}{{k!}}, \\qquad P(i, j) = \\frac{{\\lambda_H^i e^{{-\\lambda_H}}}}{{i!}} \\cdot \\frac{{\\lambda_A^j e^{{-\\lambda_A}}}}{{j!}}$$

Outcome probabilities integrate the truncated grid ($k \\le 10$):

$$P_{{H}} = \\sum_{{i>j}} P(i,j), \\quad P_{{D}} = \\sum_{{i=j}} P(i,j), \\quad P_{{A}} = \\sum_{{i<j}} P(i,j)$$

The published exact scoreline is the conditional mode $\\arg\\max_{{(i,j) \\in \\Omega}} P(i,j)$ where $\\Omega$ is the cell-set of the predicted outcome class.

**Third-place selection (8 of 12).** Group tables are scored deterministically from modal results (3/1/0 points). Third-placed teams are ranked by the lexicographic differential vector

$$\\succ \\; := \\; \\left(Pts, \\; GD, \\; GF, \\; R_i\\right)$$

i.e., points, then goal difference, then goals for, with the overall strength rating $R_i$ standing in for FIFA's conduct/ranking tiebreakers. The top eight advance. In this baseline, all twelve thirds finish on 3 points, so the probability-differential tiebreak chain decides: the advancing set is **{{A, C, D, E, F, G, I, J}}** (Czechia, Scotland, Paraguay, Ivory Coast, Sweden, Iran, Senegal, Algeria), which maps to **Annex C combination row 281**, fixing the bracket slots 1A→3C, 1B→3G, 1D→3J, 1E→3D, 1G→3A, 1I→3F, 1K→3E, 1L→3I.

## 2. Global Team Strength Assessment (Scoring Matrix)

Relative Strength Ratings for all 48 qualified teams (0–100; Overall $= 0.7R^{{recent}} + 0.3R^{{hist}}$):

| Rank | Team | Offensive Rating | Defensive Rating | Overall Strength |
|---|---|---|---|---|
{ratings_rows}

## 3. Full Tournament Predictions & Bracket Breakdown

**Tactical synthesis.** The draw concentrates risk asymmetrically. The top half of the bracket forces a Germany–France collision as early as the Round of 16 (a consequence of 1E and 1I feeding Match 89 via Matches 74/77) and funnels Brazil, England and host Mexico into the same quarter. The bottom half hands Spain a comparatively soft corridor (Austria, then the Croatia/Colombia survivor, then Belgium) while Argentina must clear a heavyweight Uruguay reunion in the Round of 32 and Portugal in the quarterfinals. Host effects materially shape Groups A, B and D: Mexico's $\\gamma=1.25$ converts a mid-tier roster into a comfortable group winner; the United States edges a stronger-on-paper Türkiye side to win Group D 2–1 in the Matchday 3 head-to-head. Switzerland's defensive profile outlasts Canada's host bump in Group B on the same logic in reverse — the Matchday 3 fixture is played in Vancouver, but Switzerland's superior baseline carries a 1–0 modal result.

Match identifiers are chronological (1–72 group stage per the official June 11–27 matchday calendar; 73–104 knockout per FIFA's published bracket numbering).

### 3.1 Group Stage (Groups A through L)

{chr(10).join(group_section(g) for g in "ABCDEFGHIJKL")}

**Third-place ranking (best eight advance):**

| Rank | Team (Group) | Pts | GD | GF | Status |
|---|---|---|---|---|---|
{thirds_rows}

### 3.2 Round of 32

Slot allocation follows FIFA's fixed R32 template with Annex C row 281 resolving the third-place feeds.

{ko_table(range(73, 89))}

**Advancing to the Round of 16:** Canada, Germany, Netherlands, Brazil, France, Norway, Mexico, England, United States, Belgium, Croatia, Spain, Switzerland, Argentina, Portugal, Türkiye.

The volatility cluster sits in Matches 73, 75, 78, 83 and 88, where $|P_{{adv}}-0.5|<0.08$: Canada–South Korea and Croatia–Colombia are statistical coin flips resolved only by the $\\omega$ dominance ratio in the shootout reduction.

### 3.3 Round of 16

{ko_table(range(89, 97))}

The headline is Match 89: **Germany–France**, the earliest top-four collision the bracket permits. France's superior two-way rating (93/93 vs 87/84) overcomes Germany's marginally better group-stage seeding; the model resolves it 1–0 to France in 90 minutes ($P_{{adv}}^{{FRA}} = 0.64$). England ends Mexico's run as the host's $\\gamma$ decays to 1.15 and the rating gap (89.8 vs 77.9) reasserts itself. Belgium survives the United States in the bracket's tightest R16 tie ($P_{{adv}}^{{BEL}} = 0.53$), on penalties.

### 3.4 Quarterfinals & Semifinals

**Quarterfinals**

{ko_table(range(97, 101))}

**Semifinals**

{ko_table([101, 102])}

England–Brazil (Match 99) is the tournament's marquee volatility event: a 1–1 deadlock resolved by England's defensive edge (91 vs 87) in the shootout reduction, $P_{{adv}}^{{ENG}} = 0.53$. Both semifinals sit deep inside the volatility band — France–Spain at $P_{{adv}}^{{ESP}} = 0.52$ and England–Argentina at $P_{{adv}}^{{ARG}} = 0.54$ — and both are published as 1–1 with extra-time/penalty resolutions, reflecting the elite defensive parity at this depth of the bracket.

### 3.5 Third-Place Playoff & Grand Final

{ko_table([103, 104])}

**Match 103 (Miami):** France defeats England on penalties after 1–1 to take bronze.

**Match 104 — Grand Final, MetLife Stadium, East Rutherford, July 19, 2026:** the model's *a priori* champion is **SPAIN**, surviving Argentina on penalties after a 1–1 final ($P_{{adv}}^{{ESP}} = 0.53$). Spain's championship path: top Group H with a +5 differential, Austria (1–0), Croatia (1–0), Belgium (1–0), France (1–1, pens), Argentina (1–1, pens). The verdict rests on the tournament's highest overall rating (93.9), the strongest attack rating (95), and a recent-cycle weighting (70%) that fully credits the Euro 2024 title and 2025–26 Nations League form, while Argentina's path is taxed by the bracket's harder bottom-right quadrant (Uruguay, Portugal) before the final.

## 4. Technical Appendix & Probability Distributions

Probability Density Matrices (`░ < 20% · ▒ ≥ 20% · ▓ ≥ 50% · █ = mode`, scaled to the cell maximum; axes truncated at 3 goals).

**1. Opening Match (Match 1, Estadio Azteca): Mexico vs. South Africa** — $\\lambda_{{MEX}} = 1.92$, $\\lambda_{{RSA}} = 0.98$. Mode at (1, 0); the $\\gamma = 1.25$ altitude coefficient lifts Mexico's probability of scoring at least twice to 57%.

```text
{g_open}
```

**2. High-Volatility Group Match (Match 63, Matchday 3, Group H): Uruguay vs. Spain** — $\\lambda_{{URU}} = 0.94$, $\\lambda_{{ESP}} = 1.59$. Mode at (0, 1) but with heavy ridge mass along the diagonal and the (1, 2) corridor: Uruguay's elite defensive rating (84) compresses Spain's edge into the single-goal bands, making this the group stage's premier upset/draw hedge.

```text
{g_vol}
```

**3. Predicted Grand Final (Match 104): Spain vs. Argentina** — $\\lambda_{{ESP}} = 1.32$, $\\lambda_{{ARG}} = 1.23$. The joint mode is (1, 1) — the rare fixture whose most probable exact scoreline is the draw itself, which is precisely why the model publishes 1–1 with a penalty resolution rather than forcing a 90-minute verdict.

```text
{g_final}
```

## 5. Conclusion & Baseline Strategy

Across all 104 fixtures the mean probability of the model's chosen outcome class is **{mean_maxp:.3f}** — a standard user following this sheet should expect to call ≈ **52% of results correctly** (≈ 54 of 104), with exact scorelines landing at ≈ **12%** (≈ 12–13 matches), figures consistent with the irreducible variance of tournament football. Confidence distribution: **{high_n} high / {med_n} medium / {low_n} low**.

**Highest-confidence anchors (play straight):** Spain–Cape Verde (0.79), France–Iraq (0.75), Brazil–Haiti (0.75), Argentina over Jordan (0.76), England over Panama (0.72), Germany–Curaçao (0.71), plus France over Sweden ($P_{{adv}} = 0.82$) and Spain over Austria (0.79) in the Round of 32.

**Maximum-volatility fixtures (hedge):** South Korea–Czechia (0.39/0.26/0.35 — near-uniform), DR Congo–Uzbekistan, Paraguay–Australia and Egypt–Iran in the group stage; Canada–South Korea ($P_{{adv}} = 0.53$), Croatia–Colombia (0.51), Türkiye–Egypt (0.53) in the Round of 32; and every match from the quarterfinals onward except Spain–Belgium — the title odds separating Spain, Argentina and France are thinner than a single penalty kick. Users should treat the champion call as a 53/47 edge, not a certainty, and diversify bracket exposure across Spain, Argentina and France accordingly.

---

*Generated by Anthropic Claude. Deterministic baseline: modal outcomes propagated as ground truth per the tournament-rules mandate; probabilities are exact Poisson-grid integrals, not Monte Carlo estimates. Companion machine-readable dataset: `predictions.json` (104 records, schema-validated).*
"""

open("worldcup2026_prediction_paper.md", "w").write(doc)
print("written", len(doc), "chars")
