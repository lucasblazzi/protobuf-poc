import grpc
from concurrent import futures
from datetime import datetime
import os
from utils.metrics import Metrics

import metrics_pb2 as pbuff_metric
import metrics_pb2_grpc as pbuff_metric_grpc
from metrics_pb2_grpc import MetricsStub
from metrics_pb2 import PricesRequest
from google.protobuf.json_format import MessageToDict
import pandas as pd


prices_host = os.getenv("PRICES_HOST", "localhost")
channel = grpc.insecure_channel(f"[::]:777")
client = MetricsStub(channel)


def get_date(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def response_builder(request, result):
    print("______________________________________")
    print(f"RAW CALCULATED METRICS  \n{result}")
    metric_response = pbuff_metric.MetricsResponse()
    metric_response.startDate = get_date(list(result.keys())[0])
    metric_response.endDate = get_date(list(result.keys())[-1])
    metric_response.ticker = request["ticker"]
    metric_response.metric = request["metric"].capitalize().replace("_", " ")
    for k, v in result.items():
        metric_value = metric_response.values.add()
        metric_value.x = k
        metric_value.y = v
    return metric_response


def get_prices(request):
    prices_request = PricesRequest(
        ticker=request.ticker, startDate=request.startDate, endDate=request.endDate)
    print("______________________________________")
    print(f"REQUESTING PRICES \n{prices_request}")
    prices_response = client.GetPrices(prices_request)
    print("______________________________________")
    print(f"PRICES RECEIVED \n{prices_response}")
    return pd.DataFrame(MessageToDict(prices_response)["values"]).rename(columns={"y": "Close"}).set_index("x")


def setup():
    listener = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pbuff_metric_grpc.add_MetricsServicer_to_server(MetricsServicer(), listener)
    listener.add_insecure_port(f"[::]:666")
    listener.start()
    print("Server is running on localhost:666")
    listener.wait_for_termination()


class MetricsServicer(pbuff_metric_grpc.MetricsServicer):
    def GetMetrics(self, request, context):
        data = get_prices(request)
        request = MessageToDict(request)
        result = Metrics(request).get_metric(data)
        response = response_builder(request, result)
        print("______________________________________")
        print(f"RETURNING METRICS  \n{response}")
        return response

setup()