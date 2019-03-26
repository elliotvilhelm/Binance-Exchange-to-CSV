## Binance Data Fetcher
Binance Exchange data to .csv. Iterates over date range using `req_size` step. Makes a bunch of requests, builds up a python object, converts object to a pandas `DataFrame` and saves to a `.csv`.


### Format
 Columns:
 ```
 ['time', 'low', 'high', 'open', 'close', 'volume']
 ```

### Execution
In the following example the `req_size` is 1 day so each API request will fetch 1 day of day. The `interval` is 12 Hours. This means each request should return 2 data points. Our start date and end date are given in milliseconds UNIX time. They are exactly two days apart `06/19/2018 @ 9:32am (UTC)` and `06/21/2018 @ 9:32am (UTC)`. 2 days, 12 hour intervals gives us 4 data points. Each of dimension 6 in the format described above.

```python
def example():
  symbol = 'BTCUSDT'
  start_str = '1529400720000' # BINANCE API uses milliseconds
  end_str   = '1529573520000'
  client = Client(api_key, api_secret)
  data = get_data(client, symbol, binance_constants.KLINE_INTERVAL_12HOUR, start_str, end_str, output_file='tester.pkl', req_size=86400)
  data_to_csv(data, 'BTC-USD.csv')
  ```
  ```
  Fetching Segment:  0
  Fetching Segment:  1
  [
      [1529409600, 6653.0, 6841.74, 6726.11, 6741.21, 13170.313863],
      [1529452800, 6551.81, 6745.06, 6740.0, 6626.61, 12326.407427],
      [1529496000, 6572.0, 6817.23, 6626.6, 6761.51, 14033.345025],
      [1529539200, 6680.0, 6795.0, 6763.21, 6732.85, 12833.964411]
  ]
```

### Remarks
I plan to write a CLI for this.