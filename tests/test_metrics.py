import numpy as np
import pandas as pd
import pytest

from backtester.metrics import cagr, max_drawdown, sharpe


def test_max_drawdown():
    equity = pd.Series([1.0, 1.2, 0.9, 1.1, 1.3])
    assert max_drawdown(equity) == pytest.approx(0.9 / 1.2 - 1)


def test_cagr_un_an():
    equity = pd.Series(np.linspace(1.0, 1.10, 252))
    assert cagr(equity) == pytest.approx(0.10)


def test_sharpe_nul_si_aucune_volatilite():
    assert sharpe(pd.Series([0.0] * 10)) == 0.0
