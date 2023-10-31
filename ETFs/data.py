import config
import requests
import pandas as pd


def downloadData():
    pass


ticker = 'tsla'
start = '2020-01-05'
end = '2020-02-05'

_BASE_URL_ = f'https://eodhd.com/api/eod/{ticker}'

payload = {'api_token': config.api_key,
           'period': 'd',
           'from': start,
           'to': end,
           'fmt': 'json'}

r = requests.get(_BASE_URL_, params=payload)
data = r.json()
df = pd.DataFrame(data)

print(df)
