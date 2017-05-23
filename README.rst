Dogdriver
=========

This project aims at collecting performance metrics to build a
dashboard displaying a trend. The goal is to answer this simple
question : is this service getting slower or faster over time.

The Dogdriver is composed of two parts:

- a client that performs a smoe test using Molotov
- a server that collects metrics from datadog and displays them

Client
------

When the client runs it does the following:

- query the ServiceBook to get the URL of the molotov test.
- sends a start event to datadog
- runs a calibrated smoke+load test using molotov on a stack
- sends a stop event to datadog
- sends the start and stop values to the Dogdriver Server


Server
------

The server does the following:

- exposes an API to receive tests runs. Each run is stored in a queue
- when a run is older than 10 minutes, the server queries Datadog to build metrics
- Metrics are stored as JSON files on the server, grouped by project names
- a metrics displaying the performance trend for a specific project is updated
- a simple JS dashboard display those all those metrics

Integration
-----------

The Dogdriver client is added to a Jenkins pipeline, so it can be
run continuously to build a high-level performance trend per application.


