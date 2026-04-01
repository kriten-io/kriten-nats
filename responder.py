import aiohttp
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
import os
import sys

async def request_handler(msg: Msg) -> None:
    nats = NATS()
    # Connect to the NATS server
    await nats.connect(f"nats://{NATS_HOST}:{NATS_PORT}")
    # Process request
    # Expect message format to be task:task_args
    # task is Kriten task name
    # task_args is Kriten task args in key,value pairs (optional)
    request: str = msg.data.decode()
    print(f"Received Kriten job request: {request}")
    task = request.split(":")[0]
    kriten_launch_url = KRITEN_JOBS_URL + task
    if ":" in request:
        task_args = ":".join(request.split(':')[1:])
        payload = json.loads(task_args)
    else:
        payload = {}

    async with aiohttp.ClientSession() as session:
        # if ":" in request:
        async with session.post(kriten_launch_url, json=payload, headers=KRITEN_HEADERS) as response:
            data = await response.json()
            print("Received response from Kriten:", data)
            # Send job id back to requester
            await msg.respond(json.dumps(data).encode("utf-8"))
            error = data.get('error')
            if error:
                print(f"Kriten error: {error}")
                result = error
            else:
                job_id = data.get('id')
                url = KRITEN_JOBS_URL + job_id
                completed = 0
                failed = 0
                # Query Kriten for job result every 4 seconds
                while not completed and not failed:
                    await asyncio.sleep(4)
                    async with session.get(url, headers=KRITEN_HEADERS) as response:
                        result = await response.json()
                        completed = result.get("completed")
                        failed = result.get("failed")
                if completed:
                    print(f"Kriten job id: {job_id} completed.")
                else:
                    print(f"Kriten job id: {job_id} failed.")
        await nats.publish("kriten.job.results", json.dumps(result).encode())


async def run() -> None:
    nats: NATS = NATS()
    await nats.connect(f"nats://{NATS_HOST}:{NATS_PORT}")
    # Subscribe to the requests subject
    subject = "kriten.job.requests"
    await nats.subscribe(subject, cb=request_handler)
    print(f"Subscribed to '{subject}'")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    NATS_HOST = os.getenv("NATS_HOST")
    NATS_PORT = os.getenv("NATS_PORT")
    KRITEN_URL = os.getenv("KRITEN_URL")
    KRITEN_API_TOKEN = os.getenv("KRITEN_API_TOKEN")

    if not NATS_HOST:
        print("Environment variable NATS_HOST not set.")
    if not NATS_PORT:
        print("Environment variable NATS_PORT not set.")
    if not KRITEN_URL:
        print("Environment variable KRITEN_URL not set.")
    if not KRITEN_API_TOKEN:
        print("Environment variable KRITEN_API_TOKEN not set.")
    if not NATS_HOST or not NATS_PORT or not KRITEN_URL or not KRITEN_API_TOKEN:
        sys.exit()

    KRITEN_JOBS_URL = f"{KRITEN_URL}/api/v1/jobs/"
    KRITEN_HEADERS = {
        'Content-Type': 'application/json',
        'Token': KRITEN_API_TOKEN
        }

    asyncio.run(run())