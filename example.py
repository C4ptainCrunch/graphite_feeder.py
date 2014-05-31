# -*- coding: utf-8 -*-
from graphite_feeder import GraphiteFeeder

server = GraphiteFeeder("server.tld", prefix="test2", delay=20)

@server.metric()
def myMetric():
    return 1234

@server.metric(name="betterMetric")
def myOtherMetric():
    return 10


@server.metric(multiple=True)
def myMultipleMetric():
    return {
        'subvalue' : 12,
        'subvalue2': 50
    }


if __name__ == '__main__':
    server.feed()
