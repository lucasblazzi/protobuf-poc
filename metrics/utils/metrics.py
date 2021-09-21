
class Metrics:
    def __init__(self, request) -> None:
        self.ticker = request["ticker"]
        self.start_date = request["startDate"]
        self.end_date = request["endDate"]
        self.metric = request["metric"]

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

    def get_metric(self, data):
        result = getattr(self, self.metric)(data)
        return result.to_dict()
