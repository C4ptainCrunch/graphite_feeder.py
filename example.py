from collector import GraphiteCollector

server = GraphiteCollector("shamir.wu", prefix="my_prefix", delay=20)

@server.metric()
def my_metric():
    return 1234

@server.metric(name="my_better_metric_name")
def my_metric():
    return 10


@server.metric(multiple=True)
def my_multiple_metric():
    return {
        'sub_value' : 12,
        'other_subvalue': 50
    }


if __name__ == '__main__':
    server.feed()
