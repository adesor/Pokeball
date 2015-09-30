# Pokeball
Pokeball is a wrapper around pika (Python client for RabbitMQ). It provides functions that can be used to publish and subscribe messages to and from a fanout exchange.

## Installation
```$ pip install pokeball```

## Example Usage
### Publishing messages
```python
>>> from pokeball import pub
>>> pub.send_message("This is a test message")

```
By default, the messages will be sent to a RabbitMQ server running on localhost on port 5672. If you want to customize this, you can get a publisher function using the ```get_publisher``` function:
```python
>>> publish = pub.get_publisher(host='127.0.0.1', port=5672)
>>> publish("This is another test message")
```

## Consuming messages
```python
>>> from pokeball import sub
>>> def foo(message):
...   print message
  
>>> sub.start_consuming(foo)

```
The function ```foo``` will be called whenever a new message is received by the consumer. The message will be passed on in the ```message``` argument to the function passed to ```start_consuming```.

```start_consuming``` will wait for messages. The default host and port are ```localhost``` and 5672 respectively.

You can get a customized ```start_consuming``` function by using the ```get_subscriber``` function as below:

```python
>>> consume = sub.get_subscriber(host='127.0.0.1', port=5672)
>>> consume(foo)

```
The ```get_subscriber``` function takes in an optional host and a port and returns a consuming function (```consume``` in the above case)


Starting multiple consumers will make each consumer receive a copy of the message, and hence execute the passe function, by default. If you want multiple consumers to consume messages in a round robin fashion, and not have all of them consume the message, you have to specify a queue:
```python
>>> consume = sub.get_subscriber(host='127.0.0.1', port=5672, queue='test_queue')
>>> consume(foo)

```
Alternatively, you can use ```start_consuming_from_queue```:
```python
>>> sub.start_consuming_from_queue(foo, "test_queue")

```

If you want to ensure that no other consumer uses the same queue, you can use the ```exclusive``` parameter of ```get_subscriber```:
```python
>>> consume = sub.get_subscriber(host='127.0.0.1', port=5672, exclusive=True)
>>> consume(foo)

```
Or, you can use the shortcut function ```start_consuming_exclusively```
```python
>>> sub.start_consuming_exclusively(foo)

```

If you also want to specify a queue and have it be exclusive to your consumer, you can specify the ```queue``` and ```exclusive``` parameters of ```get_subscriber```. Or, you can use the shortcut function ```start_consuming_exclusively_from_queue```

```python
>>> sub.start_consuming_exclusively_from_queue(foo, "test_queue")

```

## Routing messages
By default, all messages go to all consumers. If you want to send messages selectively, you have to set a ```routing_key``` for the message.

```python
>>> pub.send_message("This is a test message", routing_key='test_message')

```

On the subscriber side, you have to specify ```binding_keys```. If the ```routing_key``` matches with one of the ```binding_keys```, the message is received by the subscriber.
```binding_keys``` is a list containing the routing keys that the subscriber would accept. For example,

```python
>>> consume = sub.get_subscriber(binding_keys=['test_message'])
>>> consume(foo)

```

The ```binding_keys``` can have wildcards:
- ```#``` (hash): placeholder for zero or more words
- ```*``` (asterisk): placeholder for exactly one word
