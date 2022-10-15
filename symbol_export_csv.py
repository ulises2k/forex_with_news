# Script que exporta los simbolos a CSV
# Created by @ulises2k
# v1.0 - 06/10/2022
#
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Enable "Python integration->Tools->Options->Community"
# Get Price Data from MetaTrader5 (Symbol, Timeframe)
#
#
def getPrices(symbol, timeframe, from_year):
    # if not mt5.initialize():
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize(login=27049283, server="RoboForex-Pro", password="XXXXXXXXXX"):
        print("[Metatrader5 initialization faild !]=", mt5.last_error())
        return pd.Dataframe()
    print('[MetaTrader5]-> Initialization passed!')

    timezone = pytz.timezone("Europe/Helsinki")  # Roboforex (Brokers Timezone)
    yesterday = datetime.now(tz=timezone) - timedelta(-1)
    utc_from = datetime(from_year, 1, 1, tzinfo=timezone)
    utc_to = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=timezone)
    rates = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
    print(f'[MetaTrader5]-> Symbol {symbol} [{str(timeframe)}]')
    print(f'[MetaTrader5]-> from {utc_from:%Y.%m.%d} to {utc_to:%Y.%m.%d}')
    print(f'[MetaTrader5]-> Loaded data length: {len(rates)}')

    # attempt to enable the display of the EURUSD symbol in MarketWatch
    selected = mt5.symbol_select(symbol, True)
    if not selected:
        print(f'Failed to select {symbol}')
        mt5.shutdown()
        return pd.Dataframe()

    # display EURUSD symbol properties
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info != None:
        digits = symbol_info.digits
    else:
        print("Error symbol_info() ", mt5.last_error())
        mt5.shutdown()
        return pd.Dataframe()

    mt5.shutdown()

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = pd.to_datetime(df['time'], format='%Y/%m/%d %H:%M:%S').dt.strftime('%Y.%m.%d %H:%M:%S')

    df = df.set_index('time')
    df = df.rename(columns={"tick_volume": "volume"})

    #last_value = df['open'].iloc[-1]
    #digits = str(last_value)[::-1].find('.')
    if digits == 2:
        multi = 100
    if digits == 3:
        multi = 100
    elif digits == 4:
        multi = 10000
    elif digits == 5:
        multi = 10000
    else:
        multi = 1
    df['diff openclose'] = round((df['open'] - df['close']) * multi, digits)
    return df[['open', 'high', 'low', 'close', 'volume', 'spread', 'diff openclose']]


year = 2022  # 2007 2020
timeframe = mt5.TIMEFRAME_M5

# AllPairs mas Bitcoin, Gold, Index
symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']
#symbols = ['EURUSD']
for symbol in symbols:
    df = getPrices(symbol=symbol, timeframe=timeframe, from_year=year)
    df.to_csv(f'./{symbol}-{str(timeframe)}.csv', sep=";")
