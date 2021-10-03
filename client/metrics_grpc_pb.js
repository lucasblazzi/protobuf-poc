// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var metrics_pb = require('./metrics_pb.js');

function serialize_MetricsRequest(arg) {
  if (!(arg instanceof metrics_pb.MetricsRequest)) {
    throw new Error('Expected argument of type MetricsRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_MetricsRequest(buffer_arg) {
  return metrics_pb.MetricsRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_MetricsResponse(arg) {
  if (!(arg instanceof metrics_pb.MetricsResponse)) {
    throw new Error('Expected argument of type MetricsResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_MetricsResponse(buffer_arg) {
  return metrics_pb.MetricsResponse.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_PricesRequest(arg) {
  if (!(arg instanceof metrics_pb.PricesRequest)) {
    throw new Error('Expected argument of type PricesRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_PricesRequest(buffer_arg) {
  return metrics_pb.PricesRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_PricesResponse(arg) {
  if (!(arg instanceof metrics_pb.PricesResponse)) {
    throw new Error('Expected argument of type PricesResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_PricesResponse(buffer_arg) {
  return metrics_pb.PricesResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var MetricsService = exports.MetricsService = {
  getMetrics: {
    path: '/Metrics/GetMetrics',
    requestStream: false,
    responseStream: false,
    requestType: metrics_pb.MetricsRequest,
    responseType: metrics_pb.MetricsResponse,
    requestSerialize: serialize_MetricsRequest,
    requestDeserialize: deserialize_MetricsRequest,
    responseSerialize: serialize_MetricsResponse,
    responseDeserialize: deserialize_MetricsResponse,
  },
  getPrices: {
    path: '/Metrics/GetPrices',
    requestStream: false,
    responseStream: false,
    requestType: metrics_pb.PricesRequest,
    responseType: metrics_pb.PricesResponse,
    requestSerialize: serialize_PricesRequest,
    requestDeserialize: deserialize_PricesRequest,
    responseSerialize: serialize_PricesResponse,
    responseDeserialize: deserialize_PricesResponse,
  },
};

exports.MetricsClient = grpc.makeGenericClientConstructor(MetricsService);
