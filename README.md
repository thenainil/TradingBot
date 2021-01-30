PROJECT NAME: Trading Robot with Machine Learning

DESCRIPTION: A Python script where the trader receives the highest-probability stock trade of the week, daily. 

INSTALLATION: 
Just download.
Ensure python is installed in your computer.
-pip install any required libraries which the terminal asks at runtime.
*Special note for matplotlib, install version 3.2.2. The latest version is not yet supported by all the libraries used*

USAGE:
Run Strategy.py, it will backtest the program.

1. You can edit the range of days you can test between. Simply change the date in line 5 and line 6.
2. You can also edit the period outwards you want to test at (as in do you want to check the best trade a week from now, a month, etc). By default it is one week. To do this, in Model.py, change the number in line 43 to the desired number (in days).
3. You can also edit which symbol you want to use. To do so, in line 11 of Model.py and in line 30 of Strategy.py, change "SPY" into the ticker for the stock you want to use. By default, the S&P500 index is used. You are encouraged to use some sort of index or a stable, established company. Other companies could be too volatile to predict accurately, although you can clearly try.
