import grpc
from concurrent import futures
from datetime import datetime

from utils.metrics import Metrics

import protobufpy.metrics_pb2 as pbuff_metric
import protobufpy.metrics_pb2_grpc as pbuff_metric_grpc
from google.protobuf.json_format import MessageToDict


def get_date(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def response_builder(request, result):
    metric_response = pbuff_metric.MetricsResponse()
    metric_response.startDate = get_date(list(result.keys())[0].timestamp())
    metric_response.endDate = get_date(list(result.keys())[-1].timestamp())
    metric_response.ticker = request["ticker"]
    metric_response.metric = request["metric"].capitalize()
    for k, v in result.items():
        metric_value = metric_response.values.add()
        metric_value.x = int(k.timestamp())
        metric_value.y = v
    return metric_response


def setup():
    listener = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pbuff_metric_grpc.add_MetricsServicer_to_server(MetricsServicer(), listener)
    listener.add_insecure_port("localhost:666")
    listener.start()
    print("Server is running on localhost:666")
    listener.wait_for_termination()


class MetricsServicer(pbuff_metric_grpc.MetricsServicer):
    def GetMetrics(self, request, context):
        print("Requested")
        metric_request = pbuff_metric.MetricsRequest()
        metric_request.ParseFromString(request.read())
        request = MessageToDict(metric_request)
        print(request)
        result = Metrics(request).get_metric()
        response = response_builder(request, result)
        return response.SerializeToString()


setup()