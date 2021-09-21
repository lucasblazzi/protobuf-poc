import protobufpy.metrics_pb2 as pbuff_metric
from datetime import datetime
import json


def get_date(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def create_mock_request():
    mock_request = pbuff_metric.MetricsRequest()
    mock_request.ticker = "ITSA4"
    mock_request.metric = 1
    mock_request.startDate = 842659516
    mock_request.endDate = 1631479603

    with open("mock_request", "wb") as f:
        f.write(mock_request.SerializeToString())


def json_response_builder(request, result):
    metric_response = dict()
    metric_response["startDate"] = get_date(list(result.keys())[0].timestamp())
    metric_response["endDate"] = get_date(list(result.keys())[-1].timestamp())
    metric_response["ticker"] = request["ticker"]
    metric_response["metric"] = request["metric"].capitalize()
    metric_response["values"] = []
    for k, v in result.items():
        metric_response["values"].append({"x": int(k.timestamp()), "y": v})
    with open('json_response.json', 'w') as outfile:
        json.dump(metric_response, outfile)
    return metric_response


def read_mock_response():
    mock_response = pbuff_metric.MetricsResponse()
    with open("mock_performance/1years", "rb") as f:
        mock_response.ParseFromString(f.read())
        print(mock_response)

def read_json_response():
    with open("json_response.json", "r") as f:
        r = json.load(f)
        print(r)