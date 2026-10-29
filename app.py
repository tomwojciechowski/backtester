"""Démo interactive. Usage : streamlit run app.py"""
import pandas as pd
import streamlit as st

from backtester.data import load_prices
from backtester.engine import buy_and_hold, run_backtest
from backtester.metrics import resume
from backtester.strategies import MeanReversion, MovingAverageCross

st.set_page_config(page_title="Backtester", layout="wide")
st.title("Backtester de stratégies")

with st.sidebar:
    ticker = st.text_input("Ticker Yahoo Finance", "SPY")
    debut = st.date_input("Début", pd.Timestamp("2010-01-01"))
    choix = st.selectbox("Stratégie", ["Moyennes mobiles", "Mean reversion"])
    if choix == "Moyennes mobiles":
        court = st.slider("Moyenne courte (jours)", 5, 100, 50)
        long = st.slider("Moyenne longue (jours)", court + 1, 300, max(200, court + 1))
        strategie = MovingAverageCross(court, long)
    else:
        fenetre = st.slider("Fenêtre (jours)", 5, 60, 20)
        seuil = st.slider("Seuil (écarts-types)", 0.5, 3.0, 1.0, 0.1)
        strategie = MeanReversion(fenetre, seuil)
    cout = st.slider("Coûts de transaction (bps)", 0, 30, 5)

try:
    prix = load_prices(ticker, str(debut))
except ValueError as e:
    st.error(str(e))
    st.stop()

res = run_backtest(prix, strategie.generate_signals(prix), cout)
bench = buy_and_hold(prix)

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Croissance de 1 € investi")
    st.line_chart(pd.DataFrame({strategie.name: res["equity"], "Buy & hold": bench["equity"]}))
    st.subheader("Drawdown")
    st.area_chart(res["equity"] / res["equity"].cummax() - 1)
with col2:
    st.subheader("Métriques")
    st.table(pd.DataFrame({"Stratégie": resume(res), "Buy & hold": resume(bench)}))
