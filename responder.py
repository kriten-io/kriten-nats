import aiohttp
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg

async def request_handler(msg: Msg) -> None:
    nats = NATS()
    # Connect to the NATS server
    await nats.connect("nats://localhost:4222")
    # Process request
    request: str = msg.data.decode()
    print(f"Received Kriten job request: {request}")
    kriten_url = "http://kriten-dev.192.168.10.190.nip.io/api/v1/jobs/"
    kriten_launch_url = kriten_url + request
    headers = {
        'Content-Type': 'application/json',
        'Token': 'kri_Rnx8Pvr2jBalEjvfwA4nIHUhI8lIUGHIK5zH'
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(kriten_launch_url, headers=headers) as response:
            data = await response.json()
            print("Received response from Kriten:", data)
            # Send job id back to requester
            await msg.respond(json.dumps(data).encode("utf-8"))
            job_id = data.get('id')
            url = kriten_url + job_id
            completed = 0
            failed = 0
            # Query Kriten for job result every 4 seconds
            while not completed and not failed:
                await asyncio.sleep(4)
                async with session.get(url, headers=headers) as response:
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
    await nats.connect("nats://localhost:4222")
    # Subscribe to the requests subject
    subject = "kriten.job.requests"
    await nats.subscribe(subject, cb=request_handler)
    print(f"Subscribed to '{subject}'")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())