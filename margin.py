#!/usr/bin/env python3
"""Reseller Margin Calculator — Hobby Home Fun's real pricing math.

Given a total cost (item + every shipping leg you pay) it computes:
  * profit at a candidate sale price:  profit = 0.92 * sell - cost
    (0.92 = sale price minus ~3% card processing and a 5% refund reserve)
  * margin % at that price:            margin = profit / sell * 100
  * the first-bar price: the LOWER of the $8-profit price ((cost+8)/0.92)
    and the 35%-margin price (cost/0.57), rounded UP to the next .99 —
    i.e. the cheapest price that still clears one of the two bars.

Usage:
  python3 margin.py --cost 7.34
  python3 margin.py --cost 7.34 --sell 12.99
  python3 margin.py --cost 13.46 --sell 23.99

Exit code is 0 when a --sell price clears at least one bar, 1 when it
clears neither (handy for scripts), 0 when no --sell is given.
"""
import argparse
import math
import sys

PROFIT_BAR = 8.00      # dollars of profit
MARGIN_BAR = 0.35      # 35% margin
KEEP = 0.92            # share of the sale price kept after fees/reserve


def profit(cost: float, sell: float) -> float:
    return KEEP * sell - cost


def margin_pct(cost: float, sell: float) -> float:
    return profit(cost, sell) / sell * 100 if sell else 0.0


def round_up_99(x: float) -> float:
    """Round up to the next price ending in .99."""
    whole = math.floor(x)
    candidate = whole + 0.99
    if candidate < x - 1e-9:
        candidate += 1.00
    return round(candidate, 2)


def first_bar_price(cost: float) -> tuple[float, float, float]:
    """Return (first-bar price, $8-profit price, 35%-margin price)."""
    p_profit = round_up_99((cost + PROFIT_BAR) / KEEP)
    p_margin = round_up_99(cost / (1 - MARGIN_BAR - 0.08))  # cost / 0.57
    return min(p_profit, p_margin), p_profit, p_margin


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cost", type=float, required=True,
                    help="Total realistic cost: item + all shipping legs you pay.")
    ap.add_argument("--sell", type=float, default=None,
                    help="Candidate sale price to evaluate (optional).")
    args = ap.parse_args()

    if args.cost < 0:
        ap.error("--cost must be >= 0")

    fb, p_profit, p_margin = first_bar_price(args.cost)
    print(f"Total cost:            ${args.cost:,.2f}")
    print(f"$8-profit price:       ${p_profit:,.2f}   ((cost + 8) / 0.92, up to .99)")
    print(f"35%-margin price:      ${p_margin:,.2f}   (cost / 0.57, up to .99)")
    print(f"FIRST-BAR price:       ${fb:,.2f}   (lower of the two)")

    if args.sell is None:
        print("\nNo --sell given. At the first-bar price:")
        print(f"  profit ${profit(args.cost, fb):,.2f} | margin {margin_pct(args.cost, fb):.1f}%")
        return 0

    p = profit(args.cost, args.sell)
    m = margin_pct(args.cost, args.sell)
    clears = p >= PROFIT_BAR or m >= MARGIN_BAR * 100
    close = (6.00 <= p < PROFIT_BAR) or (30.0 <= m < MARGIN_BAR * 100)
    print(f"\nAt sell price ${args.sell:,.2f}:")
    print(f"  profit ${p:,.2f} | margin {m:.1f}%")
    if clears:
        print("  Verdict: PASSES (clears the profit bar, the margin bar, or both).")
        return 0
    if close:
        print("  Verdict: CLOSE — clears neither bar but is within reach of one. Hold for a human decision.")
        return 1
    print("  Verdict: FAILS both bars.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
