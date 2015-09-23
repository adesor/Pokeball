import pika


def get_message_sender(host='localhost', exchange='default', exchange_type='fanout'):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host)
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