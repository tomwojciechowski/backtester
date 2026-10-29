import pandas as pd

from .base import Strategy


class MeanReversion(Strategy):
    """Retour à la moyenne : achète quand le prix est anormalement bas (z-score < -seuil),
    vend quand il est anormalement haut (z-score > seuil)."""

    def __init__(self, fenetre: int = 20, seuil: float = 1.0):
        self.fenetre, self.seuil = fenetre, seuil
        self.name = f"Mean reversion {fenetre}j / {seuil}σ"

    def generate_signals(self, prix: pd.Series) -> pd.Series:
        moyenne = prix.rolling(self.fenetre).mean()
        ecart = prix.rolling(self.fenetre).std()
        z = (prix - moyenne) / ecart
        signal = pd.Series(0, index=prix.index)
        signal[z < -self.seuil] = 1
        signal[z > self.seuil] = -1
        return signal
