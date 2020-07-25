import pickle
import pytz
from datetime import datetime
from datetime import timezone
from binance.client import Client
api_key="rCXtmePtxRJkgFwnov2oYfE11eOaNs8U1IoVlgBYB9bt67feIEGYkCNPM5I4Nczt"
api_secret="WEjJXjg6Ppt0Jhvbm8qUvVQXKgesktMaMtTMfoNILigZXYTmsHSTQusHLjXbeLyd"


client = Client(api_key, api_secret)
server_ts = client.get_server_time()['serverTime']
server_time = datetime.fromtimestamp(int(server_ts)/ 1000.0, pytz.utc)
local_tz = pytz.timezone('Europe/Berlin')
server_time = local_tz.normalize(server_time)
print("Server time: %s" %(server_time))
klines = client.get_historical_klines("BTCEUR", Client.KLINE_INTERVAL_1MINUTE , "1 Jan, 2020")
olines = []


for l in klines:
    p = list(l)

    p[0] = int(int(p[0]) / 1000) # Open time
    p[1] = float(p[1])      # Open
    p[2] = float(p[2])      # High
    p[3] = float(p[3])      # Low
    p[4] = float(p[4])      # Close
    p[5] = float(p[5])      # Volume
    p[6] = int(int(p[6] / 1000)) # Close time
    p[7] = float(p[7])      # Quote asset volume
    p[8] = int(p[8])        # Number of trades
    p[9] = float(p[9])      # Taker buy base asset volume
    p[10] = float(p[10])    # Taker buy quote asset volume   
    del p[11]               # ignore  
    olines.append(p)

#print(olines)
with open("bdcbtc.pickle","wb") as file:
    pickle.dump(olines, file)