import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore




async def on_event(partition_context, event):
    # Print the event data.
    #print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))
    latest_temp = float(event.body_as_str(encoding='UTF-8')[15:19])
    print(latest_temp)
    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    Checkpoint_store = BlobCheckpointStore.from_connection_string("DefaultEndpointsProtocol=https;AccountName=pycomstorage;AccountKey=uZRtTT/f4Wvxoy50FJIs+AzRA3ut7arVXCIP8MLo25jJnWlAx3h7QfD0EVvgNwpcqcAqz8mHr0iJMQ3wjCm0Bw==;EndpointSuffix=core.windows.net", "temperatureblobstorage")

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string("Endpoint=sb://realtimetemp.servicebus.windows.net/;SharedAccessKeyName=RealTimeTemp_TempOutput_policy;SharedAccessKey=1KMNBdrnuWM0LGAz4ruFiV/OdZ9s4VZdcIIJWQmnqcM=;EntityPath=realtimetempoutput", consumer_group="$Default", eventhub_name="realtimetempoutput")
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="-1")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())
