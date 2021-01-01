import backtrader as bt
from datetime import datetime
from Model import calculator

startDay = datetime(2020, 11, 1)
endDay = datetime(2020, 12, 11)

class Regression(bt.Strategy):
	def next(self):
		self.currentDay = self.datetime.datetime(ago=0)
		self.price = self.datas[0].close
		self.max_stake = self.broker.getvalue() / self.price

		self.bounds = calculator(self.currentDay)
		self.TP = self.bounds[0]
		self.SL = self.bounds[1] 

		if not self.position:
			if(self.TP != 0 and self.SL != 0):
				self.buy(size=round(self.max_stake, 0))
		elif(self.price >= self.TP or self.price <= self.SL): 
			self.close()

		print('Testing: ' + str(self.currentDay.strftime('%Y-%m-%d')))	


if __name__ == '__main__':
	cerebro = bt.Cerebro()
	cerebro.addstrategy(Regression)
	data = bt.feeds.YahooFinanceData(dataname='SPY', 
									 fromdate=startDay,
									 todate=endDay)

	cerebro.adddata(data)
	cerebro.run()
	cerebro.plot()


'''
Had to do the following for backtrader to work:
pip uninstall matplotlib
pip install matplotlib==3.2.2
'''