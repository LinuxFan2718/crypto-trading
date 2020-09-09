import pandas as pd
from pylab import mpl, plt

SMA1 = 34
SMA2 = 140

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

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size'] = 12

df['SMA_short'] = df[source].rolling(SMA1).mean()
df['SMA_long'] = df[source].rolling(SMA2).mean()
df.dropna(inplace=True)

ax = df[
  [
    source, 
    'SMA_short',
    'SMA_long'
    ]
  ].plot()
ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
plt.tight_layout()
plt.show()