# Backtester de stratégies de trading

![tests](https://github.com/tomwojciechowski/backtester/actions/workflows/tests.yml/badge.svg)

Je m'intéresse à la finance de marché et je voulais comprendre concrètement comment on teste une stratégie de trading avant de la mettre en production. Plutôt que d'utiliser une librairie toute faite (Backtrader, Zipline…), j'ai codé mon propre moteur de backtest en Python, pour bien maîtriser chaque étape : les données, les signaux, l'exécution, les coûts et les métriques.

<!-- Démo en ligne : (lien Streamlit) -->

<!-- ![Courbe d'equity](equity_curve.png) -->

## Ce que fait le projet

- Il récupère les prix historiques sur Yahoo Finance (avec un petit cache pour ne pas tout retélécharger à chaque fois).
- Il teste deux stratégies pour l'instant :
  - un **croisement de moyennes mobiles** (50/200 jours par défaut), une stratégie de suivi de tendance classique ;
  - une stratégie de **retour à la moyenne** : j'achète quand le prix s'écarte trop vers le bas de sa moyenne (z-score) et je vends quand il s'écarte trop vers le haut.
- Il prend en compte les coûts de transaction, ce qui change pas mal les résultats sur les stratégies qui tradent souvent.
- Il calcule les indicateurs habituels : CAGR, volatilité, Sharpe, Sortino, max drawdown et turnover.
- Il compare toujours la stratégie à un simple buy & hold, parce qu'une stratégie qui ne bat pas le buy & hold n'a pas beaucoup d'intérêt.
- Il fait une validation **walk-forward** pour vérifier que les résultats ne sont pas juste du surapprentissage.
- Une petite appli Streamlit permet de jouer avec les paramètres et de voir directement l'impact sur la performance.

## Lancer le projet

```bash
git clone https://github.com/tomwojciechowski/backtester.git
cd backtester
python -m venv .venv
source .venv/bin/activate        # sur Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

Ensuite :

```bash
python run.py            # backtest sur le S&P 500 (SPY) + walk-forward, et sauvegarde du graphique
streamlit run app.py     # l'appli interactive
python -m pytest         # les tests
```

## Comment c'est organisé

```
backtester/
├── data.py              # récupération des prix
├── engine.py            # le moteur de backtest
├── metrics.py           # les indicateurs de perf et de risque
├── optimisation.py      # recherche de paramètres et walk-forward
└── strategies/          # une classe par stratégie
tests/                   # tests unitaires
run.py                   # exemple en ligne de commande
app.py                   # appli Streamlit
```

J'ai essayé de rendre le code facile à étendre : toutes les stratégies héritent d'une classe `Strategy` et doivent juste implémenter `generate_signals`. Pour en ajouter une nouvelle, il suffit de créer un fichier dans `strategies/`.

## Les points auxquels j'ai fait attention

**Ne pas tricher avec le futur (look-ahead bias).** C'est l'erreur la plus classique en backtest : utiliser le cours de clôture d'un jour pour décider d'une position… et profiter du rendement de ce même jour. Dans mon moteur, un signal calculé à la clôture du jour *t* n'est appliqué qu'à partir du jour *t+1* (`signaux.shift(1)`). J'ai écrit un test exprès pour le vérifier.

Concrètement, le rendement de la stratégie chaque jour est :

$$r^{strat}_t = p_{t-1} \cdot r_t - c \cdot |p_{t-1} - p_{t-2}|$$

avec $p$ la position (-1, 0 ou 1), $r_t$ le rendement de l'actif et $c$ le coût de transaction.

**Le Sharpe** est annualisé avec $\sqrt{252}$ (nombre de jours de bourse par an), et je suppose un taux sans risque nul pour simplifier.

**Le surapprentissage.** Si on teste plein de paramètres sur toute la période, on finit toujours par trouver une combinaison qui a l'air géniale… sur le passé. Pour éviter ça, je choisis les paramètres uniquement sur les données avant 2019, puis je regarde ce que ça donne après 2019, sur des données que l'optimisation n'a jamais vues. Si le Sharpe s'effondre entre les deux périodes, c'est que la stratégie était surtout calée sur le passé.

## Les limites (pour être honnête)

- **Biais du survivant** : Yahoo Finance ne contient que les actions encore cotées, donc celles qui ont fait faillite n'apparaissent pas. Sur un indice comme le S&P 500, c'est moins gênant, mais sur un panier d'actions ça gonflerait les résultats.
- **Exécution simplifiée** : je suppose qu'on achète et vend exactement au cours de clôture, sans impact sur le marché ni problème de liquidité.
- **Coûts fixes** : en réalité, le spread et les frais varient selon l'actif et selon les périodes (en 2008 ou en mars 2020, ils explosent).
- **Un seul actif à la fois** pour l'instant, donc pas de vraie gestion de portefeuille.

## La suite

Ce que j'aimerais ajouter ensuite :

- une stratégie de **pairs trading** avec un test de cointégration ;
- du **momentum** sur plusieurs ETF sectoriels (acheter chaque mois ceux qui ont le mieux performé) ;
- une heatmap pour voir à quel point le Sharpe dépend des paramètres choisis ;
- un dimensionnement des positions en fonction de la volatilité.

Si vous avez des remarques ou des idées, n'hésitez pas à ouvrir une issue !
