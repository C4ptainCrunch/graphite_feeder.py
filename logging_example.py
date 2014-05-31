import logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s] [%(levelname)s] %(message)s')

from collector import GraphiteCollector

server = GraphiteCollector("server.tld", prefix="myPrefix", delay=20)

@server.metric()
def myMetric():
    return 1234

if __name__ == '__main__':
    server.feed()
