const grpc = require('grpc');
const messages = require('./metrics_pb');
const services = require('./metrics_grpc_pb');

function main() {
  const client = new services.MetricsClient(
    'localhost:666', grpc.credentials.createInsecure()
  );

  const metricsRequest = new messages.MetricsRequest();
  metricsRequest.setTicker("BPAC11");
  metricsRequest.setStartdate(1600392413);
  metricsRequest.setEnddate(1631928413);
  metricsRequest.setMetric(1);
  console.log(metricsRequest);

  client.getMetrics(metricsRequest, function (err, response) {
    if (err) {
      console.log('this thing broke!', err);
    } else {
      console.log(response);
      console.log('response from python:', response);
    }
  })
}

main();