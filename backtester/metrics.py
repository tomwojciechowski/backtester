"""Indicateurs de performance et de risque."""
import numpy as np
import pandas as pd

N = 252  # jours de bourse par an


def cagr(equity: pd.Series) -> float:
    """Rendement annualisé composé."""
    return equity.iloc[-1] ** (N / len(equity)) - 1


def volatilite(r: pd.Series) -> float:
    return r.std() * np.sqrt(N)


def sharpe(r: pd.Series) -> float:
    """Ratio de Sharpe annualisé (taux sans risque supposé nul)."""
    return float(r.mean() / r.std() * np.sqrt(N)) if r.std() > 0 else 0.0


def sortino(r: pd.Series) -> float:
    """Comme le Sharpe, mais ne pénalise que la volatilité à la baisse."""
    baisse = r[r < 0].std()
    return float(r.mean() / baisse * np.sqrt(N)) if baisse > 0 else 0.0


def max_drawdown(equity: pd.Series) -> float:
    """Pire perte depuis un plus haut."""
    return float((equity / equity.cummax() - 1).min())


def turnover(position: pd.Series) -> float:
    """Volume échangé moyen par an (1 = la position entière une fois par an)."""
    return float(position.diff().abs().sum() / len(position) * N)


def resume(res: pd.DataFrame) -> dict:
    r, eq = res["rendement"], res["equity"]
    return {
        "CAGR": f"{cagr(eq):.2%}",
        "Volatilité": f"{volatilite(r):.2%}",
        "Sharpe": f"{sharpe(r):.2f}",
        "Sortino": f"{sortino(r):.2f}",
        "Max drawdown": f"{max_drawdown(eq):.2%}",
        "Turnover annuel": f"{turnover(res['position']):.1f}",
    }
