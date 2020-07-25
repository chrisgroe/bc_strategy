import pickle
import datetime
import pytz
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import timezone

local_tz = pytz.timezone('Europe/Berlin')
def ts_to_localtime(ts):
    dt = datetime.datetime.fromtimestamp(int(ts), pytz.utc)
    return local_tz.normalize(dt)

def localtime_to_ts(lt):
    a = local_tz.localize(lt)
    return a.timestamp()

klines = pickle.load(open("bdcbtc.pickle","rb"))

print(" oldest klines set opens at: %s"%( ts_to_localtime(klines[0][0])))
print("newest klines set closes at: %s"%( ts_to_localtime(klines[-1][6])))
a_ts = localtime_to_ts(datetime.datetime(year=2020, month=6, day=1))
b_ts = localtime_to_ts(datetime.datetime(year=2020, month=6, day=30)) 
print(ts_to_localtime(a_ts), ts_to_localtime(b_ts))


day = [i for i in klines if i[0]>a_ts and i[6]<b_ts]

open_t = [i[0] for i in day]
open_p = [i[1] for i in day]


plt.plot(open_t, open_p)

plt.show()
