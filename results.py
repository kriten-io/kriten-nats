import asyncio
import json
from nats.aio.client import Client as NATS

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    # print(f"Received a message on '{subject}': {data}")
    data_object = json.loads(data)
    print(f"Job id: {data_object.get('id')}")
    print(f"stdout: {data_object.get('stdout')}")

async def run():
    nats = NATS()

    # Connect to the NATS server
    await nats.connect("nats://localhost:4222")
    # Subscribe to the results subject
    subject = "kriten.job.results"
    await nats.subscribe(subject, cb=message_handler)
    print(f"Subscribed to '{subject}'")
    # Keep the connection open to listen for messages
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
