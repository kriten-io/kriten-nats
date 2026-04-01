import argparse
import os

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
import sys

async def run(task, data) -> None:
    nats: NATS = NATS()
    await nats.connect(f"nats://{NATS_HOST}:{NATS_PORT}")
    # Send a request and wait for a reply
    try:
        if data:
            payload = json.dumps(data)
            message = f"{task}:{payload}"
            response: Msg = await nats.request("kriten.job.requests", message.encode(), timeout=10)
        else:
            response: Msg = await nats.request("kriten.job.requests", task.encode(), timeout=10)
        job_result: str = response.data.decode()
        print("Kriten job: ", job_result)
    except Exception as e:
        print(str(e))
    await nats.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kriten job via NATS')
    parser.add_argument('-t', '--task', type=str, help='Kriten task name', required=True)
    parser.add_argument('-d', '--data', nargs='*', action=ParseKwargs, help='Kriten task args')
    args = parser.parse_args()

    NATS_HOST = os.getenv("NATS_HOST")
    NATS_PORT = os.getenv("NATS_PORT")

    if not NATS_HOST:
        print("Environment variable NATS_HOST not set.")
    if not NATS_PORT:
        print("Environment variable NATS_PORT not set.")

    if not NATS_HOST or not NATS_PORT:
        sys.exit()

    asyncio.run(run(args.task, args.data))
