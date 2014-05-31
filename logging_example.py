# -*- coding: utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s] [%(levelname)s] %(message)s')

from graphite_feeder import GraphiteFeeder

server = GraphiteFeeder("server.tld", prefix="myPrefix", delay=20)

@server.metric()
def myMetric():
    return 1234

if __name__ == '__main__':
    server.feed()
