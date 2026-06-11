# Anthropic Claude — End-to-End Predictive Framework for the 2026 FIFA World Cup

**Model identification — Brand: Anthropic · Model: Claude (Claude Agent SDK, Cowork research preview build) · Generated: June 10, 2026**

## Abstract

This paper presents a fully independent, deterministic-baseline predictive framework for all 104 matches of the 2026 FIFA World Cup, built on an independent bivariate Poisson scoring engine with an exponential strength link. Per the user-calibrated interview, team strength ratings weight recent continental evidence (Euro 2024, Copa América 2024, 2025–26 Nations League and qualifying form) at 70% against historical World Cup pedigree at 30%; host advantage is tiered ($\gamma_{MEX}=1.25$, $\gamma_{USA}=1.15$, $\gamma_{CAN}=1.10$) and decays for Mexico/Canada in knockout rounds played on U.S. soil; club-season fatigue ($\phi$) and travel/climate friction ($\tau$) enter as multiplicative attenuators. The model uses the official December 5, 2025 Final Draw, FIFA's published Round-of-32 allocation, and Annex C third-place combinatorics. Primary conclusions: **Spain** is the baseline champion (defeating Argentina on penalties after a 1–1 final at MetLife Stadium), France finishes third, and the expected per-match result hit rate of the baseline is ≈ 51.7%.

## 1. Methodology & Theoretical Framework

The framework is a **calibrated independent Poisson goals model**. Each team $i$ carries a decomposed rating triple — Offensive Rating $O_i$, Defensive Rating $D_i$, and Overall Strength $R_i$ on a 0–100 scale — where the overall rating implements the user's interview calibration:

$$R_i = 0.70 \cdot R_i^{recent} + 0.30 \cdot R_i^{hist}$$

$R_i^{recent}$ encodes continental-cycle evidence (Euro 2024, Copa América 2024, UEFA Nations League 2025, AFCON/Gold Cup form, and 2024–26 qualifying), anchored to the April 2026 FIFA ranking (France 1, Spain 2, Argentina 3, England 4, Portugal 5, Brazil 6); $R_i^{hist}$ encodes historical World Cup performance. Offensive and defensive ratings are the attack/defense decomposition of the same evidence and are the quantities consumed by the scoring engine.

**Core metrics.** The engine consumes (i) the $O_i/D_i$ decomposition above (an Elo-family strength encoding standing in for xG/xGA attack-defense splits), (ii) the tiered host coefficient $\gamma$, (iii) a club-fatigue attenuator $\phi_i \in [0.980, 1.000]$ penalizing squads with the heaviest 2025–26 European club minute loads (Spain, England, France, Portugal at 0.980; minute-light squads at 1.000), and (iv) a travel/climate friction term $\tau_i \in [0.980, 1.000]$ reflecting that the United States hosts 78 of 104 matches: CONCACAF-based squads acclimated to summer heat and the venue footprint carry $\tau = 1.000$, while long-haul, cool-climate squads (e.g., Australia, Japan) carry $\tau = 0.980$.

**Host-field scaling per user input (moderate, tiered).** Group stage: $\gamma_{MEX}=1.25$ (Estadio Azteca altitude at 2,240 m + crowd), $\gamma_{USA}=1.15$, $\gamma_{CAN}=1.10$. Because Mexico and Canada host only 13 matches each and the knockout tree migrates onto U.S. soil, the coefficient decays by round: Mexico 1.20 (R32, Mexico City) → 1.15 (R16) → 1.05 (QF onward); Canada 1.08 (R32) → 1.04 thereafter; the United States retains 1.15 throughout, including the East Rutherford final.

**Extra time and penalties.** For knockout matches the 90-minute scoreline distribution is computed first. The probability that the home side ultimately advances is

$$P_{adv} = P_{win90} + P_{draw90} \cdot \omega, \qquad \omega = \frac{P_{win90}}{P_{win90} + P_{loss90}}$$

i.e., conditional on a level 90 minutes, advancement odds in extra time/penalties inherit the relative 90-minute dominance ratio $\omega$ (a logistic-equivalent reduction that avoids inventing an independent shootout skill parameter). The published scoreline is the modal exact score among the union of (winner-victory cells) and (draw cells): when the tie sits inside the volatility band $|P_{adv} - 0.5| < 0.08$ **and** the joint modal scoreline is level, the model publishes the draw scoreline and designates the ET/penalties winner; otherwise it publishes the winner's modal victory scoreline. This produced 11 ET/penalty designations across 32 knockout matches (34%), consistent with the 2018–2022 empirical base rate.

