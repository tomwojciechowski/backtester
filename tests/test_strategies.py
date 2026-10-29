import numpy as np
import pandas as pd
import pytest

from backtester.optimisation import grid_search, walk_forward
from backtester.strategies import MeanReversion, MovingAverageCross


@pytest.fixture
def prix():
    rng = np.random.default_rng(0)
    rend = rng.normal(0.0003, 0.01, 1500)
    return pd.Series(100 * np.cumprod(1 + rend), index=pd.bdate_range("2015-01-01", periods=1500))


def test_tendance_haussiere_donne_signal_acheteur():
    prix = pd.Series(np.arange(1, 301, dtype=float), index=pd.bdate_range("2020-01-01", periods=300))
    signaux = MovingAverageCross(10, 50).generate_signals(prix)
    assert signaux.iloc[-1] == 1


def test_fenetres_invalides():
    with pytest.raises(ValueError):
        MovingAverageCross(200, 50)


def test_mean_reversion_signaux_valides(prix):
    signaux = MeanReversion(20, 1.0).generate_signals(prix)
    assert set(signaux.unique()) <= {-1, 0, 1}


def test_grid_search_ignore_combinaisons_invalides(prix):
    res = grid_search(prix, MovingAverageCross, {"court": [20, 100], "long": [50, 200]})
    assert len(res) == 3  # (100, 50) est rejetée
    assert res["sharpe"].is_monotonic_decreasing


def test_walk_forward(prix):
    wf = walk_forward(prix, MovingAverageCross, {"court": [10, 20], "long": [50, 100]}, "2019-01-01")
    assert set(wf) == {"parametres", "sharpe_in_sample", "sharpe_out_of_sample"}
    assert isinstance(wf["parametres"]["court"], int)
