var readline = require('readline');
const grpc = require('grpc');
const messages = require('./metrics_pb');
const services = require('./metrics_grpc_pb');

function main() {
  const client = new services.MetricsClient(
    'localhost:666', grpc.credentials.createInsecure()
  );

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question("TICKER: ", function(ticker) {
    const metricsRequest = new messages.MetricsRequest();
    metricsRequest.setTicker(ticker);
    metricsRequest.setStartdate(1632794884);
    metricsRequest.setEnddate(1635558836);
    metricsRequest.setMetric(1);
  
    client.getMetrics(metricsRequest, function (error, response) {
      if (error) {
        console.log("An error occurred! ", error);
      } else {
        console.log("getMetrics response received:\n", response);
      }
    })
  });

}

main();