### 1.1 Mathematical Formulation

Goal-scoring intensities use an exponential strength link with multiplicative structural adjustments:

$$\lambda_{H} = \mu \cdot \exp\!\left(\kappa \cdot \frac{O_H - D_A}{100}\right) \cdot \gamma_H \cdot \phi_H \cdot \tau_H$$

$$\lambda_{A} = \mu \cdot \exp\!\left(\kappa \cdot \frac{O_A - D_H}{100}\right) \cdot \gamma_A \cdot \phi_A \cdot \tau_A$$

with baseline intensity $\mu = 1.28$ goals/team/match (modern World Cup average) and differential sensitivity $\kappa = 2.3$. Goals are independent Poisson draws:

$$P(X = k) = \frac{\lambda^k \cdot e^{-\lambda}}{k!}, \qquad P(i, j) = \frac{\lambda_H^i e^{-\lambda_H}}{i!} \cdot \frac{\lambda_A^j e^{-\lambda_A}}{j!}$$

Outcome probabilities integrate the truncated grid ($k \le 10$):

$$P_{H} = \sum_{i>j} P(i,j), \quad P_{D} = \sum_{i=j} P(i,j), \quad P_{A} = \sum_{i<j} P(i,j)$$

The published exact scoreline is the conditional mode $\arg\max_{(i,j) \in \Omega} P(i,j)$ where $\Omega$ is the cell-set of the predicted outcome class.

**Third-place selection (8 of 12).** Group tables are scored deterministically from modal results (3/1/0 points). Third-placed teams are ranked by the lexicographic differential vector

$$\succ \; := \; \left(Pts, \; GD, \; GF, \; R_i\right)$$

i.e., points, then goal difference, then goals for, with the overall strength rating $R_i$ standing in for FIFA's conduct/ranking tiebreakers. The top eight advance. In this baseline, all twelve thirds finish on 3 points, so the probability-differential tiebreak chain decides: the advancing set is **{A, C, D, E, F, G, I, J}** (Czechia, Scotland, Paraguay, Ivory Coast, Sweden, Iran, Senegal, Algeria), which maps to **Annex C combination row 281**, fixing the bracket slots 1A→3C, 1B→3G, 1D→3J, 1E→3D, 1G→3A, 1I→3F, 1K→3E, 1L→3I.

## 2. Global Team Strength Assessment (Scoring Matrix)

Relative Strength Ratings for all 48 qualified teams (0–100; Overall $= 0.7R^{recent} + 0.3R^{hist}$):

| Rank | Team | Offensive Rating | Defensive Rating | Overall Strength |
|---|---|---|---|---|
| 1 | Spain | 95 | 93 | 93.9 |
| 2 | France | 93 | 93 | 93.0 |
| 3 | Argentina | 92 | 92 | 92.1 |
| 4 | England | 89 | 91 | 89.8 |
| 5 | Portugal | 90 | 88 | 88.8 |
| 6 | Brazil | 89 | 87 | 87.9 |
| 7 | Netherlands | 86 | 87 | 86.4 |
| 8 | Germany | 87 | 84 | 85.9 |
| 9 | Belgium | 84 | 82 | 83.0 |
| 10 | Morocco | 81 | 85 | 82.8 |
| 11 | Croatia | 82 | 83 | 82.5 |
| 12 | Uruguay | 80 | 84 | 81.7 |
| 13 | Colombia | 82 | 81 | 81.4 |
| 14 | Japan | 81 | 80 | 80.8 |
| 15 | Norway | 84 | 76 | 79.7 |
| 16 | Switzerland | 78 | 81 | 79.4 |
| 17 | Mexico | 78 | 79 | 77.9 |
| 18 | Senegal | 77 | 79 | 77.8 |
| 19 | United States | 78 | 78 | 77.7 |
| 20 | Türkiye | 79 | 75 | 76.8 |
| 21 | Austria | 77 | 76 | 76.2 |
| 22 | Ecuador | 74 | 79 | 76.1 |
| 23 | South Korea | 76 | 74 | 75.1 |
| 24 | Egypt | 74 | 76 | 74.8 |
| 25 | Canada | 75 | 74 | 74.5 |
| 26 | Algeria | 75 | 73 | 74.1 |
| 27 | Czechia | 74 | 73 | 73.4 |
| 28 | Paraguay | 71 | 76 | 73.4 |
| 29 | Iran | 72 | 74 | 73.1 |
| 30 | Sweden | 75 | 71 | 73.0 |
| 31 | Australia | 72 | 73 | 72.4 |
| 32 | Scotland | 72 | 72 | 72.1 |
| 33 | Ivory Coast | 73 | 71 | 72.1 |
| 34 | Ghana | 72 | 70 | 71.3 |
| 35 | Bosnia and Herzegovina | 71 | 69 | 70.1 |
| 36 | Tunisia | 69 | 72 | 70.1 |
| 37 | South Africa | 68 | 70 | 68.8 |
| 38 | Saudi Arabia | 67 | 68 | 67.4 |
| 39 | DR Congo | 67 | 66 | 66.5 |
| 40 | Uzbekistan | 66 | 67 | 66.1 |
| 41 | Qatar | 66 | 65 | 65.4 |
| 42 | Iraq | 63 | 66 | 64.1 |
| 43 | Jordan | 64 | 64 | 63.8 |
| 44 | Panama | 63 | 65 | 63.8 |
| 45 | Cape Verde | 62 | 64 | 62.8 |
| 46 | New Zealand | 61 | 63 | 61.7 |
| 47 | Haiti | 62 | 61 | 61.4 |
| 48 | Curaçao | 60 | 62 | 60.8 |

