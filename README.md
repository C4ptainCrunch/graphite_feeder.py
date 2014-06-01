# Graphite Feeder
Graphite feeder is a Python (2.7+ and 3.3+) library to feed metrics into Graphite.

It's only purpose is to allow the user to define some functions that will be periodicaly evaluated and their result will be sent to a graphite server.


# Usage

## Installation
`pip install git+https://github.com/C4ptainCrunch/graphite_feeder.py.git`

## Example

This example grabs a metric named `myMetric` every 20 seconds and pushes the result to `server.tld`. That's all.
```python
from graphite_feeder import GraphiteFeeder

server = GraphiteFeeder("server.tld", prefix="myMachine", delay=20)

@server.metric()
def myMetric():
    return 1234

if __name__ == '__main__':
    server.feed()
```

## Metric names

All metric names (including prefixes) will be translated before beeing feeded to graphite.

* All `_` are replaced by `.`

If you want an `_` in your metric name please double it : `__`

Example :
* `my_awesome_metric` -> `my.awesome.metric`
* `no__dot__metric` -> `no_dot_metric`
* `mix__it_metric` -> `mix_it.metric`

## Configuration
All the configuration is done at the creation of `GraphiteFeeder`

```python
GraphiteFeeder(self, server, port=2003, prefix=platform.node(), delay=10, timeout=2)
```
* `server` : your graphite server
* `port` : your graphite server port
* `prefix` will add a prefix to all of your metrics

```python
server = GraphiteFeeder(..., prefix="myPrefix", ...)
@server.metric()
def myName():
    return 1
```

Will send a metric named `myPrefix.myName`

* `delay` in seconds : time between sending metrics to graphite (10 sends metrics 6 times per minute)
* `timeout` in seconds : timeout before giving up while trying to connect to graphite

## Advanced

The `.metric()` decorator accepts some optional arguments :
`name` overrites the metric name (defaults to the function name)

Example:
```python
@server.metric(name="myBetterName")
def myIgnoredName():
    return 1
```
Will send a metric named `myBetterName` instead of `myIgnoredName`

`multiple` : if set to `True` your function has to return a dict of values (instead of a value). Each key of the dict will be a "sub-metric"

Example:
```python
@server.metric(multiple=True)
def myMetric():
    return {
        'submetric' : 10,
        'othersubmetric': 20
    }
```

Will send 2 metrics: `myMetric.submetric` and `othersubmetric`

### Logging

Graphite feeder uses the stdlib python logger. Look at `logging_example.py` to have an example.

# License

> The MIT License (MIT)
> Copyright (c) 2014 Nikita Marchant <nikita.marchant@gmail.com>

# Contributing

I'm open to contributions. Plase open a bug or a pull request :)
