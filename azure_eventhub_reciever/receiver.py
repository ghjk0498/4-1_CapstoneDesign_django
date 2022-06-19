import asyncio
import datetime
import random
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import TimeSeriesPoint, DetectRequest, TimeGranularity, AnomalyDetectorError
from azure.core.credentials import AzureKeyCredential
import socket
import threading
import csv
import SocketServer

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

# Configuration
with open("../key_value.keys") as f:
    keys = json.load(f)

anomaly_detector_key = keys["anomaly_detector_key"]
anomaly_detector_endpoint = keys["anomaly_detector_endpoint"]
weight = [1, 1, 1, 1]  # weight for EMA
ema_period = 5

def request_anomaly(request):
    print("request_anomaly")
    # print('Detecting the anomaly status of the latest data point.')
    client = AnomalyDetectorClient(AzureKeyCredential(anomaly_detector_key), anomaly_detector_endpoint)

    response = None
    try:
        response = client.detect_last_point(request)
        #response = client.detect_entire_series(request)
    except KeyboardInterrupt as e:
        pass
    except AnomalyDetectorError as e:
        print('Error code: {}'.format(e.error.code), 'Error message: {}'.format(e.error.message))
    except Exception as e:
        print(e)

    if response is None:
        return 'exit'

    # print(response)
    if response.is_anomaly:
        print('The latest point is detected as anomaly.')
    else:
        pass
        # print('The latest point is not detected as anomaly.')
    return response


def series_init(df, w):
    # w is a weight for EMA
    series = []
    df["ema"] = df["value"].rolling(ema_period).mean()
    df = df.dropna()
    for index, row in df.iterrows():
        # caution! it's not an exponential
        series.append(TimeSeriesPoint(timestamp=row[0], value=row[2]))
    return series


def new_value_processor(value_as_row, df, series):
    time, new_value = value_as_row
    ema_value = (sum(df["value"].to_list()[-ema_period+1:]) + new_value) / ema_period

    series.append(TimeSeriesPoint(timestamp=time, value=ema_value))
    request = DetectRequest(series=series, granularity=TimeGranularity.PER_SECOND)
    response = request_anomaly(request)
    print(response)
    print(value_as_row + [ema_value, response.is_anomaly])
    df.loc[len(df)] = value_as_row + [ema_value, response.is_anomaly]

    df.to_csv("sensor_v1.csv", index=False)
    df.to_csv("MEDIA/Anomaly_Simulation_with_tzinfo_v0.csv", index=False)
    return response






def init_receive():
    data_file = pd.read_csv("sensor_v1.csv", parse_dates=['time'], index_col=False)  # past data
    data_file['time'] = pd.to_datetime(data_file['time']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    series = series_init(data_file, weight)  # list to send Azure Anomaly Detector

    return data_file, series

# data load
def receive(msg, data_file, series):
    ts = msg.split(" ")
    time = ts[0] + "T" + ts[1] + "Z"
    value = float(ts[2])
    try:
        sensor_data = [time, value]
        new_value_processor(sensor_data, data_file, series)
    except KeyboardInterrupt as e:
        print(e)

if __name__ == '__main__':
    data_file, series = init_receive()
    receive("2022-06-17 11:50:22 15", data_file, series)



