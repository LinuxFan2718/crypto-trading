# run this script to discover optimal values for SMA long and short
import numpy as np
import pandas as pd
import datetime
from pylab import mpl, plt
from itertools import product

# 0 for exit market, -1 for go short
NOT_LONG = -1

# Data Import
# hourly data
#bitcoin_csv = 'Binance_BTCUSDT_1h.csv'
# daily data
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
full_df = full_df.sort_values(by='Date')
source = 'Close'
# The backtest ignores transaction costs, bid-ask spreads, places
# all trades at close price, and ignores market microstructures.

# this script based on the one in Python for Finance by Yves Hilpisch
# page 490
sma1 = range(20, 91, 2)
sma2 = range(50, 241, 5)

# initialize an empty matrix to store performance data for SMA pairs
parameter_view = pd.DataFrame()
parameter_view = parameter_view.reindex(columns = sma2)
parameter_view = parameter_view.reindex(parameter_view.index.tolist() + list(sma1))

results = pd.DataFrame()
for SMA1, SMA2 in product(sma1, sma2):
  df = pd.DataFrame(full_df[source])
  df.dropna(inplace=True)
  df['Returns']  = np.log(df[source] / df[source].shift(1))
  df['SMA1'] = df[source].rolling(SMA1).mean()
  df['SMA2'] = df[source].rolling(SMA2).mean()
  df.dropna(inplace=True)
  # trading rules
  # Go long =  +1 when the shorter SMA is above the longer SMA
  # exit market = 0
  # Go short = -1 when the shorter SMA is below the longer SMA
  df['Position'] = np.where(df['SMA1'] > df['SMA2'], 1, NOT_LONG)
  df['Strategy'] = df['Position'].shift(1) * df['Returns']
  df.dropna(inplace=True)
  # store results to find optimum parameters
  perf = np.exp(df[['Returns', 'Strategy']].sum())
  results = results.append(pd.DataFrame(
              {'SMA1': SMA1, 'SMA2': SMA2,
               'MARKET': perf['Returns'],
               'STRATEGY': perf['Strategy'],
               'OUT': perf['Strategy'] - perf['Returns']},
               index=[0]), ignore_index=True)
  
  # store performance for visualization
  ratio = round(perf[1]/perf[0], 2)
  parameter_view.at[SMA1, SMA2] = ratio


results.info()
print(results.sort_values('OUT', ascending=False).head(7))

fig, ax = plt.subplots()
mat = ax.matshow(parameter_view)
cax = fig.colorbar(mat)

plt.xticks(range(len(parameter_view.columns)), parameter_view.columns)
plt.yticks(range(len(parameter_view.index)), parameter_view.index)
# ax.set_xticklabels([None] + list(parameter_view.columns))
# ax.set_yticklabels([None] + list(parameter_view.index))
# ax.axis('image')

plt.tight_layout()
plt.show()
