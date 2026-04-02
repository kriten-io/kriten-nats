# kriten-nats
Run Kriten jobs via NATS

### requester.py
Put messages on the NATs queue kriten.job.requests
The message contains kriten task name and any optional arguments.

### responder.py
Subscribes to kriten.job.requests and launches the kriten jobs.
Returns job id to the requester.
Posts job result to kriten.job.results

### results.py
Subscribes to kriten.job.results and prints job stdout.

## Install
```
export NATS_HOST=<host where NATS is running>
export NATS_PORT=<NATs port>
export KRITEN_URL=<kriten URL>
export KRITEN_API_TOKEN=<kriten API token>
```
You will need [uv](https://docs.astral.sh/uv/) installed.

## Start results subscriber
This subscribes to 'kriten.job.results' and prints messages.
```
uv run results.py
```
## Start responder
Subscribes to 'kriten.job.requests'. Responds to requester with job id and then periodically queries Kriten for job completion.
Job results are published to 'kriten.job.results'.
```
uv run responder.py
```

## Send a request
Send a request specifying Kriten task name.
```
uv run requester.py -t hello-kriten
```
Send a request with variables.
```
uv run requester.py -t hello-kriten -d name=Steve greeting=Hello
```
