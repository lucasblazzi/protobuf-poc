import yfinance as yf
from datetime import datetime


class Metrics:
    def __init__(self, request) -> None:
        self.ticker = request["ticker"]
        self.start_date = request["startDate"]
        self.end_date = request["endDate"]
        self.metric = request["metric"]

    @staticmethod
    def get_date(ts):
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    def get_data(self):
        ticker = yf.Ticker(f"{self.ticker}.SA")
        historic = ticker.history(start=self.get_date(self.start_date), end=self.get_date(self.end_date))
        print(historic.head(5))
        return historic

    @staticmethod
    def close(data):
        return data.Close

    @staticmethod
    def returns(data):
        return data.Close.pct_change().fillna(0)

    def cumulative_return(self, data):
        return self.returns(data).add(1).cumprod().sub(1)

    def drawdown(self, data):
        wealth_index = self.returns(data).add(1).cumprod()
        previous_peaks = wealth_index.cummax()
        return ((wealth_index - previous_peaks) / previous_peaks).fillna(0)

    def get_metric(self):
        data = self.get_data()
        result = getattr(self, self.metric)(data)
        return result.to_dict()
