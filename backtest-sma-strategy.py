import pandas as pd
import datetime

# https://stackoverflow.com/a/34122596
def dateparse(time_in_secs):
    return datetime.datetime.fromtimestamp(float(time_in_secs))

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
pass