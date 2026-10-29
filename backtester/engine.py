"""Moteur de backtest vectorisé."""
import pandas as pd


def run_backtest(prix: pd.Series, signaux: pd.Series, cout_bps: float = 5) -> pd.DataFrame:
    """Simule une stratégie à partir de ses signaux.

    - Le signal calculé à la clôture du jour t est exécuté pour le jour t+1
      (shift(1)) : aucune information future n'est utilisée.
    - Chaque changement de position coûte cout_bps points de base sur le montant échangé.
    """
    rend = prix.pct_change().fillna(0)
    position = signaux.reindex(prix.index).shift(1).fillna(0)
    couts = position.diff().abs().fillna(0) * cout_bps / 10_000
    rend_strat = position * rend - couts
    return pd.DataFrame(
        {
            "prix": prix,
            "position": position,
            "rendement": rend_strat,
            "equity": (1 + rend_strat).cumprod(),
        }
    )


def buy_and_hold(prix: pd.Series) -> pd.DataFrame:
    """Benchmark : investi en permanence, sans coûts."""
    return run_backtest(prix, pd.Series(1, index=prix.index), cout_bps=0)
