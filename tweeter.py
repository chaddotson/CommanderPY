#!/usr/bin/env python

from json import loads
from logging import basicConfig, getLogger, INFO
import ConfigParser

import pika

from CommanderPy.common.twitter.core import tweet

config = ConfigParser.RawConfigParser()
config.read('tweeter.cfg')



logger = getLogger(__name__)
logger.setLevel(INFO)

basicConfig()


CONSUMER_KEY = config.get("TWEETER", "CONSUMER_KEY")
CONSUMER_SECRET = config.get("TWEETER", "CONSUMER_SECRET")
ACCESS_KEY = config.get("TWEETER", "ACCESS_KEY")
ACCESS_SECRET = config.get("TWEETER", "ACCESS_SECRET")


message_queue_host = config.get("MESSAGE_QUEUE", "HOST")
message_queue_user = config.get("MESSAGE_QUEUE", "USER")
message_queue_pass = config.get("MESSAGE_QUEUE", "PASS")
message_queue_name = config.get("MESSAGE_QUEUE", "NAME")

logger.info("Connecting to message queue on {0}".format(message_queue_host))


message_broker_credentials = pika.PlainCredentials(message_queue_user, message_queue_pass)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=message_queue_host, credentials=message_broker_credentials))

channel = connection.channel()

channel.queue_declare(queue=message_queue_name)


def on_request(ch, method, props, body):
    logger.info("Processing message")

    results = dict(STATUS="", MESSAGE="")

    try:
        message = loads(body)
        # raise KeyboardInterrupt
        tweet(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, message["MESSAGE"])
        results["STATUS"] = "OK"
        ch.basic_ack(delivery_tag = method.delivery_tag)


    except Exception as e:
        logger.exception("Failed to tweet!")
        results["STATUS"] = "ERROR"
        results["MESSAGE"] = e.message

    # ch.basic_publish(exchange='',
    #                  routing_key=props.reply_to,
    #                  properties=pika.BasicProperties(correlation_id = \
    #                                                  props.correlation_id),
    #                 body=dumps(results))
    # ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=message_queue_name)
channel.start_consuming()
