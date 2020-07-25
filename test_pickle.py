import pickle
import datetime
import pytz
import time
import numpy
import pprint
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from datetime import timezone

local_tz = pytz.timezone('Europe/Berlin')

def ts_to_localtime(ts):
    dt = datetime.datetime.fromtimestamp(int(ts), pytz.utc)
    return local_tz.normalize(dt)

def localtime_to_ts(lt):
    a = local_tz.localize(lt)
    return int(a.timestamp())

def extract(klines, startdt, enddt):
    start_ts = localtime_to_ts(startdt)
    end_ts = localtime_to_ts(enddt)
    return [i for i in klines if i[0]>= start_ts and i[0]<=end_ts]

klines = pickle.load(open("bdcbtc.pickle","rb"))

newset_kline_dt = ts_to_localtime(klines[-1][6])
oldest_kline_dt = ts_to_localtime(klines[0][0])
print("first klines set opens at: %s"%( oldest_kline_dt))
print(" last klines set closes at: %s"%( newset_kline_dt))

start_date = oldest_kline_dt.date() + datetime.timedelta(days=1)
end_date = newset_kline_dt.date()
no_of_days = (end_date-start_date).days 

set_8oc = set()
set_16oc = set()
for single_date in (start_date + datetime.timedelta(days=n) for n in range(no_of_days)):
    set_8oc.add(
        localtime_to_ts(datetime.datetime.combine(single_date, datetime.time(hour=8, minute=0, second=0)))
    )
    set_16oc.add(
        localtime_to_ts(datetime.datetime.combine(single_date, datetime.time(hour=16, minute=0, second=0)))
    )

klines_8 =  [i for i in klines if i[0] in set_8oc]
klines_16 = [i for i in klines if i[0] in set_16oc]
klines_8_dates  = set([ts_to_localtime(i[0]).date() for i in klines_8])
klines_16_dates = set([ts_to_localtime(i[0]).date() for i in klines_16])

# remove datasets which are only in one sample
only_in_8 = klines_8_dates- klines_16_dates
only_in_16 = klines_16_dates- klines_8_dates

klines_8 = [i for i in klines_8 if ts_to_localtime(i[0]).date() not in only_in_8]
klines_16 = [i for i in klines_16 if ts_to_localtime(i[0]).date() not in only_in_16]

dt_8 = [[i[0], ts_to_localtime(i[0]).strftime("%d.%m.%y %H:%M:%S %z")] for i in klines_8]
dt_16 = [[i[0], ts_to_localtime(i[0]).strftime("%d.%m.%y %H:%M:%S %z")] for i in klines_16]

klines_day = [[
    ts_to_localtime(a[0]),
    ts_to_localtime(b[0]), 

    a[1], 
    b[1], 
    b[1]/a[1]-1.0
] for a,b in zip(klines_8, klines_16)]
open_t = [i[0] for i in klines_8]
yield_ = [i[1] for i in klines_8]

print (tabulate(klines_day))


yield_of_strategy = (numpy.average([i[4] for i in klines_day]) ) * 100.0

print ("Yield of strategy: %f %%"%(yield_of_strategy))
open_t = [i[0] for i in klines_day]
yield_ = [(numpy.average([i[4] for i in klines_day[:idx]]) ) * 100.0 for idx, i in enumerate(klines_day)]

plt.plot(open_t, yield_)
plt.show()