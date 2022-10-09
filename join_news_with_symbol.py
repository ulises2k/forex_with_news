# Script que recorre todas las velas del simbolo y busca si en esas velas hubo noticias y exporta todo en un solo csv
# Created by @ulises2k
# v1.0 - 06/10/2022
#
import csv
import re
import os
from os.path import expanduser
from os.path import exists

def joinSymbolNews(fileNameCandles,csv_file):
    t=1
    csv_row = [{}]
    
    with open(f'./{fileNameCandles}', "r") as f:
        c_reader = csv.reader(f, delimiter=";")
        for i, c_line in enumerate(c_reader):
            if t:
                t=0
                continue
            fecha_c = c_line[0].split(" ")[0]
            print (f'Join Symbol file {fileNameCandles} With News {fecha_c}...')
            match_c = re.search(r'^\d{4}\.\d{2}\.\d{2}', fecha_c)
            if match_c is not None:
                year_c = fecha_c.split(".")[0]
                month_c = fecha_c.split(".")[1]
                # print(year_c)
                if (int(year_c) >= 2000):
                    fileNameNews = expanduser("~") + '\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\News\\FF\\' + str(year_c) + '.' + str(month_c) + '.01.csv'
                    with open(fileNameNews, "r") as fnews:
                        n_reader = csv.reader(fnews, delimiter=";")
                        for x, n_line in enumerate(n_reader):
                            fecha = n_line[0].split(" ")[0]
                            horario = n_line[0].split(" ")[1]
                            # print(fecha)
                            match = re.search(r'^\d{2}\:\d{2}\:\d{2}', horario)
                            if match is not None:
                                hora_news = str(horario.split(":")[0])
                                minutos_news = int(horario.split(":")[1])
                                #segundos_news = str(horario.split(":")[2])
                                segundos_news = "00"
                                if minutos_news >= 0 and minutos_news <= 4:
                                    minutos_news=str("00")
                                elif minutos_news >= 5 and minutos_news <= 14:
                                    minutos_news=str("05")
                                elif minutos_news >= 15 and minutos_news <= 24:
                                    minutos_news=str("15")
                                elif minutos_news >= 25 and minutos_news <= 34:
                                    minutos_news=str("25")
                                elif minutos_news >= 35 and minutos_news <= 44:
                                    minutos_news=str("35")
                                elif minutos_news >= 45 and minutos_news <= 54:
                                    minutos_news=str("45")
                                elif minutos_news >= 55 and minutos_news <= 59:
                                    minutos_news=str("55")
                                else:
                                    print("Error!")
                                    exit
                            fecha_completa = str(fecha) + " " + hora_news + ":" + minutos_news + ":" + segundos_news
                            #print(fecha_completa)
                            if (c_line[0] == fecha_completa):
                                csv_row.append({'time': c_line[0],
                                                'open': c_line[1],
                                                'close': c_line[4],
                                                'diff openclose': c_line[7],
                                                'currency':n_line[1],
                                                'impact':n_line[2],
                                                'news':n_line[3]})                            
                                continue
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

#AllPairs mas Bitcoin, Gold, Index
symbols = ['AUDCAD','AUDCHF','AUDJPY','AUDNZD','AUDUSD','CADCHF','CADJPY','CHFJPY','EURAUD','EURCAD','EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','GBPAUD','GBPCAD','GBPCHF','GBPJPY','GBPNZD','GBPUSD','NZDCAD','NZDCHF','NZDJPY','NZDUSD','USDCAD','USDCHF','USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']
timeframe = '5'
for symbol in symbols:
    symbol_news=f'{symbol}-News.csv' 
    joinSymbolNews(f'./{symbol}-{str(timeframe)}.csv', symbol_news)
