import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.linear_model
import scipy.stats as stats
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

api_key = '8FIYTT49ZEZT2GV5'
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='SPY', outputsize = 'full')

def probability(price, prediction, dev):
	probability = 0
	zscore = float((price - prediction) / dev)
	cdf = stats.norm.cdf(zscore)
	if(cdf <= .5):
		probability = cdf
	elif(cdf >= .5):
		probability = 1-cdf
	return probability

def calculator(currentDay):
	global data, meta_data
	Data = data

	Data = Data[(Data.index < currentDay)]
	Data = Data.reset_index()
	Data['date'] = Data['date'].dt.strftime('%Y-%m-%d')
	Data['index'] = list(reversed(range(0, len(Data))))

	X = np.c_[Data['index']]
	Y = np.c_[Data['4. close']]
	X = [x[0] for x in X]
	Y = [x[0] for x in Y]

	model = np.polyfit(X, Y, 3)
	std = np.std(Y)
	todayDate = X[0]
	currentPrice = Y[0]
	std = np.std(Y)
	dateTestBench = [3, 5, 7, 11, 13, 17, 19]
	dateTestBench = [7] #Kept this way to speed up backtesting

	orderTP = 0
	orderSL = 0
	orderRank = 0

	for testDay in dateTestBench:
		testDate = todayDate + testDay
		daysFromToday = testDate - todayDate 
		testPrediction = np.polyval(model, testDate) 
		desiredRange = Y[0:daysFromToday]
		minRisk = np.std(desiredRange)

		testList = list(range(-100, 101))
		testList = [testPrediction + (std * (x / 100)) for x in testList]
		profits = [x for x in testList if x > currentPrice]
		losses = [x for x in testList if x < currentPrice]

		currentRank = 0
		bestRank = 0
		bestTP = 0
		bestSL = 0

		for i in profits:
			for j in losses:
				reward = i - currentPrice
				risk = currentPrice - j
				rewardrisk = reward / risk
				winrate =  probability(i, testPrediction, std) / (probability(i, testPrediction, std) + probability(j, testPrediction, std))
				currentRank = winrate * reward

				if(currentRank > bestRank):
					if(risk > minRisk/2 and winrate > (1/3) and rewardrisk > 2): 
						if((j > currentPrice - minRisk) and (i < currentPrice + minRisk*2)): 
							bestRank = currentRank
							bestTP = i
							bestSL = j


		if(bestRank > orderRank):
			orderRank = bestRank
			orderTP = bestTP
			orderSL = bestSL
	
	return [orderTP, orderSL]