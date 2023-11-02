import requests
import pandas as pd

import os
import time
import concurrent.futures
import threading
from functools import partial

import config

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def downloadTicker(ticker, start, end, period='d', filter=None):
    """
    """
    cwd = os.getcwd()
    folderPath_rsrc = '/Resources/'
    path_results = cwd + folderPath_rsrc

    _BASE_URL_ = f'https://eodhd.com/api/eod/{ticker}'

    payload = {'api_token': config.api_key,
               'period': period,
               'from': start,
               'to': end,
               'fmt': 'json',
               'filter': filter}
    session = get_session()
    r = session.get(_BASE_URL_, params=payload)
    data = r.json()
    df = pd.DataFrame(data)
    # df.to_pickle(f'{path_results}{ticker.upper()}')
    df.to_excel(f'{path_results}{ticker.upper()}.xlsx')
    # print(f"{ticker}: {r}")


def downloadAllTickers(tickers, start, end):
    """
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(partial(downloadTicker, start=start, end=end), tickers)


if __name__ == "__main__":

    start = '2023-05-01'
    end = '2023-05-02'
    tickers = ["CHIS", "CLIX"]

    start_time = time.time()
    downloadAllTickers(tickers, start=start, end=end)
    duration = time.time() - start_time
    print(f"Elapsed time: {duration:.2f} seconds")

    # cwd = os.getcwd()
    # folderPath_rsrc = '/ETFs/Resources/'
    # path_results = cwd + folderPath_rsrc
    # # data = pd.read_pickle(f"{path_results}{tickers[0]}")

    # print()
