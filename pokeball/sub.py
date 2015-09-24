import pika


def get_subscriber(host='localhost', port=5672, exchange='default',
                   exchange_type='fanout', queue=None, exclusive=False):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, type=exchange_type)

    queue_declare_kwargs = {
        "exclusive": exclusive
    }
    if queue is not None:
        queue_declare_kwargs.update({"queue": queue})
    result = channel.queue_declare(**queue_declare_kwargs)
    channel.queue_bind(exchange=exchange, queue=result.method.queue)

    def start_consuming(func):
        def callback(ch, method, properties, message):
            func(message=message)

        channel.basic_consume(
            callback,
            queue=result.method.queue,
            no_ack=True
        )
        channel.start_consuming()

    return start_consuming

start_consuming = get_subscriber()

start_consuming_exclusively = get_subscriber(exclusive=True)

def start_consuming_from_queue(func, queue):
    get_subscriber(queue=queue)(func)

def start_consuming_exclusively_from_queue(func, queue):
    get_subscriber(queue=queue, exclusive=True)(func)
