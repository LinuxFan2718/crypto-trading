import numpy as np
import pandas as pd
import datetime
from pylab import mpl, plt

# parse Unix timestamps into a datetime that pandas understands
# https://stackoverflow.com/a/34122596
def dateparse(time_in_secs):
    return datetime.datetime.fromtimestamp(float(time_in_secs))

# Data Import
bitcoin_csv = 'Binance_BTCUSDT_1h.csv'
raw = pd.read_csv(
  bitcoin_csv,
  skiprows=1,
  comment='#',
  sep=',',
  index_col=0,
  parse_dates=True,
  date_parser=dateparse)
df = pd.DataFrame(raw)

source = 'Close'

# The backtest ignores transaction costs, bid-ask spreads, places
# all trades at close price, and ignores market microstructures.
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

# Trading Strategy
mult = 12
SMA1 = 42 * mult
SMA2 = 252 * mult

df['SMA1'] = df[source].rolling(SMA1).mean()
df['SMA2'] = df[source].rolling(SMA2).mean()

df.dropna(inplace=True)
# trading rules
# Go long =  +1 when the shorter SMA is above the longer SMA
# Go short = -1 when the shorter SMA is below the longer SMA
df['Position'] = np.where(df['SMA1'] > df['SMA2'], 1, -1)

# Vectorized Backtesting
df['Returns']  = np.log(df[source] / df[source].shift(1))
df['Strategy'] = df['Position'].shift(1) * df['Returns']

ax = df[['Returns', 'Strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))
df['Position'].plot(ax=ax, secondary_y='Position', style='--')
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
plt.show()