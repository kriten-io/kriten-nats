import argparse
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg
from pprint import pprint

async def run_sync(task) -> None:
    nats: NATS = NATS()
    await nats.connect("nats://localhost:4222")
    # Send a request and wait for a reply
    try:
        response: Msg = await nats.request("kriten.job.sync", task.encode(), timeout=10)
        job_result: str = response.data.decode()
        job_result_object: dict = json.loads(job_result)
        print(f"Received job result:")
        pprint(job_result_object)
        print("Kriten job: ", job_result)
    except Exception as e:
        print(str(e))
    await nats.close()

async def run_async(task) -> None:
    nats = NATS()
    # Connect to the NATS server
    await nats.connect("nats://localhost:4222")
    # Publishing a message
    subject = "kriten.job.async"
    message = task
    await nats.publish(subject, message.encode())
    print(f"Published message: {message} to {subject}")
    # Close the connection to the server
    await nats.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Kriten job via NATS')
    parser.add_argument('-m', '--mode', choices=['async', 'sync'], help='Asynchronous or synchronous', default='async')
    parser.add_argument('-t', '--task', type=str, help='Kritn task name', required=True)
    args = parser.parse_args()
    if args.mode == 'sync':
        asyncio.run(run_sync(args.task))
    elif args.mode == 'async':
        asyncio.run(run_async(args.task))