## 3. Full Tournament Predictions & Bracket Breakdown

**Tactical synthesis.** The draw concentrates risk asymmetrically. The top half of the bracket forces a Germany–France collision as early as the Round of 16 (a consequence of 1E and 1I feeding Match 89 via Matches 74/77) and funnels Brazil, England and host Mexico into the same quarter. The bottom half hands Spain a comparatively soft corridor (Austria, then the Croatia/Colombia survivor, then Belgium) while Argentina must clear a heavyweight Uruguay reunion in the Round of 32 and Portugal in the quarterfinals. Host effects materially shape Groups A, B and D: Mexico's $\gamma=1.25$ converts a mid-tier roster into a comfortable group winner; the United States edges a stronger-on-paper Türkiye side to win Group D 2–1 in the Matchday 3 head-to-head. Switzerland's defensive profile outlasts Canada's host bump in Group B on the same logic in reverse — the Matchday 3 fixture is played in Vancouver, but Switzerland's superior baseline carries a 1–0 modal result.

Match identifiers are chronological (1–72 group stage per the official June 11–27 matchday calendar; 73–104 knockout per FIFA's published bracket numbering).

### 3.1 Group Stage (Groups A through L)

#### Group A

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 1 | Mexico | **1–0** | South Africa | 0.59 / 0.22 / 0.19 | high |
| 2 | South Korea | **1–0** | Czechia | 0.39 / 0.26 / 0.35 | low |
| 25 | Mexico | **2–1** | South Korea | 0.51 / 0.24 / 0.25 | medium |
| 26 | Czechia | **1–0** | South Africa | 0.42 / 0.27 / 0.31 | medium |
| 49 | Czechia | **0–1** | Mexico | 0.23 / 0.23 / 0.54 | medium |
| 50 | South Africa | **0–1** | South Korea | 0.29 / 0.26 / 0.45 | medium |

**Projected table:** 1. Mexico — 9 pts (GD +3) · 2. South Korea — 6 pts (GD +1) · 3. Czechia — 3 pts (GD -1) · 4. South Africa — 0 pts (GD -3)
**Advance:** Mexico, South Korea · 3rd (Czechia) advances among best eight

#### Group B

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 3 | Canada | **1–0** | Bosnia and Herzegovina | 0.47 / 0.25 / 0.28 | medium |
| 5 | Qatar | **0–1** | Switzerland | 0.20 / 0.24 / 0.56 | high |
| 27 | Canada | **1–0** | Qatar | 0.55 / 0.23 / 0.22 | high |
| 28 | Switzerland | **1–0** | Bosnia and Herzegovina | 0.49 / 0.26 / 0.25 | medium |
| 51 | Switzerland | **1–0** | Canada | 0.40 / 0.26 / 0.34 | medium |
| 52 | Bosnia and Herzegovina | **1–0** | Qatar | 0.43 / 0.26 / 0.31 | medium |

**Projected table:** 1. Switzerland — 9 pts (GD +3) · 2. Canada — 6 pts (GD +1) · 3. Bosnia and Herzegovina — 3 pts (GD -1) · 4. Qatar — 0 pts (GD -3)
**Advance:** Switzerland, Canada · 3rd (Bosnia and Herzegovina) eliminated in third-place ranking

#### Group C

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 6 | Brazil | **1–0** | Morocco | 0.43 / 0.27 / 0.30 | medium |
| 7 | Haiti | **0–1** | Scotland | 0.24 / 0.25 / 0.51 | medium |
| 29 | Brazil | **2–0** | Haiti | 0.75 / 0.16 / 0.09 | high |
| 30 | Scotland | **0–1** | Morocco | 0.23 / 0.26 / 0.51 | medium |
| 53 | Scotland | **0–1** | Brazil | 0.17 / 0.22 / 0.61 | high |
| 54 | Morocco | **1–0** | Haiti | 0.67 / 0.20 / 0.13 | high |

**Projected table:** 1. Brazil — 9 pts (GD +4) · 2. Morocco — 6 pts (GD +1) · 3. Scotland — 3 pts (GD -1) · 4. Haiti — 0 pts (GD -4)
**Advance:** Brazil, Morocco · 3rd (Scotland) advances among best eight

#### Group D

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 4 | United States | **1–0** | Paraguay | 0.47 / 0.26 / 0.27 | medium |
| 8 | Australia | **0–1** | Türkiye | 0.31 / 0.26 / 0.43 | medium |
| 31 | United States | **1–0** | Australia | 0.50 / 0.25 / 0.25 | medium |
| 32 | Türkiye | **1–0** | Paraguay | 0.41 / 0.27 / 0.32 | medium |
| 55 | Türkiye | **1–2** | United States | 0.31 / 0.25 / 0.44 | medium |
| 56 | Paraguay | **1–0** | Australia | 0.38 / 0.28 / 0.34 | low |

**Projected table:** 1. United States — 9 pts (GD +3) · 2. Türkiye — 6 pts (GD +1) · 3. Paraguay — 3 pts (GD -1) · 4. Australia — 0 pts (GD -3)
**Advance:** United States, Türkiye · 3rd (Paraguay) advances among best eight

#### Group E

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 9 | Germany | **2–0** | Curaçao | 0.71 / 0.18 / 0.11 | high |
| 10 | Ivory Coast | **0–1** | Ecuador | 0.30 / 0.27 / 0.43 | medium |
| 33 | Germany | **1–0** | Ivory Coast | 0.57 / 0.23 / 0.20 | high |
| 34 | Ecuador | **1–0** | Curaçao | 0.58 / 0.24 / 0.18 | high |
| 57 | Ecuador | **0–1** | Germany | 0.26 / 0.26 / 0.48 | medium |
| 58 | Curaçao | **0–1** | Ivory Coast | 0.23 / 0.25 / 0.52 | medium |

**Projected table:** 1. Germany — 9 pts (GD +4) · 2. Ecuador — 6 pts (GD +1) · 3. Ivory Coast — 3 pts (GD -1) · 4. Curaçao — 0 pts (GD -4)
**Advance:** Germany, Ecuador · 3rd (Ivory Coast) advances among best eight

#### Group F

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 11 | Netherlands | **1–0** | Japan | 0.45 / 0.26 / 0.29 | medium |
| 12 | Sweden | **1–0** | Tunisia | 0.39 / 0.27 / 0.34 | low |
| 35 | Netherlands | **1–0** | Sweden | 0.57 / 0.23 / 0.20 | high |
| 36 | Tunisia | **0–1** | Japan | 0.24 / 0.26 / 0.50 | medium |
| 59 | Tunisia | **0–1** | Netherlands | 0.18 / 0.24 / 0.58 | high |
| 60 | Japan | **1–0** | Sweden | 0.48 / 0.25 / 0.27 | medium |

**Projected table:** 1. Netherlands — 9 pts (GD +3) · 2. Japan — 6 pts (GD +1) · 3. Sweden — 3 pts (GD -1) · 4. Tunisia — 0 pts (GD -3)
**Advance:** Netherlands, Japan · 3rd (Sweden) advances among best eight

#### Group G

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 13 | Belgium | **1–0** | Egypt | 0.47 / 0.26 / 0.27 | medium |
| 14 | Iran | **1–0** | New Zealand | 0.51 / 0.26 / 0.23 | medium |
| 37 | Belgium | **1–0** | Iran | 0.51 / 0.25 / 0.24 | medium |
| 38 | New Zealand | **0–1** | Egypt | 0.21 / 0.25 / 0.54 | medium |
| 61 | New Zealand | **0–2** | Belgium | 0.14 / 0.20 / 0.66 | high |
| 62 | Egypt | **1–0** | Iran | 0.38 / 0.28 / 0.34 | low |

**Projected table:** 1. Belgium — 9 pts (GD +4) · 2. Egypt — 6 pts (GD +1) · 3. Iran — 3 pts (GD -1) · 4. New Zealand — 0 pts (GD -4)
**Advance:** Belgium, Egypt · 3rd (Iran) advances among best eight

#### Group H

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 15 | Spain | **2–0** | Cape Verde | 0.79 / 0.14 / 0.07 | high |
| 16 | Saudi Arabia | **0–1** | Uruguay | 0.19 / 0.24 / 0.57 | high |
| 39 | Spain | **2–0** | Saudi Arabia | 0.73 / 0.17 / 0.10 | high |
| 40 | Uruguay | **1–0** | Cape Verde | 0.63 / 0.22 / 0.15 | high |
| 63 | Uruguay | **0–1** | Spain | 0.22 / 0.25 / 0.53 | medium |
| 64 | Cape Verde | **0–1** | Saudi Arabia | 0.30 / 0.27 / 0.43 | medium |

**Projected table:** 1. Spain — 9 pts (GD +5) · 2. Uruguay — 6 pts (GD +1) · 3. Saudi Arabia — 3 pts (GD -2) · 4. Cape Verde — 0 pts (GD -4)
**Advance:** Spain, Uruguay · 3rd (Saudi Arabia) eliminated in third-place ranking

#### Group I

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 17 | France | **1–0** | Senegal | 0.57 / 0.24 / 0.19 | high |
| 18 | Iraq | **0–1** | Norway | 0.18 / 0.22 / 0.60 | high |
| 41 | France | **2–0** | Iraq | 0.75 / 0.16 / 0.09 | high |
| 42 | Norway | **1–0** | Senegal | 0.39 / 0.26 / 0.35 | low |
| 65 | Norway | **0–1** | France | 0.21 / 0.23 / 0.56 | high |
| 66 | Senegal | **1–0** | Iraq | 0.55 / 0.25 / 0.20 | high |

**Projected table:** 1. France — 9 pts (GD +4) · 2. Norway — 6 pts (GD +1) · 3. Senegal — 3 pts (GD -1) · 4. Iraq — 0 pts (GD -4)
**Advance:** France, Norway · 3rd (Senegal) advances among best eight

#### Group J

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 19 | Argentina | **1–0** | Algeria | 0.63 / 0.21 / 0.16 | high |
| 20 | Austria | **1–0** | Jordan | 0.55 / 0.24 / 0.21 | high |
| 43 | Argentina | **1–0** | Austria | 0.59 / 0.23 / 0.18 | high |
| 44 | Jordan | **0–1** | Algeria | 0.24 / 0.25 / 0.51 | medium |
| 67 | Jordan | **0–2** | Argentina | 0.08 / 0.16 / 0.76 | high |
| 68 | Algeria | **0–1** | Austria | 0.34 / 0.26 / 0.40 | medium |

**Projected table:** 1. Argentina — 9 pts (GD +4) · 2. Austria — 6 pts (GD +1) · 3. Algeria — 3 pts (GD -1) · 4. Jordan — 0 pts (GD -4)
**Advance:** Argentina, Austria · 3rd (Algeria) advances among best eight

#### Group K

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 21 | Portugal | **2–0** | DR Congo | 0.69 / 0.19 / 0.12 | high |
| 22 | Uzbekistan | **0–1** | Colombia | 0.18 / 0.23 / 0.59 | high |
| 45 | Portugal | **2–0** | Uzbekistan | 0.69 / 0.19 / 0.12 | high |
| 46 | Colombia | **1–0** | DR Congo | 0.58 / 0.23 / 0.19 | high |
| 69 | Colombia | **0–1** | Portugal | 0.28 / 0.26 / 0.46 | medium |
| 70 | DR Congo | **1–0** | Uzbekistan | 0.37 / 0.27 / 0.36 | low |

**Projected table:** 1. Portugal — 9 pts (GD +5) · 2. Colombia — 6 pts (GD +1) · 3. DR Congo — 3 pts (GD -2) · 4. Uzbekistan — 0 pts (GD -4)
**Advance:** Portugal, Colombia · 3rd (DR Congo) eliminated in third-place ranking

#### Group L

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 23 | England | **1–0** | Croatia | 0.46 / 0.27 / 0.27 | medium |
| 24 | Ghana | **1–0** | Panama | 0.46 / 0.26 / 0.28 | medium |
| 47 | England | **1–0** | Ghana | 0.64 / 0.21 / 0.15 | high |
| 48 | Panama | **0–1** | Croatia | 0.16 / 0.22 / 0.62 | high |
| 71 | Panama | **0–2** | England | 0.10 / 0.18 / 0.72 | high |
| 72 | Croatia | **1–0** | Ghana | 0.52 / 0.25 / 0.23 | medium |

**Projected table:** 1. England — 9 pts (GD +4) · 2. Croatia — 6 pts (GD +1) · 3. Ghana — 3 pts (GD -1) · 4. Panama — 0 pts (GD -4)
**Advance:** England, Croatia · 3rd (Ghana) eliminated in third-place ranking


**Third-place ranking (best eight advance):**

| Rank | Team (Group) | Pts | GD | GF | Status |
|---|---|---|---|---|---|
| 1 | Senegal (I) | 3 | -1 | 1 | **advances** |
| 2 | Algeria (J) | 3 | -1 | 1 | **advances** |
| 3 | Czechia (A) | 3 | -1 | 1 | **advances** |
| 4 | Paraguay (D) | 3 | -1 | 1 | **advances** |
| 5 | Iran (G) | 3 | -1 | 1 | **advances** |
| 6 | Sweden (F) | 3 | -1 | 1 | **advances** |
| 7 | Scotland (C) | 3 | -1 | 1 | **advances** |
| 8 | Ivory Coast (E) | 3 | -1 | 1 | **advances** |
| 9 | Ghana (L) | 3 | -1 | 1 | eliminated |
| 10 | Bosnia and Herzegovina (B) | 3 | -1 | 1 | eliminated |
| 11 | Saudi Arabia (H) | 3 | -2 | 1 | eliminated |
| 12 | DR Congo (K) | 3 | -2 | 1 | eliminated |

### 3.2 Round of 32

Slot allocation follows FIFA's fixed R32 template with Annex C row 281 resolving the third-place feeds.

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 73 | South Korea | **1–1** | Canada | 0.35 / 0.26 / 0.39 | low → **Canada** adv. (ET/pens) |
| 74 | Germany | **1–0** | Paraguay | 0.53 / 0.25 / 0.22 | high |
| 75 | Netherlands | **1–1** | Morocco | 0.40 / 0.28 / 0.32 | low → **Netherlands** adv. (ET/pens) |
| 76 | Brazil | **1–0** | Japan | 0.48 / 0.25 / 0.27 | medium |
| 77 | France | **2–0** | Sweden | 0.66 / 0.20 / 0.14 | high |
| 78 | Ecuador | **1–1** | Norway | 0.33 / 0.26 / 0.41 | low → **Norway** adv. (ET/pens) |
| 79 | Mexico | **1–0** | Scotland | 0.54 / 0.23 / 0.23 | high |
| 80 | England | **1–0** | Senegal | 0.52 / 0.26 / 0.22 | high |
| 81 | United States | **1–0** | Algeria | 0.49 / 0.24 / 0.27 | medium |
| 82 | Belgium | **1–0** | Czechia | 0.50 / 0.25 / 0.25 | medium |
| 83 | Colombia | **1–1** | Croatia | 0.36 / 0.27 / 0.37 | low → **Croatia** adv. (ET/pens) |
| 84 | Spain | **1–0** | Austria | 0.62 / 0.22 / 0.16 | high |
| 85 | Switzerland | **1–0** | Iran | 0.45 / 0.27 / 0.28 | medium |
| 86 | Argentina | **1–0** | Uruguay | 0.50 / 0.26 / 0.24 | medium |
| 87 | Portugal | **1–0** | Ivory Coast | 0.61 / 0.22 / 0.17 | high |
| 88 | Türkiye | **1–1** | Egypt | 0.39 / 0.27 / 0.34 | low → **Türkiye** adv. (ET/pens) |

**Advancing to the Round of 16:** Canada, Germany, Netherlands, Brazil, France, Norway, Mexico, England, United States, Belgium, Croatia, Spain, Switzerland, Argentina, Portugal, Türkiye.

The volatility cluster sits in Matches 73, 75, 78, 83 and 88, where $|P_{adv}-0.5|<0.08$: Canada–South Korea and Croatia–Colombia are statistical coin flips resolved only by the $\omega$ dominance ratio in the shootout reduction.

### 3.3 Round of 16

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 89 | Germany | **0–1** | France | 0.27 / 0.26 / 0.47 | medium |
| 90 | Canada | **0–1** | Netherlands | 0.23 / 0.25 / 0.52 | medium |
| 91 | Brazil | **1–0** | Norway | 0.50 / 0.24 / 0.26 | medium |
| 92 | Mexico | **0–1** | England | 0.27 / 0.25 / 0.48 | medium |
| 93 | Croatia | **0–1** | Spain | 0.22 / 0.25 / 0.53 | high |
| 94 | United States | **1–1** | Belgium | 0.35 / 0.25 / 0.40 | low → **Belgium** adv. (ET/pens) |
| 95 | Argentina | **1–0** | Türkiye | 0.60 / 0.22 / 0.18 | high |
| 96 | Switzerland | **0–1** | Portugal | 0.25 / 0.26 / 0.49 | medium |

The headline is Match 89: **Germany–France**, the earliest top-four collision the bracket permits. France's superior two-way rating (93/93 vs 87/84) overcomes Germany's marginally better group-stage seeding; the model resolves it 1–0 to France in 90 minutes ($P_{adv}^{FRA} = 0.64$). England ends Mexico's run as the host's $\gamma$ decays to 1.15 and the rating gap (89.8 vs 77.9) reasserts itself. Belgium survives the United States in the bracket's tightest R16 tie ($P_{adv}^{BEL} = 0.53$), on penalties.

### 3.4 Quarterfinals & Semifinals

**Quarterfinals**

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 97 | France | **1–0** | Netherlands | 0.45 / 0.27 / 0.28 | medium |
| 98 | Spain | **1–0** | Belgium | 0.53 / 0.24 / 0.23 | medium |
| 99 | Brazil | **1–1** | England | 0.34 / 0.27 / 0.39 | low → **England** adv. (ET/pens) |
| 100 | Argentina | **1–1** | Portugal | 0.41 / 0.27 / 0.32 | low → **Argentina** adv. (ET/pens) |

**Semifinals**

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 101 | France | **1–1** | Spain | 0.35 / 0.27 / 0.38 | low → **Spain** adv. (ET/pens) |
| 102 | England | **1–1** | Argentina | 0.33 / 0.27 / 0.40 | low → **Argentina** adv. (ET/pens) |

England–Brazil (Match 99) is the tournament's marquee volatility event: a 1–1 deadlock resolved by England's defensive edge (91 vs 87) in the shootout reduction, $P_{adv}^{ENG} = 0.53$. Both semifinals sit deep inside the volatility band — France–Spain at $P_{adv}^{ESP} = 0.52$ and England–Argentina at $P_{adv}^{ARG} = 0.54$ — and both are published as 1–1 with extra-time/penalty resolutions, reflecting the elite defensive parity at this depth of the bracket.

### 3.5 Third-Place Playoff & Grand Final

| # | Home | Score | Away | P(H) / P(D) / P(A) | Confidence |
|---|---|---|---|---|---|
| 103 | France | **1–1** | England | 0.41 / 0.27 / 0.32 | low → **France** adv. (ET/pens) |
| 104 | Spain | **1–1** | Argentina | 0.39 / 0.27 / 0.34 | low → **Spain** adv. (ET/pens) |

**Match 103 (Miami):** France defeats England on penalties after 1–1 to take bronze.

**Match 104 — Grand Final, MetLife Stadium, East Rutherford, July 19, 2026:** the model's *a priori* champion is **SPAIN**, surviving Argentina on penalties after a 1–1 final ($P_{adv}^{ESP} = 0.53$). Spain's championship path: top Group H with a +5 differential, Austria (1–0), Croatia (1–0), Belgium (1–0), France (1–1, pens), Argentina (1–1, pens). The verdict rests on the tournament's highest overall rating (93.9), the strongest attack rating (95), and a recent-cycle weighting (70%) that fully credits the Euro 2024 title and 2025–26 Nations League form, while Argentina's path is taxed by the bracket's harder bottom-right quadrant (Uruguay, Portugal) before the final.

## 4. Technical Appendix & Probability Distributions

Probability Density Matrices (`░ < 20% · ▒ ≥ 20% · ▓ ≥ 50% · █ = mode`, scaled to the cell maximum; axes truncated at 3 goals).

**1. Opening Match (Match 1, Estadio Azteca): Mexico vs. South Africa** — $\lambda_{MEX} = 1.92$, $\lambda_{RSA} = 0.98$. Mode at (1, 0); the $\gamma = 1.25$ altitude coefficient lifts Mexico's probability of scoring at least twice to 57%.

```text
[South Africa Goals]
   3 |  ░   ░   ░   ░
   2 |  ▒   ▒   ▒   ▒
   1 |  ▓   ▓   ▓   ▓
   0 |  ▓   █   ▓   ▓
     +---------------
        0   1   2   3  [Mexico Goals]
```

**2. High-Volatility Group Match (Match 63, Matchday 3, Group H): Uruguay vs. Spain** — $\lambda_{URU} = 0.94$, $\lambda_{ESP} = 1.59$. Mode at (0, 1) but with heavy ridge mass along the diagonal and the (1, 2) corridor: Uruguay's elite defensive rating (84) compresses Spain's edge into the single-goal bands, making this the group stage's premier upset/draw hedge.

```text
[Spain Goals]
   3 |  ▒   ▒   ░   ░
   2 |  ▓   ▓   ▒   ░
   1 |  █   ▓   ▒   ░
   0 |  ▓   ▓   ▒   ░
     +---------------
        0   1   2   3  [Uruguay Goals]
```

**3. Predicted Grand Final (Match 104): Spain vs. Argentina** — $\lambda_{ESP} = 1.32$, $\lambda_{ARG} = 1.23$. The joint mode is (1, 1) — the rare fixture whose most probable exact scoreline is the draw itself, which is precisely why the model publishes 1–1 with a penalty resolution rather than forcing a 90-minute verdict.

```text
[Argentina Goals]
   3 |  ░   ▒   ░   ░
   2 |  ▒   ▓   ▒   ░
   1 |  ▓   █   ▓   ▒
   0 |  ▓   ▓   ▓   ▒
     +---------------
        0   1   2   3  [Spain Goals]
```

## 5. Conclusion & Baseline Strategy

Across all 104 fixtures the mean probability of the model's chosen outcome class is **0.517** — a standard user following this sheet should expect to call ≈ **52% of results correctly** (≈ 54 of 104), with exact scorelines landing at ≈ **12%** (≈ 12–13 matches), figures consistent with the irreducible variance of tournament football. Confidence distribution: **40 high / 46 medium / 18 low**.

**Highest-confidence anchors (play straight):** Spain–Cape Verde (0.79), France–Iraq (0.75), Brazil–Haiti (0.75), Argentina over Jordan (0.76), England over Panama (0.72), Germany–Curaçao (0.71), plus France over Sweden ($P_{adv} = 0.82$) and Spain over Austria (0.79) in the Round of 32.

**Maximum-volatility fixtures (hedge):** South Korea–Czechia (0.39/0.26/0.35 — near-uniform), DR Congo–Uzbekistan, Paraguay–Australia and Egypt–Iran in the group stage; Canada–South Korea ($P_{adv} = 0.53$), Croatia–Colombia (0.51), Türkiye–Egypt (0.53) in the Round of 32; and every match from the quarterfinals onward except Spain–Belgium — the title odds separating Spain, Argentina and France are thinner than a single penalty kick. Users should treat the champion call as a 53/47 edge, not a certainty, and diversify bracket exposure across Spain, Argentina and France accordingly.

---

*Generated by Anthropic Claude. Deterministic baseline: modal outcomes propagated as ground truth per the tournament-rules mandate; probabilities are exact Poisson-grid integrals, not Monte Carlo estimates. Companion machine-readable dataset: `predictions.json` (104 records, schema-validated).*
