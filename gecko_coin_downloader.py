import pandas as pd
import datetime as dt
from pathlib import Path
import pprint
from pycoingecko import CoinGeckoAPI
from retry_decorator import retry, logger
from requests.exceptions import HTTPError

pd.set_option("display.max_columns", 12)
pp = pprint.PrettyPrinter(indent=4)
client = CoinGeckoAPI()


class GeckoQuotes:
    start_date = 1262300400  # 2010_01_01
    end_date = int(dt.datetime.timestamp(dt.datetime.now()))
    quotes_folder = 'GeckoData'

    def __init__(self, ticker):
        self.ticker = ticker
        self.quotes = self.get_quotes()

    @retry(HTTPError, total_tries=5, initial_wait=10, backoff_factor=2, logger=logger)
    def get_quotes(self):
        return client.get_coin_market_chart_range_by_id(self.ticker, vs_currency='USD',
                                                        from_timestamp=self.start_date,
                                                        to_timestamp=self.end_date)

    def check_dir(self):
        path = Path(str(Path.cwd()) + '/' + self.quotes_folder)
        path.mkdir(exist_ok=True)

    def make_as_df(self):
        col_time = (t for t, _ in self.quotes['prices'])
        col_close = (cl for _, cl in self.quotes['prices'])
        col_market_cap = (cap for _, cap in self.quotes['market_caps'])
        col_vol = (vol for _, vol in self.quotes['total_volumes'])

        df = pd.DataFrame(data=zip(col_time, col_close, col_market_cap, col_vol),
                          columns=['date', *self.quotes.keys()]).set_index(keys='date')
        df.index = pd.to_datetime(df.index, unit='ms')
        df.index = df.index.date
        df.index.set_names('date', inplace=True)
        return df

    def quotes_to_csv(self):
        self.check_dir()
        self.make_as_df().to_csv(f'{self.quotes_folder}\\{self.ticker}_daily.csv')