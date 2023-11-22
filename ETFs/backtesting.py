# import libraries
import pandas as pd
import time
import os
from datetime import timedelta

from tools import dates_list
import main


def backtesting(years=0, months=0, days=0):
    """
    """

    # setup
    folderPath_rsrc = '/ETFs/Resources/'
    cwd = os.getcwd()
    path_rsrc = cwd + folderPath_rsrc

    # read data
    ETFs = pd.read_excel(path_rsrc + "ETFs list.xlsx")

    dates = dates_list(years=years, months=months, days=days)
    # Strategy for sectors itself
    for date in dates:
        end = date + timedelta(weeks=3)
        main.run_strategy_sectors(end=end, start=date,
                                  column_name='Close',
                                  showFig=False,
                                  fig_path=str(date).split(" ")[0])

    for date in dates:
        print("\n", f"|-> Date: [{date}] Begin execution", "\n")
        end = date + timedelta(weeks=3)
        # Strategy [component sectors]
        for sector in ETFs.columns:
            print("\t", f"--> {sector}")
            print(main.run_strategy(sector=sector, end=end, start=date,
                                    tickers=ETFs[sector].dropna().to_list(),
                                    column_name='Close',
                                    fig_path=str(date).split(" ")[0]))
            print("\t", "="*100)


if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # backtesting
    backtesting(years=2)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print("Elapsed time: ", elapsed_time)
