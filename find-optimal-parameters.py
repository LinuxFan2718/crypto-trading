# run this script to discover optimal values for SMA long and short

import numpy as np
import pandas as pd
import datetime
from pylab import mpl, plt
from itertools import product

# parse Unix timestamps into a datetime that pandas understands
# https://stackoverflow.com/a/34122596
# def dateparse(time_in_secs):
#     return datetime.datetime.fromtimestamp(float(time_in_secs))

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
full_df = full_df.sort_values(by='Date')
source = 'Close'
# The backtest ignores transaction costs, bid-ask spreads, places
# all trades at close price, and ignores market microstructures.

# this script based on the one in Python for Finance by Yves Hilpisch
# page 490
sma1 = range(20, 91, 4)
sma2 = range(110, 301, 10)
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
  # Go short = -1 when the shorter SMA is below the longer SMA
  df['Position'] = np.where(df['SMA1'] > df['SMA2'], 1, -1)
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

results.info()
print(results.sort_values('OUT', ascending=False).head(7))
