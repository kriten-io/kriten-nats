import aiohttp
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg

async def request_handler(msg: Msg) -> None:
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
            job_id = data['id']
            url = kriten_url + job_id
        completed = 0
        failed = 0
        while not completed and not failed:
            await asyncio.sleep(4)
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                completed = result.get("completed")
                failed = result.get("failed")
                print("result", result)
    await msg.respond(json.dumps(result).encode("utf-8"))

async def run() -> None:
    nats: NATS = NATS()
    await nats.connect("nats://localhost:4222")
    # Subscribe to handle requests
    await nats.subscribe("kriten.job.sync", cb=request_handler)
    print("Responder listening for Kriten sync job requests...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())