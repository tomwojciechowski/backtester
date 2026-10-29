"""Exemple : compare une stratégie au buy & hold et lance un walk-forward.

Usage : python run.py
"""
import matplotlib.pyplot as plt
import pandas as pd

from backtester.data import load_prices
from backtester.engine import buy_and_hold, run_backtest
from backtester.metrics import resume
from backtester.optimisation import walk_forward
from backtester.strategies import MovingAverageCross

TICKER = "SPY"

prix = load_prices(TICKER)
strategie = MovingAverageCross(50, 200)
res = run_backtest(prix, strategie.generate_signals(prix), cout_bps=5)
bench = buy_and_hold(prix)

print(f"\n=== {TICKER} : {strategie.name} vs buy & hold ===")
print(pd.DataFrame({strategie.name: resume(res), "Buy & hold": resume(bench)}))

print("\n=== Walk-forward : optimisation avant 2019, test après ===")
wf = walk_forward(
    prix,
    MovingAverageCross,
    {"court": [10, 20, 50, 100], "long": [100, 150, 200, 250]},
    date_coupure="2019-01-01",
)
print(f"Paramètres retenus : {wf['parametres']}")
print(f"Sharpe in-sample     : {wf['sharpe_in_sample']:.2f}")
print(f"Sharpe out-of-sample : {wf['sharpe_out_of_sample']:.2f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, height_ratios=[3, 1])
res["equity"].plot(ax=ax1, label=strategie.name)
bench["equity"].plot(ax=ax1, label="Buy & hold")
ax1.set_title(f"{TICKER} : croissance de 1 € investi")
ax1.legend()
(res["equity"] / res["equity"].cummax() - 1).plot(ax=ax2, color="tab:red")
ax2.set_title("Drawdown de la stratégie")
plt.tight_layout()
plt.savefig("equity_curve.png", dpi=120)
plt.show()
