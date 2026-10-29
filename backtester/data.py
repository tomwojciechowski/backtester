"""Chargement des prix depuis Yahoo Finance, avec cache local."""
from pathlib import Path

import pandas as pd
import yfinance as yf

CACHE = Path("data_cache")


def load_prices(ticker: str, start: str = "2010-01-01") -> pd.Series:
    """Renvoie les prix de clôture ajustés (dividendes et splits) d'un ticker.

    Les données sont téléchargées une seule fois puis lues depuis data_cache/.
    """
    CACHE.mkdir(exist_ok=True)
    fichier = CACHE / f"{ticker}_{start}.csv"
    if fichier.exists():
        prix = pd.read_csv(fichier, index_col=0, parse_dates=True).squeeze("columns")
    else:
        brut = yf.download(ticker, start=start, auto_adjust=True, progress=False)
        if brut.empty:
            raise ValueError(f"Aucune donnée trouvée pour le ticker « {ticker} ».")
        prix = brut["Close"].squeeze()
        prix.to_csv(fichier)
    prix.name = ticker
    return prix.dropna()
