from flask import Flask, render_template, request
import grpc
import json
import plotly
import plotly.graph_objects as go
from datetime import datetime
import time
from metrics_pb2 import MetricsRequest, MetricTypes
from metrics_pb2_grpc import MetricsStub
import os

metrics_host = os.getenv("METRICS_HOST", "localhost")

app = Flask(__name__)
channel = grpc.insecure_channel(f"{metrics_host}:666")
client = MetricsStub(channel)


def get_unix_time(date):
    return int(time.mktime(datetime.strptime(date, "%d-%m-%Y").timetuple()))


def build_graph(metrics):
    x = [datetime.fromtimestamp(metric.x).strftime("%Y-%m-%d") for metric in metrics]
    y = [metric.y * 100 for metric in metrics]
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(color="white"),
        yaxis=dict(color="white", title="%"),
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/<ticker>/<start_date>/<end_date>")
def load_metric(ticker="BPAC11", start_date=1600392413, end_date=1631928413):
    start_date = get_unix_time(start_date)
    end_date = get_unix_time(end_date)

    app.logger.error(start_date)
    app.logger.error(end_date)
    app.logger.error(ticker)
    metric_request = MetricsRequest(
        ticker=ticker, startDate=start_date, endDate=end_date, metric=MetricTypes.cumulative_return
    )
    # metric_request = MetricsRequest(
    #     ticker="BPAC11", startDate=1600392413, endDate=1631928413, metric=MetricTypes.cumulative_return
    # )

    metrics_response = client.GetMetrics(metric_request)
    graph = build_graph(metrics_response.values)

    return render_template(
        "home.html",
        metric=metrics_response,
        plot=graph
    )