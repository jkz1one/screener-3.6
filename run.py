from backend.screenbuilder import build_screening_output

results = build_screening_output()

for _, r in results.iterrows():
    print(f"▶ {r['symbol']}: T1={r['tier1_hits']}  T2={r['tier2_hits']}  T3={r['tier3_hits']}  Score={r['score']}")
