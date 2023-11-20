# Copyright 2023-2023 Juan Sebastian Rojas Rodriguez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import libraries
import pandas as pd
import numpy as np
import os

import yfinance as yf

from datetime import date
from datetime import datetime


def run_strategy(sector, column_name='Close'):
    """
    """
    # 1. Download data
    end_ = date.today()  # yyyy-mm-dd
    if end_.day == 31:
        start_ = datetime(end_.year, end_.month - 1, 30)
    else:
        start_ = datetime(end_.year, end_.month - 1, end_.day)

    data = yf.download(sector, start=start_, end=end_, interval="1wk")

    # select colmn_name data
    data = data[column_name]

    return data


if __name__ == "__main__":

    # setup
    folderPath_rsrc = '/ETFs/Resources/'
    folderPath_results = '/ETFs/Results/'
    cwd = os.getcwd()
    path_rsrc = cwd + folderPath_rsrc
    path_results = cwd + folderPath_results
    # read data
    ETFs = pd.read_excel(path_rsrc + "ETFs list.xlsx")

    for sector in ETFs.columns:
        print(run_strategy(sector=ETFs[sector].to_list()), column_name='Close')
        break
