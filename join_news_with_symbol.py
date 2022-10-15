# Script que recorre todas las velas del simbolo y busca si en esas velas hubo noticias y exporta todo en un solo csv
# Created by @ulises2k
# v1.0 - 06/10/2022
#
import csv
import re
from os.path import expanduser
from datetime import datetime, timedelta
import pytz
#
#
def joinSymbolNews(fileNameCandles,csv_file):
    

    # Create timezone objects for different parts of the world    
    tz_candle = pytz.timezone("Europe/Helsinki")    #Roboforex(Brokers Timezone)
    tz_news= pytz.timezone('US/Eastern')    #News

    try:
        with open(fileNameCandles, "r") as f:
            c_reader = csv.reader(f, delimiter=";")
            t=1
            csv_row = [{}]
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
                
                print (f'Join Symbol file {fileNameCandles} {date_with_timezone_candle}...')

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
            with open(f'./{csv_file}', 'w') as csvfile:
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

#AllPairs mas Bitcoin, Gold, Index
#symbols = ['AUDCAD','AUDCHF','AUDJPY','AUDNZD','AUDUSD','CADCHF','CADJPY','CHFJPY','EURAUD','EURCAD','EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','GBPAUD','GBPCAD','GBPCHF','GBPJPY','GBPNZD','GBPUSD','NZDCAD','NZDCHF','NZDJPY','NZDUSD','USDCAD','USDCHF','USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']
symbols = ['EURUSD','GBPAUD','GBPCAD','GBPCHF','GBPJPY','GBPNZD','GBPUSD','NZDCAD','NZDCHF','NZDJPY','NZDUSD','USDCAD','USDCHF','USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']
timeframe = '5'
for symbol in symbols:
    symbol_news=f'{symbol}-News.csv'
    joinSymbolNews(f'./{symbol}-{str(timeframe)}.csv', symbol_news)
