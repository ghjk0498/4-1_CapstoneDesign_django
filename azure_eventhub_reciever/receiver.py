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

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

# Configuration


def request_anomaly(request):
    print("request_anomaly")
    # print('Detecting the anomaly status of the latest data point.')
    client = AnomalyDetectorClient(AzureKeyCredential(anomaly_detector_key), anomaly_detector_endpoint)
    response = None
    try:
        response = client.detect_last_point(request)
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
    series = []
    for index, row in df.iterrows():
        # caution! it's not an exponential
        series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))
    return series





with open("../key_value.keys") as f:
    keys = json.load(f)
anomaly_detector_key = keys["anomaly_detector_key"]
anomaly_detector_endpoint = keys["anomaly_detector_endpoint"]
weight = [1, 1, 1, 1]  # weight for EMA
# data load
data = pd.read_csv("Anomaly Simulation with tzinfo.csv", parse_dates=['time'], index_col=False)  # past data
series = series_init(data, weight)  # list to send Azure Anomaly Detector

index = 0

def work():
    HOST = "220.66.115.161"
    PORT = 9998

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                ts = data.split(" ")
                time = ts[0] + " " + ts[1]
                value = ts[2]
                print(time, value)

thread = threading.Thread(target=work)
thread.daemon = True
thread.start()

while True:
    while len(series) == index:
        time.sleep(1)

    #request_anomaly()
