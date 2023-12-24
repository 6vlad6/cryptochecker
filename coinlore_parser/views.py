import json

import requests

class CoinloreParser:
    def __init__(self, tickers: list, tickers_url, ticker_url):
        self.tickers = tickers
        self.tickers_url = tickers_url
        self.ticker_url = ticker_url


    def get_tickers(self):
        tickers = self.tickers
        tickers_ids = [0] * len(tickers)

        tickers_data = []

        found_tokens = 0

        res = []

        i = 0
        while True:

            r = requests.get(self.tickers_url.format(i))

            tickers_data = json.loads(r.text)['data']

            for item in tickers_data:
                if str(item['symbol']) in tickers:

                    indx = tickers.index(str(item['symbol']))

                    tickers_ids[indx] = item['id']

                    found_tokens += 1

            if found_tokens == len(tickers_ids):
                break

            i += 100


        for i in range(len(tickers)):
            res.append([tickers[i], tickers_ids[i]])

        return res

    def get_tickers_prices(self):
        data = self.get_tickers()

        for item in data:
            ticker_id_cl = item[1]

            r = requests.get(self.ticker_url.format(ticker_id_cl))
            ticker_data = json.loads(r.text)[0]

            price = ticker_data['price_usd']

            item.append(price)

        return data
