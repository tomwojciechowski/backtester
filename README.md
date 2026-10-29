# Backtester de stratégies de trading

Moteur de backtest en Python pour évaluer des stratégies systématiques sur données de marché réelles (Yahoo Finance) : coûts de transaction, métriques de risque, validation walk-forward et démo interactive.

![tests](https://github.com/tomwojciechowski/backtester/actions/workflows/tests.yml/badge.svg)

**Démo en ligne :** _lien Streamlit à ajouter_

![Courbe d'equity](equity_curve.png)
<!-- image générée par `python run.py` : pense à la committer -->

## Fonctionnalités

- **Stratégies** : croisement de moyennes mobiles (suivi de tendance), retour à la moyenne par z-score. Ajouter une stratégie = créer une classe qui hérite de `Strategy`.
- **Moteur vectorisé** avec exécution à J+1 (aucune information future utilisée) et coûts de transaction paramétrables.
- **Métriques** : CAGR, volatilité, Sharpe, Sortino, max drawdown, turnover.
- **Optimisation** : grid search et validation walk-forward (paramètres choisis sur une période, évalués sur une autre).
- **Démo Streamlit** : choix du ticker, de la stratégie, des paramètres et des coûts.
- **Tests unitaires** (pytest) et intégration continue (GitHub Actions).

## Installation

```bash
git clone https://github.com/tomwojciechowski/backtester.git
cd backtester
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
python run.py            # backtest + walk-forward sur le S&P 500 (SPY), génère equity_curve.png
streamlit run app.py     # démo interactive dans le navigateur
python -m pytest         # tests
```

## Structure

```
backtester/
├── data.py              # téléchargement des prix + cache local
├── engine.py            # moteur de backtest
├── metrics.py           # indicateurs de performance et de risque
├── optimisation.py      # grid search et walk-forward
└── strategies/          # une classe par stratégie
tests/                   # tests unitaires
run.py                   # exemple en ligne de commande
app.py                   # démo Streamlit
```

## Méthodologie

**Pas de look-ahead.** Le signal calculé avec le cours de clôture du jour *t* n'est appliqué qu'au rendement du jour *t+1* (`signaux.shift(1)`). Un test unitaire le vérifie.

**Rendement de la stratégie** :

$$r^{strat}_t = p_{t-1} \cdot r_t - c \cdot |p_{t-1} - p_{t-2}|$$

où $p$ est la position (-1, 0 ou 1), $r_t$ le rendement de l'actif et $c$ le coût de transaction.

**Ratio de Sharpe annualisé** : $S = \frac{\bar{r}}{\sigma_r}\sqrt{252}$ (taux sans risque supposé nul).

**Walk-forward.** Les paramètres sont optimisés uniquement sur la période d'entraînement (avant 2019), puis la stratégie est évaluée sur la période de test, jamais utilisée pendant l'optimisation. Un écart important entre Sharpe in-sample et out-of-sample signale du surapprentissage.

## Limites

- **Biais du survivant** : Yahoo Finance ne fournit que les titres encore cotés.
- **Exécution simplifiée** : ordres supposés exécutés au cours de clôture, sans impact de marché ni contrainte de liquidité.
- **Coûts constants** : le spread et les frais réels varient selon l'actif et la période.
- **Un seul actif à la fois** : pas encore de gestion de portefeuille multi-actifs.

## Pistes d'amélioration

- Momentum cross-sectionnel sur un univers d'actions ou d'ETF
- Pairs trading avec test de cointégration
- Heatmap de sensibilité du Sharpe aux paramètres
- Dimensionnement des positions par ciblage de volatilité
