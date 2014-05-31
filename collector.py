# -*- coding: utf-8 -*-
import platform
import time
import socket
import logging
import sys

log = logging.getLogger(__name__)
PY3 = sys.version_info.major == 3

class Carbon(object):

    def __init__(self, host, port=2003, timeout=2):
        self.host = host
        self.port = port
        self.timeout = timeout

        self.socket = None

    def __enter__(self):
        self.socket = socket.socket()
        self.socket.settimeout(self.timeout)

        self.socket.connect((self.host, self.port))
        log.debug("Graphite connection opened")

        return CarbonConnection(self.socket)

    def __exit__(self, *args):
        self.socket.close()
        log.debug("Graphite connection closed")

class CarbonConnection(object):

    def __init__(self, socket):
        self.socket = socket

    def send(self, name, data):
        timestamp = int(time.time())
        message = "{} {} {}\n".format(name, data, timestamp)
        log.debug("Sending message:'{}'".format(message.strip()))
        if PY3:
            message = message.encode('utf-8')
        self.socket.sendall(message)

class GraphiteCollector(object):

    def __init__(self, server, port=2003, prefix=platform.node(), delay=10, timeout=2):
        self.server = server
        self.port = port
        self.prefix = prefix
        self.delay = delay
        self.timeout = timeout

        self.metrics = {}
        self.multiple = []

    def metric(self, name=None, multiple=False):
        if name == "":
            raise ValueError("The metric name can not be empty")
        elif callable(name):
            raise ValueError("The @metric decorator must be called with (). Eg:\n@server.metric()\ndef my_metric()")

        metric_name = name
        mul = multiple

        def metric_decorator(fn):
            name = metric_name
            multiple = mul
            # todo : multiples
            if name is None:
                name = fn.__name__
            elif name == "":
                raise ValueError("The metric name can not be empty")
            if self.prefix != "":
                name = self.prefix + "." + name
            name = name.replace("_", ".").replace("..", "_")

            log.debug("Registering new metric : {} (function {})".format(name, fn.__name__))
            self.metrics[name] = fn

            if multiple:
                self.multiple.append(name)

            return fn

        return metric_decorator


    def _mesure(self):
        try:
            with Carbon(self.server, self.port, self.timeout) as carbon:
                for name, metric in self.metrics.items():
                    log.debug("Mesuring {}".format(name))
                    data = metric()
                    if not name in self.multiple:
                        carbon.send(name, data)
                    else:
                        for sub_name, sub_data in data.items():
                            sub_name = sub_name.replace("_", ".").replace("..", "_")
                            sub_name = name + "." + sub_name
                            carbon.send(sub_name, sub_data)
        except socket.timeout:
            pass

    def feed(self):
        log.info("Start the feeding loop")
        while True:
            log.debug("Start metric acquisition")
            start = time.time()
            self._mesure()
            stop = time.time()
            sleep_time = max(self.delay - (stop - start), 0)

            if sleep_time == 0:
                log.warning("Metric acquisition and upload ({}s) was longer than the delay ({}s)".format(stop - start, self.delay))
                log.warning("Graphite will behave strangely")

            log.debug("Loop sleeping {}s".format(sleep_time))
            time.sleep(sleep_time)
