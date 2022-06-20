import asyncio
import datetime
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import TimeSeriesPoint, DetectRequest, TimeGranularity, AnomalyDetectorError
from azure.core.credentials import AzureKeyCredential



async def on_event(partition_context, event):
    # Save new event info
    event_info = event.body_as_str(encoding='UTF-8')
    s = str(event_info)
    time = s[s.find(":") + 2: s.find(";")]
    value = int(float(s[s.rfind(":") + 2:]))



    print(f"Received the event: \"{event.body_as_str(encoding='UTF-8')}\" "
          f" Arrived Time : {datetime.datetime.now()} "
          f"from the partition with ID: \"{partition_context.partition_id}\"")

    ema_value = series_update(data, time, value, limit_n=1441)
    response = read_and_request_anomaly()


    dataframe_update(data, time, ema_value, response.is_anomaly)


    if response.is_anomaly is True:
        print(f"Anomaly Detected {response}")

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.

    await partition_context.update_checkpoint(event)

def read_and_request_anomaly():
    # request anomaly
    request = DetectRequest(series=series, granularity=TimeGranularity.PER_SECOND)
    response = request_anomaly(request)
    return response


# async def main():
#     # Create an Azure blob checkpoint store to store the checkpoints.
#     blob_conn_str = keys["blob_conn_str"]
#     blob_container_name = keys["blob_container_name"]
#     #checkpoint_store = BlobCheckpointStore.from_connection_string(blob_conn_str, blob_container_name)
#     # Create a consumer client for the event hub.
#     eventhub_conn_str = keys["eventhub_conn_str"]
#     eventhub_name = keys["eventhub_name"]
#     #client = EventHubConsumerClient.from_connection_string(eventhub_conn_str,
#                                                            # consumer_group="$Default",
#                                                            # eventhub_name=eventhub_name,
#                                                            # checkpoint_store=checkpoint_store)
#     async with client:
#         # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
#         await client.receive(on_event=on_event, starting_position="-1")


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


def anomaly_simulation():
    n = 1800
    std = 15
    mean = 45
    data = [(mean - std) + random.randint(0, std * 2) for i in range(n)]


    # end time must consider period parameter.
    index = pd.date_range(start="2022-06-19T16:45:00Z", end=f"2022-06-19T17:15:00Z", periods=n)
    index = index.strftime("%Y-%m-%dT%H:%M:%SZ")

    df = pd.DataFrame(data={
        'time': index,
        'value': data,
        "ema" : None,
        "is_anomaly": False
    })
    print(df.head())
    df.plot()
    plt.show()

    df.to_csv("test_v1.csv", index=False)


def series_init(df, w):
    series = []
    for index, row in df.iterrows():
        # caution! it's not an exponential
        series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))
    return series


def series_update(df, time, new_value, limit_n=1441):
    print("series_update")
    temp_list = [weight[i] * series[i].value for i in range(-4, 0, 1)] + [new_value]
    temp_avg = sum(temp_list + [new_value]) / 5
    ema_value = int(temp_avg)

    series.append(TimeSeriesPoint(timestamp=time, value=ema_value))

    if len(series) >= limit_n:
        series.pop(0)
    return ema_value

def dataframe_update(df, time, ema_value, is_anomaly):
    df.append({
        "time": time,
        "value": ema_value,
        "is_anomaly": is_anomaly
    })

# Configuration
with open("../key_value.keys") as f:
    keys = json.load(f)

anomaly_detector_key = keys["anomaly_detector_key"]
anomaly_detector_endpoint = keys["anomaly_detector_endpoint"]
weight = [1, 1, 1, 1]  # weight for EMA
# data load
data = pd.read_csv("Anomaly Simulation with tzinfo.csv", parse_dates=['time'], index_col=False)  # past data
series = series_init(data, weight)  # list to send Azure Anomaly Detector

if __name__ == '__main__':
    print("receiver")
    # make event loop
    #loop = asyncio.get_event_loop()
    # Run the main method.
    #loop.run_until_complete(main())
    anomaly_simulation()
    # data_file['time'] = pd.to_datetime(data_file['time']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
