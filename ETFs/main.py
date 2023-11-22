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
import os

import yfinance as yf

from datetime import date
from datetime import datetime
import time

import plot
import tools


def run_strategy(sector, end, start,
                 tickers, fig_path, column_name='Close',
                 showFig=False):
    """
    """
    # 1. Download data
    df = yf.download(tickers, start=start, end=end, interval="1wk")

    # select column_name data
    df = df[column_name]

    # Compute returns
    returns = df.pct_change()

    # current row data
    last_row, val_max, val_min = tools.currentRow(returns)

    # Select best and worst ETFs
    selection_ = tools.selection(last_row, n=10)

    # ## Plot
    # Matrix formation
    new_names, new_array = plot.matrix_to_plot(selection_)

    # Plot
    plot.heatmap(values=new_array, labels=new_names,
                 max_=val_max, min_=val_min, sector=sector, show=showFig,
                 path=fig_path)

    return selection_


if __name__ == "__main__":

    # Start timer
    start_time = time.time()

    # setup
    folderPath_rsrc = '/ETFs/Resources/'
    folderPath_results = '/ETFs/Results/'
    pictures = '/Pictures/'
    cwd = os.getcwd()
    path_rsrc = cwd + folderPath_rsrc
    path_results = cwd + folderPath_results
    path_pictures = cwd + pictures
    # read data
    ETFs = pd.read_excel(path_rsrc + "ETFs list.xlsx")

    end_ = date.today()  # yyyy-mm-dd
    if end_.day == 31:
        start_ = datetime(end_.year, end_.month - 1, 30)
    else:
        start_ = datetime(end_.year, end_.month - 1, end_.day)

    # execute strategy
    for sector in ETFs.columns:
        print(f"---> {sector}")
        print(run_strategy(sector=sector, end=end_, start=start_,
                           tickers=ETFs[sector].dropna().to_list(),
                           column_name='Close',
                           fig_path=str(start_).split(" ")[0]))
        print("="*100)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)
