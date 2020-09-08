# run this script to generate a plot for given parameters
import numpy as np
import pandas as pd
import datetime
from pylab import mpl, plt
from itertools import product

# 0 for exit market, -1 for go short
NOT_LONG = 0
# Trading Strategy
SMA1 = 76
SMA2 = 110

# Data Import
# hourly data
#bitcoin_csv = 'Binance_BTCUSDT_1h.csv'
# daily date
bitcoin_csv = 'Binance_BTCUSDT_d.csv'
raw = pd.read_csv(
  bitcoin_csv,
  skiprows=1,
  comment='#',
  sep=',',
  index_col=0,
  parse_dates=True)
full_df = pd.DataFrame(raw).dropna()
full_df.index = pd.to_datetime(full_df.index, unit='s')
df = full_df.sort_values(by='Date')

source = 'Close'

# The backtest ignores transaction costs, bid-ask spreads, places
# all trades at close price, and ignores market microstructures.
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

df['SMA_short'] = df[source].rolling(SMA1).mean()
df['SMA_long'] = df[source].rolling(SMA2).mean()

df.dropna(inplace=True)
# trading rules
# Go long =  +1 when the shorter SMA is above the longer SMA
# Go short = -1 when the shorter SMA is below the longer SMA
df['Position'] = np.where(df['SMA_short'] > df['SMA_long'], 1, NOT_LONG)

# Vectorized Backtesting
df['Returns']  = np.log(df[source] / df[source].shift(1))
df['Strategy'] = df['Position'].shift(1) * df['Returns']

ax = df[['Returns', 'Strategy']].cumsum().apply(np.exp).plot(figsize=(20,12))
df['Position'].plot(ax=ax, secondary_y='Position', style='--')
#df[['SMA_short', 'SMA_long']].plot(ax=ax, secondary_y='SMA')
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
perf = np.exp(df[['Returns', 'Strategy']].sum())
ratio = round(perf[1]/perf[0], 2)
print(perf)
print(f'Strategy outperforms buy and hold {ratio}x')
plt.tight_layout()
plt.show()