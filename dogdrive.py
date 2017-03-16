# Configure the module according to your needs
import time
import json
from datadog import initialize


with open('options.json') as f:
    options = json.loads(f.read())


initialize(**options)

# Use Datadog REST API client
from datadog import api

title = "Molotov"
text = "We're doing a Molotov test on kintowe"
_tags = ['version:1', 'app:kintowe']


def start(test_name):
    tags = list(_tags)
    tags.append('step:start')
    tags.append('test:%s' % test_name)
    return api.Event.create(title=title, text=text, tags=tags)


def stop(test_name):
    tags = list(_tags)
    tags.append('step:stop')
    tags.append('test:%s' % test_name)
    return api.Event.create(title='Molotov-Stop', text=text, tags=tags)


# the test
start_event = start("My test")
try:
    # run the molotov test against the stack
    time.sleep(10)
finally:
    stop_event = stop("My Test")

start = start_event['event']['date_happened']
end = stop_event['event']['date_happened']


_200 = 'aws.elb.httpcode_backend_2xx{app:kintowe,env:stage}.as_count()'



# now we want to grab metrics on that time window
print(api.Metric.query(start=start, end=end, query=_200))


