# Script que exporta los simbolos a CSV
# Created by @ulises2k
# v1.0 - 06/10/2022
#
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz



#Get Price Data from MetaTrader5 (Symbol, Timeframe)
def getPrices(symbol, timeframe):
    if not mt5.initialize():
        print("[Metatrader5 initialization faild !]=",mt5.last_error())
        return pd.Dataframe()
    print ('[MetaTrader5]-> Initialization passed!')
    timezone = pytz.timezone("UTC")
    utc_from = datetime(year, 1, 1, tzinfo=timezone)
    utc_to   = datetime.now()
    rates    = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
    print (f'[MetaTrader5]-> Symbol {symbol} [{str(timeframe)}]')
    print (f'[MetaTrader5]-> from {utc_from:%Y.%m.%d} to {utc_to:%Y.%m.%d}')
    print (f'[MetaTrader5]-> Loaded data length: {len(rates)}')
    mt5.shutdown()

    df = pd.DataFrame(rates)   
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = pd.to_datetime(df['time'], format='%Y/%m/%d %H:%M:%S').dt.strftime('%Y.%m.%d %H:%M:%S')

    df = df.set_index('time')
    df = df.rename(columns={"tick_volume": "volume"})    

    last_value = df['open'].iloc[-1]
    decimales = str(last_value)[::-1].find('.')    
    if decimales == 1:
        multi = 10
    if decimales == 2:
        multi = 100
    if decimales == 3:
        multi = 1000
    elif decimales == 4:
        multi = 10000
    elif decimales == 5:
        multi = 100000
    else:
        multi = 1

    df['diff openclose'] = round((df['open'] - df['close']) * multi,decimales)
    
    return df[['open','high','low','close','volume', 'spread', 'diff openclose']]

year            = 2007
timeframe       = mt5.TIMEFRAME_M5

#AllPairs mas Bitcoin, Gold, Index
symbols = ['AUDCAD','AUDCHF','AUDJPY','AUDNZD','AUDUSD','CADCHF','CADJPY','CHFJPY','EURAUD','EURCAD','EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','GBPAUD','GBPCAD','GBPCHF','GBPJPY','GBPNZD','GBPUSD','NZDCAD','NZDCHF','NZDJPY','NZDUSD','USDCAD','USDCHF','USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']
for symbol in symbols:
    df = getPrices(symbol=symbol, timeframe=timeframe)
    df.to_csv(f'./{symbol}-{str(timeframe)}.csv',sep=";")
