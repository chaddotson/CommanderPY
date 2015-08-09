import pika

from logging import getLogger

logger = getLogger(__name__)


class BasicBlockingPublisher(object):
    def __init__(self, host, user, password):

        logger.info("Connecting to RabbitMQ - Host: %s.", host)

        message_broker_credentials = pika.PlainCredentials(user, password)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host, credentials=message_broker_credentials))

        self.channel = self.connection.channel()

        logger.info("Connected to RabbitMQ.")

    def publish(self, queue_name, message, exchange=''):

        logger.info("Publishing message.")

        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=queue_name,
                                   body=message)
