import pika


def get_subscriber(host='localhost', port=5672, exchange='default',
                   exchange_type='fanout', queue=None, exclusive=False):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, type=exchange_type)
    result = channel.queue_declare(exclusive=exclusive)
    queue = queue or result.method.queue
    channel.queue_bind(exchange=exchange, queue=queue)

    def start_consuming(func):
        def callback(ch, method, properties, message):
            func(message=message)

        channel.basic_consume(
            callback,
            queue=queue,
            no_ack=True
        )
        channel.start_consuming()

    return start_consuming

start_consuming = get_subscriber()

start_consuming_exclusively = get_subscriber(exclusive=True)

def start_consuming_from_queue(queue):
    get_subscriber(queue=queue)()

def start_consuming_exclusively_from_queue(queue):
    get_subscriber(queue=queue, exclusive=True)()
