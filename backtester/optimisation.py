"""Recherche de paramètres et validation walk-forward (hors échantillon)."""
from itertools import product

import pandas as pd

from .engine import run_backtest
from .metrics import sharpe


def grid_search(prix: pd.Series, strategie_cls, grille: dict, cout_bps: float = 5) -> pd.DataFrame:
    """Teste toutes les combinaisons de paramètres et renvoie le Sharpe de chacune."""
    lignes = []
    noms = list(grille)
    for valeurs in product(*grille.values()):
        params = dict(zip(noms, valeurs))
        try:
            strat = strategie_cls(**params)
        except ValueError:
            continue  # combinaison invalide (ex. court >= long)
        res = run_backtest(prix, strat.generate_signals(prix), cout_bps)
        lignes.append({**params, "sharpe": sharpe(res["rendement"])})
    return pd.DataFrame(lignes).sort_values("sharpe", ascending=False).reset_index(drop=True)


def walk_forward(prix: pd.Series, strategie_cls, grille: dict, date_coupure: str, cout_bps: float = 5) -> dict:
    """Optimise sur les données avant date_coupure, puis évalue sur les données après.

    Les signaux sont calculés sur tout l'historique (pour que les moyennes mobiles
    soient « chaudes » au début de la période de test), mais les paramètres ne sont
    choisis qu'avec la période d'entraînement.
    """
    train = prix[prix.index < date_coupure]
    resultats = grid_search(train, strategie_cls, grille, cout_bps)
    meilleurs = resultats.iloc[0].drop("sharpe").to_dict()
    meilleurs = {k: type(grille[k][0])(v) for k, v in meilleurs.items()}

    strat = strategie_cls(**meilleurs)
    res = run_backtest(prix, strat.generate_signals(prix), cout_bps)
    in_sample = res[res.index < date_coupure]
    out_sample = res[res.index >= date_coupure]
    return {
        "parametres": meilleurs,
        "sharpe_in_sample": sharpe(in_sample["rendement"]),
        "sharpe_out_of_sample": sharpe(out_sample["rendement"]),
    }
