import pika


def get_publisher(host='localhost', port=5672, exchange='default'):
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port)
        )
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, type='topic')

    def send_message(message, routing_key='#'):
        channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message
            )

    return send_message

send_message = get_publisher()
