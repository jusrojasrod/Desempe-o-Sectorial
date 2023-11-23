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
import sectors


def run_strategy(sector, end, start,
                 tickers, fig_path, column_name='Close',
                 showFig=False,
                 figure=False):
    """
    """

    # ================ Sectorial componets =====================

    # 1. Download data
    df = yf.download(tickers, start=start, end=end, interval="1wk")

    # select column_name data
    df = df[column_name]

    # Compute returns
    returns = df.pct_change()

    # current row data
    last_row, val_max, val_min = tools.currentRow(returns)

    # folder's label
    week_date = str(last_row.name).split(" ")[0]

    # Select best and worst ETFs
    selection_ = tools.selection(last_row, n=10)

    if figure:
        # ## Plot
        # Matrix formation
        new_names, new_array = plot.matrix_to_plot(selection_)

        # Plot
        plot.heatmap(values=new_array, labels=new_names,
                     max_=val_max, min_=val_min, sector=sector, show=showFig,
                     path=week_date)

    else:
        path = tools.create_dir(existing_directory="ETFs/results",
                                new_folder=week_date)
        selection_.to_excel(f"{path}/{sector}.xlsx")

    return selection_


def run_strategy_sectors(end, start,
                         fig_path, column_name='Close',
                         showFig=False,
                         figure=False):
    # =================== Sectors ==============================

    ETF_sectors = sectors.ETF_sectors
    tickers = [i for i in ETF_sectors.keys()]

    # Download data
    sectorsETF = yf.download(tickers, start=start, end=end, interval="1wk")
    sectors_df = sectorsETF[column_name]

    # Returns
    sector_returns = sectors_df.pct_change()

    # select last row (current one)
    last_sec_ret, *_ = tools.currentRow(sector_returns)

    # folder's label
    week_date = str(last_sec_ret.name).split(" ")[0]

    # Plot sectors
    if figure:
        plot.plot_bar_sectors(x=last_sec_ret.index,
                              y=(last_sec_ret.values*100).round(2),
                              show=showFig,
                              path=week_date)

    else:
        path = tools.create_dir(existing_directory="ETFs/results",
                                new_folder=week_date)
        last_sec_ret.to_excel(f"{path}/sectorial.xlsx")
    # ==================================================================


if __name__ == "__main__":

    # Start timer
    start_time = time.time()

    # setup
    folderPath_rsrc = '/ETFs/Resources/'
    folderPath_results = '/ETFs/results/'
    pictures = '/Pictures/'
    cwd = os.getcwd()
    path_rsrc = cwd + folderPath_rsrc
    path_results = cwd + folderPath_results
    path_pictures = cwd + pictures
    # read data
    ETFs = pd.read_excel(path_rsrc + "ETF.xlsx")

    end_ = date.today()  # yyyy-mm-dd
    if end_.day == 31:
        start_ = datetime(end_.year, end_.month - 1, 30)
    else:
        start_ = datetime(end_.year, end_.month - 1, end_.day)

    # Strategy [component sectors]
    for sector in ETFs.columns:
        print(f"---> {sector}")
        print(run_strategy(sector=sector, end=end_, start=start_,
                           tickers=ETFs[sector].dropna().to_list(),
                           figure=False,
                           column_name='Close',
                           fig_path=str(start_).split(" ")[0]))
        print("="*100)

    # Strategy for sectors itself
    run_strategy_sectors(end=end_, start=start_,
                         column_name='Close',
                         showFig=False,
                         figure=False,
                         fig_path=str(start_).split(" ")[0])

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)
