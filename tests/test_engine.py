import pandas as pd
import pytest

from backtester.engine import buy_and_hold, run_backtest


@pytest.fixture
def prix():
    return pd.Series([100, 101, 99, 102, 105.0], index=pd.date_range("2024-01-01", periods=5))


def test_buy_and_hold_sans_couts(prix):
    res = buy_and_hold(prix)
    assert res["equity"].iloc[-1] == pytest.approx(105 / 100)


def test_pas_de_look_ahead(prix):
    # un signal émis le dernier jour ne doit rien rapporter
    signaux = pd.Series([0, 0, 0, 0, 1], index=prix.index)
    res = run_backtest(prix, signaux, cout_bps=0)
    assert res["equity"].iloc[-1] == pytest.approx(1.0)


def test_signal_execute_le_lendemain(prix):
    # acheteur à la clôture du jour 2 => on gagne le rendement 99 -> 102 -> 105
    signaux = pd.Series([0, 0, 1, 1, 1], index=prix.index)
    res = run_backtest(prix, signaux, cout_bps=0)
    assert res["equity"].iloc[-1] == pytest.approx(105 / 99)


def test_position_vendeuse(prix):
    signaux = pd.Series(-1, index=prix.index)
    res = run_backtest(prix, signaux, cout_bps=0)
    attendu = (1 - 0.01) * (1 - (99 / 101 - 1)) * (1 - (102 / 99 - 1)) * (1 - (105 / 102 - 1))
    assert res["equity"].iloc[-1] == pytest.approx(attendu)


def test_les_couts_reduisent_la_performance(prix):
    signaux = pd.Series([1, 0, 1, 0, 1], index=prix.index)
    sans = run_backtest(prix, signaux, cout_bps=0)["equity"].iloc[-1]
    avec = run_backtest(prix, signaux, cout_bps=10)["equity"].iloc[-1]
    assert avec < sans
