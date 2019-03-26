from binance.client import Client
from config import api_key, api_secret
import binance_constants
import pandas as pd


"""
This file is for generating data.
"""

# low, high, open, close, volume
# 0.000011645
OPEN_TIME_IDX = 0
OPEN_IDX = 1
HIGH_IDX = 2
LOW_IDX = 3
CLOSE_IDX = 4
VOLUME_IDX = 5


def get_data_helper(client, symbol, interval, start_str, end_str):
  """
  :param start_str: Start date string in UTC format or timestamp in milliseconds
  """
  data = client.get_historical_klines(
      symbol=symbol, interval=interval, start_str=start_str, end_str=end_str)
  data = list(map(lambda x: [int(x[OPEN_TIME_IDX]/1000), float(x[LOW_IDX]), float(x[HIGH_IDX]),
    float(x[OPEN_IDX]), float(x[CLOSE_IDX]), float(x[VOLUME_IDX])], data))  # opentime open high low close volume
  return data



def get_data(client, symbol, interval, start_str, end_str, output_file='out.pkl', req_size=86400):
  offset = req_size  ## one day at a time
  start_str = int(int(start_str)/1000)
  end_str = int(int(end_str)/1000)
  data = []
  for i in range(int((end_str - start_str)/offset)): # non-inclusive end date [start_day - end_day)
    # print(start_str, end_str, offset, i, start_str + (i * offset), start_str + ((i + 1) * offset))
    segment = get_data_helper(client, symbol, interval, str((start_str + (i * offset)) * 1000), str((start_str + ((i + 1) * offset))  * 1000))
    print("Fetching Segment: ", i)
    data += segment
  return data

def data_to_csv(data, fname='out.pkl'):
  labels = ['time', 'low', 'high', 'open', 'close', 'volume']
  df = pd.DataFrame.from_records(data, columns=labels)
  df.to_csv(fname, index=False)

def example():
  symbol = 'BTCUSDT'
  start_str = '1529400720000' # BINANCE API uses milliseconds
  end_str   = '1529573520000'
  client = Client(api_key, api_secret)
  data = get_data(client, symbol, binance_constants.KLINE_INTERVAL_12HOUR, start_str, end_str, output_file='tester.pkl', req_size=86400)
  data_to_csv(data, 'BTC-USD.csv')
  print(data)

if __name__ == "__main__":
  example()
