import pandas as pd

from .base import Strategy


class MovingAverageCross(Strategy):
    """Suivi de tendance : acheteur quand la moyenne courte passe au-dessus de la longue."""

    def __init__(self, court: int = 50, long: int = 200):
        if court >= long:
            raise ValueError("La fenêtre courte doit être plus petite que la longue.")
        self.court, self.long = court, long
        self.name = f"Moyennes mobiles {court}/{long}"

    def generate_signals(self, prix: pd.Series) -> pd.Series:
        mm_court = prix.rolling(self.court).mean()
        mm_long = prix.rolling(self.long).mean()
        return (mm_court > mm_long).astype(int)
