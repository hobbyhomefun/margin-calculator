# Reseller Margin Calculator

The exact pricing math used to run **Hobby Home Fun**, a real reselling store — packaged so any small reseller can use it.

## The rules it implements

- **Profit** = `0.92 × sell − cost`. The 0.92 is deliberate: it leaves ~3% for card processing and a 5% refund reserve, so "profit" here is money you actually keep.
- **An item passes** if it clears **either** bar: **~$8 profit OR ~35% margin**. Not both — either.
- **First-bar pricing:** the selling price is set at the *lower* of
  - the $8-profit price: `(cost + 8) / 0.92`
  - the 35%-margin price: `cost / 0.57`

  each rounded **up** to the next `.99`. That is the cheapest price that still clears a bar — no money left on the table, no bar missed.
- **Close-margin zone:** clears neither bar but lands within ~$6–8 profit or ~30–35% margin. The tool flags these instead of failing them — in the real store those go to a human for a final call.

`cost` always means the **full realistic cost**: item price at the regular repeat-buyer rate (never a one-time welcome/promo price) plus every shipping leg you pay.

## Two ways to use it

### 1. Command line — `margin.py` (Python 3, no dependencies)

```bash
python3 margin.py --cost 7.34            # what should I charge?
python3 margin.py --cost 7.34 --sell 12.99   # does this price work?
```

Exit code: `0` if a checked `--sell` price passes, `1` if it fails or is close — easy to wire into scripts.

### 2. In the browser — `index.html`

Open the file in any browser. Same math, no install, nothing leaves the page.

## Example runs (real numbers from the store)

A harmonica whose supplier cost is **$7.34**:

```
$ python3 margin.py --cost 7.34 --sell 12.99
Total cost:            $7.34
$8-profit price:       $16.99   ((cost + 8) / 0.92, up to .99)
35%-margin price:      $12.99   (cost / 0.57, up to .99)
FIRST-BAR price:       $12.99   (lower of the two)

At sell price $12.99:
  profit $4.61 | margin 35.5%
  Verdict: PASSES (clears the profit bar, the margin bar, or both).
```

It sells at **$12.99** — the margin bar is reached long before the $8-profit price, so $12.99 is the price. (This exact item is live in the store.)

A knitting-needle set costing **$13.46**:

```
$ python3 margin.py --cost 13.46
Total cost:            $13.46
$8-profit price:       $23.99   ((cost + 8) / 0.92, up to .99)
35%-margin price:      $23.99   (cost / 0.57, up to .99)
FIRST-BAR price:       $23.99   (lower of the two)

No --sell given. At the first-bar price:
  profit $8.61 | margin 35.9%
```

Both bars land on the same price — it sells at **$23.99** and clears both.

A failing case — cost crept to **$15.37** while the price stayed $11.99:

```
$ python3 margin.py --cost 15.37 --sell 11.99
...
At sell price $11.99:
  profit $-4.34 | margin -36.2%
  Verdict: FAILS both bars.
```

That is the signal to reprice or pull the item — the tool exists so you see it the day the cost moves, not at tax time.

## License

MIT — use it, sell with it, build on it.
