import asyncio
import datetime
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import TimeSeriesPoint, DetectRequest, TimeGranularity, AnomalyDetectorError
from azure.core.credentials import AzureKeyCredential

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

anomaly_detector_key = "b4751ab416f84b1da1e53a5296d5dd8f"
anomaly_detector_endpoint = "https://anomalydetector2022.cognitiveservices.azure.com/"

async def on_event(partition_context, event):
    # Print the event data.
    print(f"Received the event: \"{event.body_as_str(encoding='UTF-8')}\" "
          f" Arrived Time : {datetime.datetime.now()} "
          f"from the partition with ID: \"{ partition_context.partition_id}\"")

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)


async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    blob_conn_str = "DefaultEndpointsProtocol=https;AccountName=cdstorageaccount2022;AccountKey=E2M/nwaW/MLOkqHCuLhUp2+p12uYiK8QhDP9vDGmfwwWDn4jwfuz0tKbkuOUQpWvaIVZz6hYUVVuxhrXrVKf5Q==;EndpointSuffix=core.windows.net"
    blob_container_name = "blobeventhubstream"
    checkpoint_store = BlobCheckpointStore.from_connection_string(blob_conn_str, blob_container_name)

    # Create a consumer client for the event hub.
    conn_str = "Endpoint=sb://cdeventhub.servicebus.windows.net/;SharedAccessKeyName=connection_string;SharedAccessKey=Qbc6XkNXktYkQ7oiloLSef6ePOI74TA7U67BkwU4NQ4=;EntityPath=eventhub_stream"
    eventhub_str = "eventhub_stream"
    client = EventHubConsumerClient.from_connection_string(conn_str,
                                                           consumer_group="$Default",
                                                           eventhub_name=eventhub_str,
                                                           checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event, starting_position="-1")


def request_anomaly(request):
    print('Detecting the anomaly status of the latest data point.')

    try:
        response = client.detect_last_point(request)
    except AnomalyDetectorError as e:
        print('Error code: {}'.format(e.error.code), 'Error message: {}'.format(e.error.message))
    except Exception as e:
        print(e)
    print(response)
    if response.is_anomaly:
        print('The latest point is detected as anomaly.')
    else:
        print('The latest point is not detected as anomaly.')
    return response


def anomaly_simulation():
    n = 3600 * 3
    std = 50
    mean = 100

    data = [(mean - std) + random.randint(0, std * 2) for i in range(n)]
    data[4000] = 200
    data[4500] = 40
    data[6000] = 200
    data[5500] = 35
    data[7000] = 195
    data[6500] = 38
    data[9000] = 210
    data[7500] = 35

    # end time must consider period parameter.
    index = pd.date_range(start="2022-04-23 15:00:00 UTC +0900", end=f"2022-04-23 1{8}:00:00 UTC +0900", periods=n)
    index = index.strftime("%Y-%m-%d %H:%M:%S %Z %z")
    print(index)

    df = pd.DataFrame(data={
    "data": data
    },
    index=index)
    print(df.head())
    df.plot()
    plt.show()

    df.to_csv("Anomaly Simulation with tzinfo.csv")


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # Run the main method.
    # loop.run_until_complete(main())

    #This sentence is for commit
    client = AnomalyDetectorClient(AzureKeyCredential(anomaly_detector_key), anomaly_detector_endpoint)
    print(client)
    series = []
    results = []
    data_file = pd.read_csv("Anomaly Simulation with tzinfo.csv", parse_dates=[0])
    for index, row in data_file.iterrows():
        series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))
        if index > 1441:
            print("Call Method")
            print(f"Real Value : {row[1]}")
            request = DetectRequest(series=series, granularity=TimeGranularity.PER_SECOND)
            response = request_anomaly(request)
            series.pop(0)
            results.append({
                "date":row[0],
                "value":row[1],
                "is_anomaly" : response.is_anomaly
            })
        if index > 1500:
            print(results)
            break








