import math, pickle, json
exec(open("/sessions/happy-jolly-dijkstra/mnt/outputs/model.py").read().split("# ---------------- GROUP STAGE")[0])
st=pickle.load(open("/sessions/happy-jolly-dijkstra/mnt/outputs/state.pkl","rb"))
results=st["results"]; group_rank=st["group_rank"]; standings=st["standings"]

W={g:group_rank[g][0] for g in group_rank}   # winners
R={g:group_rank[g][1] for g in group_rank}   # runners-up
TH={g:group_rank[g][2] for g in group_rank}  # thirds

# Annex C combination #281 for thirds {A,C,D,E,F,G,I,J}:
# cols 1A,1B,1D,1E,1G,1I,1K,1L -> 3C,3G,3J,3D,3A,3F,3E,3I
third_for = {"79":TH["C"],"85":TH["G"],"81":TH["J"],"74":TH["D"],
             "82":TH["A"],"77":TH["F"],"87":TH["E"],"80":TH["I"]}

# R32 fixtures (home_slot listed first per official bracket)
r32 = {
 73:(R["A"],R["B"]), 74:(W["E"],third_for["74"]), 75:(W["F"],R["C"]),
 76:(W["C"],R["F"]), 77:(W["I"],third_for["77"]), 78:(R["E"],R["I"]),
 79:(W["A"],third_for["79"]), 80:(W["L"],third_for["80"]), 81:(W["D"],third_for["81"]),
 82:(W["G"],third_for["82"]), 83:(R["K"],R["L"]), 84:(W["H"],R["J"]),
 85:(W["B"],third_for["85"]), 86:(W["J"],R["H"]), 87:(W["K"],third_for["87"]),
 88:(R["D"],R["G"]),
}

stage_of={**{m:"round_of_32" for m in range(73,89)},
          **{m:"round_of_16" for m in range(89,97)},
          97:"quarterfinals",98:"quarterfinals",99:"quarterfinals",100:"quarterfinals",
          101:"semifinals",102:"semifinals",103:"third_place",104:"grand_final"}

winner={}; loser={}; knockout_rows=[]
def play(mid,h,a):
    nu = (h=="United States" or a=="United States")
    (sh,sa),lh,la,pH,pD,pA = analyze(h,a,host_home=False,knockout=True,neutral_us=nu)
    etp="none"
    if sh==sa:
        # decide ET/penalties by relative non-draw strength
        adv = h if pH>=pA else a
        etp=adv
    else:
        adv = h if sh>sa else a
    loser[mid] = a if adv==h else h
    winner[mid]=adv
    conf = "high" if abs(pH-pA)>0.30 else ("medium" if abs(pH-pA)>0.13 else "low")
    knockout_rows.append({"stage":stage_of[mid],"group":"none","match_id":mid,
        "home_team":h,"away_team":a,"predicted_home_score":sh,"predicted_away_score":sa,
        "extra_time_or_penalties_winner":etp,
        "home_win_probability":round(pH,2),"draw_probability":round(pD,2),
        "away_win_probability":round(pA,2),"model_confidence":conf})

for mid in range(73,89):
    h,a=r32[mid]; play(mid,h,a)

# R16
r16={89:(74,77),90:(73,75),91:(76,78),92:(79,80),93:(83,84),94:(81,82),95:(86,88),96:(85,87)}
for mid in range(89,97):
    x,y=r16[mid]; play(mid,winner[x],winner[y])
# QF
qf={97:(89,90),98:(93,94),99:(91,92),100:(95,96)}
for mid in range(97,101):
    x,y=qf[mid]; play(mid,winner[x],winner[y])
# SF
sf={101:(97,98),102:(99,100)}
for mid in range(101,103):
    x,y=sf[mid]; play(mid,winner[x],winner[y])
# 3rd place
play(103,loser[101],loser[102])
# Final
play(104,winner[101],winner[102])

allrows=results+knockout_rows
for r in allrows: r.pop("lh",None); r.pop("la",None)

# print knockout summary
def nm(mid):
    r=[x for x in knockout_rows if x["match_id"]==mid][0]
    s=f"M{mid} [{r['stage']}] {r['home_team']} {r['predicted_home_score']}-{r['predicted_away_score']} {r['away_team']}"
    if r["extra_time_or_penalties_winner"]!="none": s+=f"  (ET/pens: {r['extra_time_or_penalties_winner']})"
    s+=f"  -> {winner[mid]}"
    return s
print("=== KNOCKOUT ===")
for mid in range(73,105): print(nm(mid))
print("\nCHAMPION:", winner[104])
print("RUNNER-UP:", loser[104])
print("THIRD:", winner[103])

json.dump({"predictions":[{k:r[k] for k in ["stage","group","match_id","home_team","away_team",
   "predicted_home_score","predicted_away_score","extra_time_or_penalties_winner",
   "home_win_probability","draw_probability","away_win_probability","model_confidence"]} for r in allrows]},
   open("/sessions/happy-jolly-dijkstra/mnt/outputs/predictions.json","w"), indent=2)
pickle.dump({"winner":winner,"loser":loser,"allrows":allrows,"standings":standings,
             "group_rank":group_rank,"W":W,"R":R,"TH":TH,"third_for":third_for,
             "knockout_rows":knockout_rows}, open("/sessions/happy-jolly-dijkstra/mnt/outputs/final_state.pkl","wb"))
print("\nTOTAL MATCHES:", len(allrows))
