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

class Bot1:
    def __init__(self, start_ts, buy_hour):  
        self.positions = []
        self.positions_val = 0.0
        self.account = 100.0
        self.start_time = ts_to_localtime(start_ts)
        self.last_ts = start_ts
        self.last_worth = self.worth()
        self.twr = 1.0
        self.accu_t = 0
        self.buy_hour = buy_hour

    def interest_rate(self):
        part_of_year = float(self.accu_t) / float(365.0*24.0*60.0*60.0)
        
        return (self.twr ** (1/part_of_year) - 1.0) * 100

    def worth(self):
        return (self.account+self.positions_val)

    def run(self, kline):
        dt = ts_to_localtime(kline[0])
        open_c = kline[1]

        if dt.hour == self.buy_hour and dt.minute ==0 and dt.second ==0:
            val = 10
            self.account = self.account - val
            self.positions.append(
                val/open_c
            )
        
        if dt.hour == 16 and dt.minute ==0 and dt.second ==0:
            val = 0
            for i in self.positions:
                val += i * open_c
        
            self.positions = []
            self.account += val
        
        self.positions_val = 0.0
        for i in self.positions:
            self.positions_val += i * open_c

        # step end

        delta_ts = kline[0] - self.last_ts
        self.last_ts = kline[0]

        delta_yield = (self.worth() - self.last_worth)/ self.last_worth + 1.0
        self.last_worth = self.worth()

        self.twr *= delta_yield  
        self.accu_t += delta_ts 

klines = pickle.load(open("bdcbtc.pickle","rb"))

start_ts = klines[0][0]
end_ts = ts_to_localtime(klines[-1][6])
start_time = ts_to_localtime(start_ts)
print("first klines set opens at: %s"%( start_time))
print(" last klines set closes at: %s"%( end_ts))

bots = [
    Bot1(start_ts, 6), 
    Bot1(start_ts, 7), 
    Bot1(start_ts, 8)
]

bot_ir = []
for i in bots:
    bot_ir.append([])

for idx, b in enumerate(bots):
    for k in klines[1:]:
        b.run(k)
        bot_ir[idx].append(b.interest_rate())

open_t = [(i[0]-start_ts)/60.0/60.0/24.0 for i in klines]

fig, ax = plt.subplots(1)
for i in bot_ir:
    ax.plot(open_t[1:], i)

ax.set_title("Annualized TWR")
ax.set_xlabel("Days")
ax.set_ylabel("%")
plt.show()
