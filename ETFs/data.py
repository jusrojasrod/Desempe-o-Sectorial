import config
import requests
import pandas as pd

import os
import time


def downloadData(ticker, start, end, period='d'):
    """
    """
    cwd = os.getcwd()
    folderPath_rsrc = '/ETFs/Resources/'
    path_results = cwd + folderPath_rsrc

    _BASE_URL_ = f'https://eodhd.com/api/eod/{ticker}'

    payload = {'api_token': config.api_key,
               'period': period,
               'from': start,
               'to': end,
               'fmt': 'json'}

    session = requests.Session()
    r = session.get(_BASE_URL_, params=payload)
    data = r.json()
    df = pd.DataFrame(data)
    df.to_pickle(f'{path_results}{ticker.upper()}')


if __name__ == "__main__":

    start = '2023-05-01'
    end = '2023-05-02'
    ticker = 'TSLA'

    start_time = time.time()
    downloadData(ticker, start, end)
    duration = time.time() - start_time
    print(f"Elapsed time: {duration:.2f} seconds")
    cwd = os.getcwd()
    folderPath_rsrc = '/ETFs/Resources/'
    path_results = cwd + folderPath_rsrc
    data = pd.read_pickle(f"{path_results}{ticker}")

    print(data)
