import grpc
from concurrent import futures
from datetime import datetime

import yfinance as yf
import metrics_pb2 as pbuff_metric
import metrics_pb2_grpc as pbuff_metric_grpc


def get_date(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def get_prices(request):
    ticker = yf.Ticker(f"{request.ticker}.SA")
    historic = ticker.history(start=get_date(request.startDate), end=get_date(request.endDate))
    print("______________________________________")
    print(f"RAW PRICES RESULT \n{historic}")
    return historic.to_dict()


def response_builder(result):
    prices_response = pbuff_metric.PricesResponse()
    for k, v in result["Close"].items():
        price_value = prices_response.values.add()
        price_value.x = int(k.value / 10**9)
        price_value.y = v
    return prices_response


def setup():
    listener = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pbuff_metric_grpc.add_MetricsServicer_to_server(MetricsServicer(), listener)
    listener.add_insecure_port(f"[::]:777")
    listener.start()
    print("Server is running on localhost:777")
    listener.wait_for_termination()


class MetricsServicer(pbuff_metric_grpc.MetricsServicer):
    def GetPrices(self, request, context):
        result = get_prices(request)
        print("______________________________________")
        print(f"RAW PRICES RESULT \n{result}")
        response = response_builder(result)
        print("______________________________________")
        print(f"RETURNING PRICES \n{result}")
        return response

setup()
