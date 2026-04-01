# kriten-nats
Run Kriten jobs via NATS

## Install

export NATS_HOST="nats.192.168.10.190.nip.io"
export NATS_PORT="30222"
export KRITEN_URL="http://kriten-dev.192.168.10.190.nip.io"
export KRITEN_API_TOKEN="kri_Rnx8Pvr2jBalEjvfwA4nIHUhI8lIUGHIK5zH"

## Start results subscriber
This subscribes to 'kriten.job.results' and prints messages.
```
python results.py
```
## Start responder
Subscribes to 'kriten.job.requests'. Responds to requester with job id and then periodically queries Kriten for job completion.
Job results are published to 'kriten.job.results'.
```
python responder.py
```

## Send a request
Send a request specifying Kriten task name.
```
python requester.py -t hello-kriten
```
Send a request with variables.
```
python requester.py -t hello-kriten -d name=Steve greeting=Hello
```