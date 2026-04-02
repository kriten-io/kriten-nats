import asyncio
import json
from nats.aio.client import Client as NATS
import os
import sys

async def message_handler(msg):
    data = msg.data.decode()
    data_object = json.loads(data)
    print(f"Job id: {data_object.get('id')}")
    print(f"stdout: {data_object.get('stdout')}")

async def run():
    nats = NATS()
    # Connect to the NATS server
    await nats.connect(f"nats://{NATS_HOST}:{NATS_PORT}")
    # Subscribe to the results subject
    subject = "kriten.job.results"
    await nats.subscribe(subject, cb=message_handler)
    print(f"Subscribed to '{subject}'")
    # Keep the connection open to listen for messages
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    NATS_HOST = os.getenv("NATS_HOST")
    NATS_PORT = os.getenv("NATS_PORT")

    if not NATS_HOST:
        print("Environment variable NATS_HOST not set.")
    if not NATS_PORT:
        print("Environment variable NATS_PORT not set.")

    if not NATS_HOST or not NATS_PORT:
        sys.exit()
    asyncio.run(run())
