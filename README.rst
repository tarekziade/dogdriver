Dogdriver
=========


The Dogdriver does the following:

- sends a start event to datadog
- runs a calibrated smoke+load test using molotov on a stack
- sends a stop event to datadog
- queries metrics from datadog between the two events, like elb http counts
- sends that data to a specialized DB

The Dogdriver can be run continuously to build a high-level
performance trend per application.

Trends will be simple % with arrows (up/down/same)



