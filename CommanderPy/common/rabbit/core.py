from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from logging import getLogger

logger = getLogger(__name__)


# class MessageQueueConnectionError(pika.exceptions.AMQPConnectionError):
#     pass

class MessageQueueBlockingPublisher(object):
    def __init__(self, host, user, password):

        logger.info("Connecting to RabbitMQ - Host: %s.", host)

        message_broker_credentials = PlainCredentials(user, password)

        self.connection = BlockingConnection(ConnectionParameters(
            host=host, credentials=message_broker_credentials))

        self.channel = self.connection.channel()

        logger.info("Connected to RabbitMQ.")

    def publish(self, queue_name, message, exchange=''):

        logger.info("Publishing message.")

        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=queue_name,
                                   body=message)
