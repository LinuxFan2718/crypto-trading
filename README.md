# crypto-trading
Code related to crypto trading plots etc.

## Install python 3.8.5

I recommend using [`pyenv`](https://github.com/pyenv/pyenv) or similar.

## Clone this repo

```bash
git clone git@github.com:LinuxFan2718/crypto-trading.git
```

## (Optional) Download up-to-date price data

[Bitcoin prices on the Binance exchange](https://www.cryptodatadownload.com/data/binance/)

The example code uses BTC/USD Hourly data.

A data file is included in this repo but you should download an up-to-date file.

Replace the existing `Binance_BTCUSDT_1h.csv` file with the one you download.

## Install libraries

```bash
pip install -r requirements.txt
```

## Run the backtester

```bash
python backtest-sma-strategy.py
```