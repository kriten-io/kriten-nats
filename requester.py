import argparse
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from pprint import pprint

async def run(task) -> None:
    nats: NATS = NATS()
    await nats.connect("nats://localhost:4222")
    # Send a request and wait for a reply
    try:
        response: Msg = await nats.request("kriten.job.requests", task.encode(), timeout=10)
        job_result: str = response.data.decode()
        print("Kriten job: ", job_result)
    except Exception as e:
        print(str(e))
    await nats.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kriten job via NATS')
    parser.add_argument('-t', '--task', type=str, help='Kriten task name', required=True)
    args = parser.parse_args()
    asyncio.run(run(args.task))
