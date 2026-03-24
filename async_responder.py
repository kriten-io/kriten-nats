import aiohttp
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg

async def message_handler(msg: Msg) -> None:
    nats = NATS()
    # Connect to the NATS server
    await nats.connect("nats://localhost:4222")

    request: str = msg.data.decode()
    print(f"Received request: {request}")
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
            print("job_id:", job_id, "url", url)
        # await msg.respond(json.dumps(data).encode("utf-8"))
        completed = 0
        while not completed:
            await asyncio.sleep(4)
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                completed = result.get("completed")
                print("completed:", completed)
                print("result", result)
    # await msg.respond(json.dumps(result).encode("utf-8"))
    await nats.publish("kriten.job.results", json.dumps(result).encode())

async def run():
    nats = NATS()

    # Connect to the NATS server
    await nats.connect("nats://localhost:4222")

    # Subscribe to the subject
    subject = "kriten.job.async"
    await nats.subscribe(subject, cb=message_handler)

    print(f"Subscribed to '{subject}'")

    # Keep the connection open to listen for messages
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
