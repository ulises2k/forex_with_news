# Script que convierte los CSV a Excel
# Created by @ulises2k
# v1.0 - 06/10/2022
#
import xlsxwriter
import pandas as pd
# Install module:
# pip install pandas
# pip install XlsxWriter
#
#
def convertToExcel(csv_file,excel_file):
    print (f'Converting CSV -> {csv_file} to Excel -> {excel_file}...')
    try: 
        read_file = pd.read_csv (csv_file, delimiter=";")
        writer = pd.ExcelWriter (excel_file, engine='xlsxwriter')
        read_file.to_excel (writer, sheet_name='Sheet1', index = None, header = True)

        workbook = writer.book
        worksheet1 = workbook.get_worksheet_by_name('Sheet1')
        worksheet1.autofilter('A1:G1')
        worksheet1.freeze_panes(1, 0)
        workbook.close()
    except FileNotFoundError:
        print(f"File Not Found Error: ./{csv_file}")
        exit()


#AllPairs mas Bitcoin, Gold, Index
symbols = ['AUDCAD','AUDCHF','AUDJPY','AUDNZD','AUDUSD','CADCHF','CADJPY','CHFJPY','EURAUD','EURCAD','EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','GBPAUD','GBPCAD','GBPCHF','GBPJPY','GBPNZD','GBPUSD','NZDCAD','NZDCHF','NZDJPY','NZDUSD','USDCAD','USDCHF','USDJPY', 'BTCUSD', 'XAUUSD', '.US500Cash', '.US30Cash']
#symbols = ['EURUSD']
timeframe = '5'
for symbol in symbols:
    symbol_news=f'{symbol}-News.csv'
    symbol_news_Excel=f'{symbol}-News.xlsx'
    convertToExcel(symbol_news, symbol_news_Excel)
