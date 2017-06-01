dogDriver
=========

**Is service <X> getting slower or faster with this new release?**

To answer to this question, you will need to spend some time
digging into the metrics for different time windows and find when
each release was made.

Or you can let dogDriver collect performance metrics over time, and
find out immediatly how it's trending.

.. image:: https://github.com/tarekziade/dogdriver/blob/master/dd.png?raw=true


Limitations
~~~~~~~~~~~

dogDriver is still in experimental phase.

What we've learned so far:

- For consistent results, tests need to be run from the same
  location all the time
- The tests need to be run often in order to remove any
  unwanted discrepancy
- The trend will be impacted by any architectural change on
  the deployment, whether they are automatic (autoscaling)
  or manual (ops adding or removing a node.)
- The load needs to be tweaked so the infrastructure gets a
  fair load but don't get overwhelmed.

Overall, dogDriver should still provide a good indicator of
whether a release has altered the performances of a service.
But it should only be a trigger to a deeper investigation.


Architecture
------------

dogDriver is composed of three parts:

- a client that performs a smoke test using Molotov
- a worker that aggregates metrics from Datadog for each run
- a server that displays them in a simple dashboard


Client
~~~~~~

When the client runs it does the following:

- query the ServiceBook to get the URL of the molotov test.
- sends a start event to datadog
- runs a calibrated smoke+load test using molotov on a stack
- sends a stop event to datadog
- sends the start and stop values to the Dogdriver Server

Worker
~~~~~~

The worker builds metrics by doing the following:

- collect runs sent by the client
- when a run is older than 10 minutes, queries Datadog to build metrics
- store metrics for the Server

Server
~~~~~~

The server does the following:

- exposes an API to receive tests runs. Each run is stored in a queue for the
  worker.
- a metrics displaying the performance trend for a specific project is
  updated.
- a simple JS dashboard display those all those metrics.


Integration
-----------

The Dogdriver client can run from anywhere, as long as it has
access to the tested service and to the S3 bucket where results
are stored.

The client uses the ServiceBook to find out if a project has
a **dogdriver** test in its tests list. The test should be
an URL pointing to a Github repo that contains a Molotov test
along with a Molotov configuration as explained in http://molotov.readthedocs.io/en/latest/slave/

dogDriver will pick up the **dogdriver** configuration and run
Molotov using this command::

    $ moloslave <github url> dogdriver


