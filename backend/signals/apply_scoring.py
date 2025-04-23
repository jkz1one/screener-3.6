def apply_scoring(universe):
    scored = []
    for stock in universe:
        score = 0
        tags = []
        tier_hits = {"T1": [], "T2": [], "T3": []}
        isBlocked = False
        reasons = []

        sym = stock.get("symbol")
        price = stock.get("tv_price")
        volume = stock.get("tv_volume")
        change = stock.get("tv_changePercent")

        # --- Tier 2: Sector Rotation ---
        try:
            from backend.signals.sector_performance import get_sector_rotation_rankings
            top_sectors, bottom_sectors = get_sector_rotation_rankings()
            if stock.get("sector") in top_sectors or stock.get("sector") in bottom_sectors:
                tier_hits["T2"].append("Sector Rotation")
        except Exception as e:
            print(f"⚠️ Sector Rotation logic failed for {stock.get('symbol')}: {e}")

        # --- Risk Filters ---
        if not price or price <= 0:
            isBlocked = True
            reasons.append("No reliable price")

        if volume is None or volume < 1_000_000:
            isBlocked = True
            reasons.append("Low liquidity")

        if change is None or abs(change) < 0.3:
            isBlocked = True
            reasons.append("Low rel vol")

        # --- Final Scoring ---
        score += 3 * len(tier_hits["T1"])
        score += 2 * len(tier_hits["T2"])
        score += 1 * len(tier_hits["T3"])

        stock.update({
            "tier1": tier_hits["T1"],
            "tier2": tier_hits["T2"],
            "tier3": tier_hits["T3"],
            "tier1_hits": len(tier_hits["T1"]),
            "tier2_hits": len(tier_hits["T2"]),
            "tier3_hits": len(tier_hits["T3"]),
            "score": score,
            "tags": tags,
            "isBlocked": isBlocked,
            "reasons": reasons,
        })

        scored.append(stock)

    return scored
