import pika


def get_publisher(host='localhost', port=5672, exchange='default', exchange_type='fanout'):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, type=exchange_type)

    def send_message(message):
        channel.basic_publish(
            exchange=exchange,
            routing_key='',
            body=message
        )

    return send_message

send_message = get_publisher()
