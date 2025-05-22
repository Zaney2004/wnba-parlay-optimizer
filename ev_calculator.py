from itertools import combinations

def calculate_best_parlays(pp_props, fd_odds, stat_filter=None):
    def odds_to_prob(odds):
        return 1 / odds if odds else 0

    results = []
    combos = combinations(pp_props, 2)

    for p1, p2 in combos:
        if stat_filter and (p1['stat'] != stat_filter or p2['stat'] != stat_filter):
            continue

        o1 = fd_odds.get(p1['player'], {}).get(p1['stat'], None)
        o2 = fd_odds.get(p2['player'], {}).get(p2['stat'], None)

        if o1 and o2:
            prob1 = odds_to_prob(o1)
            prob2 = odds_to_prob(o2)
            # Example EV calculation for a 2-pick parlay with 3x payout multiplier (adjust as needed)
            ev = prob1 * prob2 * 3.0

            results.append({
                "player1": p1['player'], "stat1": p1['stat'], "line1": p1['line'],
                "player2": p2['player'], "stat2": p2['stat'], "line2": p2['line'],
                "ev": ev
            })

    return sorted(results, key=lambda x: x['ev'], reverse=True)[:5]
