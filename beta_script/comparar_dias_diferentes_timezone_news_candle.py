#Scritp para comparar dias y horarios de diferentes timezone que son el mismo dia y horarios
#https://pharos.sh/comparacion-de-fechas-y-horas-en-python-con-y-sin-zonas-horarias/
from datetime import datetime
import pytz

# Create timezone objects for different parts of the world
tz_candle = pytz.timezone("Europe/Helsinki")    #Roboforex
tz_news= pytz.timezone('US/Eastern')    #Noticias


# Year, Month, Day, Hour, Minute, Second
datetime_candle = datetime(2022, 10, 13, 15, 30, 0)
datetime_news = datetime(2022, 10, 13, 8, 30, 0)

# Localize the given date, according to the timezone objects
date_with_timezone_candle = tz_candle.localize(datetime_candle)
date_with_timezone_news = tz_news.localize(datetime_news)

# These are now, effectively no longer the same *date* after being localized
print(date_with_timezone_candle)
print(date_with_timezone_news)

if (date_with_timezone_candle == date_with_timezone_news):
    print("Son Iguales")


diff_date = date_with_timezone_news - date_with_timezone_candle
print(diff_date)
print(diff_date.total_seconds())

