import asyncio
import random
import time
import json
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import datetime


with open("../key_value.keys") as f:
    keys = json.load(f)


async def run(data):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    eventhub_conn_str = keys["eventhub_conn_str"]
    eventhub_name = keys["eventhub_name"]
    producer = EventHubProducerClient.from_connection_string(conn_str=eventhub_conn_str,
                                                             eventhub_name=eventhub_name)

    task = asyncio.create_task(data_generator(data))

    index = 0
    batch_count = 0
    while True:
        print("run is working")
        if index == len(data):
            await asyncio.sleep(1)
        async with producer:
            # Create a batch.
            event_data_batch = await producer.create_batch()
            # Add events to the batch.
            temp_data = data[index:]
            index = len(data)
            for row in temp_data:
                event_data_batch.add(EventData(row))
            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)
            batch_count += 1
            if index >= 10:
                break
    print("End main")
    print(f"Batch Count : {batch_count}")


async def data_generator(data):
    count = 0
    end = 10
    while True:
        print("data_generator is working")
        r = random.randint(0, 100)
        data.append(f"Event Time : {datetime.datetime.now()}; Random Number : {r}")
        count += 1
        await asyncio.sleep(1)
        if count >= end:
            break


if __name__ == '__main__':

    print("producer")
    data = []

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(data))
    #loop.run_until_complete(run(data))    # if the argument is a coroutine object it is implicity scheduled to run as a asyncio.Task. Return the Future's result or ots exception

    print("End Program")





