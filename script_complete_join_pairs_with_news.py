#Script que une todos los pares con las noticias
# Created by @ulises2k
# v1.0 - 15/10/2022
#
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz
import csv
import re
from os.path import expanduser
import xlsxwriter
# Install module:
# pip install pandas
# pip install XlsxWriter
#
#
# Enable "Python integration->Tools->Options->Community"
# Get Price Data from MetaTrader5 (Symbol, Timeframe)
#
#   
#Export Prices 
def getPrices(symbol, timeframe, from_year):    
    # establish connection to the MetaTrader 5 terminal
    if not mt5.initialize(login=27049283, server="RoboForex-Pro", password="o9928D"):
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

#Join Pairs with News
def joinSymbolNews(fileNameCandles,csv_file):    
    # Create timezone objects for different parts of the world    
    tz_candle = pytz.timezone("Europe/Helsinki")    #Roboforex(Brokers Timezone)
    tz_news= pytz.timezone('US/Eastern')    #News

    try:
        with open(fileNameCandles, "r") as f:
            c_reader = csv.reader(f, delimiter=";")
            t=1
            csv_row = [{}]
            print (f'Join Symbol file {fileNameCandles}...')
            for c, c_line in enumerate(c_reader):
                if t:
                    t=0
                    continue

                fecha_c = c_line[0].split(" ")[0]                
                c_year = int(fecha_c.split(".")[0])
                c_month = int(fecha_c.split(".")[1])
                c_day = int(fecha_c.split(".")[2])

                horario_c = c_line[0].split(" ")[1]
                c_hour = int(horario_c.split(":")[0])
                c_minute = int(horario_c.split(":")[1])
                c_second = int(horario_c.split(":")[2])
                
                # Year, Month, Day, Hour, Minute, Second
                datetime_candle = datetime(c_year, c_month, c_day, c_hour, c_minute, c_second)
                date_with_timezone_candle = tz_candle.localize(datetime_candle)
                
                match_c = re.search(r'^\d{4}\.\d{2}\.\d{2}', fecha_c)
                if match_c is not None:
                    year_c = fecha_c.split(".")[0]
                    month_c = fecha_c.split(".")[1]
                    # print(year_c)
                    if (int(year_c) >= 2000):
                        fileNameNews = expanduser("~") + '\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\News\\FF\\' + str(year_c) + '.' + str(month_c) + '.01.csv'
                        try:
                            with open(fileNameNews, "r") as fnews:
                                n_reader = csv.reader(fnews, delimiter=";")
                                for n, n_line in enumerate(n_reader):
                                    fecha = n_line[0].split(" ")[0]
                                    n_year = int(fecha.split(".")[0])
                                    n_month = int(fecha.split(".")[1])
                                    n_day = int(fecha.split(".")[2])

                                    horario = n_line[0].split(" ")[1]
                                    n_hour = int(horario.split(":")[0])
                                    n_minute = int(horario.split(":")[1])
                                    n_second = int(horario.split(":")[2])
                                    
                                    # Year, Month, Day, Hour, Minute, Second
                                    datetime_news = datetime(n_year, n_month, n_day, n_hour, n_minute, n_second)
                                    
                                    # Localize the given date, according to the timezone objects
                                    date_with_timezone_news = tz_news.localize(datetime_news)

                                    diff_date = date_with_timezone_news - date_with_timezone_candle

                                    #Si la diferencia esta entre 0 y 4 minutos, coloco la noticia en la vela de 5 minutos
                                    if (diff_date.total_seconds() >=0) and (diff_date.total_seconds() <= 240):                                    
                                        ##print (f'Candle: ({date_with_timezone_candle}) News: ({date_with_timezone_news}) diff: {diff_date}')
                                        csv_row.append({'time': c_line[0],
                                                        'open': c_line[1],
                                                        'close': c_line[4],
                                                        'diff openclose': c_line[7],
                                                        'currency':n_line[1],
                                                        'impact':n_line[2],
                                                        'news':n_line[3]})
                                        continue
                        except FileNotFoundError:
                            print(f"File Not Found Error: ./{fileNameNews}")
                            print("Run script CommunityPowerEA_News_Download.py")
                            exit()
        try:
            csv_columns = ['time','open','close','diff openclose','currency','impact','news']                        
            with open(f'{csv_file}', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = csv_columns, delimiter=';', extrasaction='raise', dialect='unix', quoting = csv.QUOTE_NONE)
                writer.writeheader()
                i=1
                for data in csv_row:
                    if i:
                        i=0
                        continue
                    writer.writerow(data)
        except IOError:
            print("I/O error")
            exit()
    except FileNotFoundError:
        print(f"File Not Found Error: ./{fileNameCandles}")
        exit()

#Convert CSV to Excel
def convertToExcel(csv_file,excel_file):
    print (f'Converting CSV -> {csv_file} to Excel -> {excel_file}...')
    try:
        read_file = pd.read_csv (f'{csv_file}', delimiter=";")
        writer = pd.ExcelWriter (f'{excel_file}', engine='xlsxwriter')
        read_file.to_excel (writer, sheet_name='Sheet1', index = None, header = True)

        workbook = writer.book
        worksheet1 = workbook.get_worksheet_by_name('Sheet1')
        worksheet1.autofilter('A1:G1')
        worksheet1.freeze_panes(1, 0)
        workbook.close()
    except FileNotFoundError:
        print(f"File Not Found Error: {csv_file}")
        exit()

#Main
if __name__ == "__main__":    
    year = 2019  # 2007 2020
    timeframe = 5

    # AllPairs mas Bitcoin, Gold, Index
    symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']

    for symbol in symbols:
        #symbol_export_csv
        df = getPrices(symbol=symbol, timeframe=timeframe, from_year=year)
        symbol_candles = f'./CSV/{symbol}-{str(timeframe)}.csv'
        df.to_csv(symbol_candles, sep=";")

        #join_news
        symbol_news=f'./CSV/{symbol}-News.csv'
        joinSymbolNews(symbol_candles, symbol_news)

        #convert_csv_to_excel
        symbol_news_Excel=f'./Excel/{symbol}-News.xlsx'
        convertToExcel(symbol_news, symbol_news_Excel)



