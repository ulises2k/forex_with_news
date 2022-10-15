#Scritp para comparar dias y horarios de diferentes timezone que son el mismo dia y horarios
from datetime import datetime
import pytz

# Create timezone objects for different parts of the world
tz_ny= pytz.timezone('America/New_York')
tz_arg = pytz.timezone("America/Argentina/Buenos_Aires")

# Year, Month, Day, Hour, Minute, Second
datetime_ny = datetime(2022, 10, 13, 8, 30, 0)
datetime_arg = datetime(2022, 10, 13, 9, 30, 0)

# Localize the given date, according to the timezone objects
date_with_timezone_1 = tz_ny.localize(datetime_ny)
date_with_timezone_2 = tz_arg.localize(datetime_arg)

# These are now, effectively no longer the same *date* after being localized
print(date_with_timezone_1) # 2010-04-20 23:30:00-04:00
print(date_with_timezone_2) # 2010-04-20 23:30:00+01:00

print(date_with_timezone_1 == date_with_timezone_2)