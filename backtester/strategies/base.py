from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    """Interface commune à toutes les stratégies.

    generate_signals renvoie, pour chaque date, la position voulue à la clôture :
    1 = acheteur, 0 = neutre, -1 = vendeur.
    """

    name: str = "Stratégie"

    @abstractmethod
    def generate_signals(self, prix: pd.Series) -> pd.Series:
        ...
