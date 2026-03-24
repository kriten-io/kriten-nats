# kriten-nats
Run Kriten jobs via NATS

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
