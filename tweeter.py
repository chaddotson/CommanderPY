#!/usr/bin/env python

import commands
import os
import sys
import tweepy
import pika



from json import load, loads, dumps
from logging import basicConfig, getLogger, INFO

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('tweeter.cfg')



logger = getLogger(__name__)
logger.setLevel(INFO)

basicConfig()


CONSUMER_KEY = config.get("TWEETER", "CONSUMER_KEY")
CONSUMER_SECRET = config.get("TWEETER", "CONSUMER_SECRET")
ACCESS_KEY = config.get("TWEETER", "ACCESS_KEY")
ACCESS_SECRET = config.get("TWEETER", "ACCESS_SECRET")


MESSAGE_QUEUE_HOST = config.get("MESSAGE_QUEUE", "HOST")
MESSAGE_QUEUE_USER = config.get("MESSAGE_QUEUE", "USER")
MESSAGE_QUEUE_PASS = config.get("MESSAGE_QUEUE", "PASS")
MESSAGE_QUEUE_NAME = config.get("MESSAGE_QUEUE", "NAME")

logger.info("Connecting to message queue on {0}".format(MESSAGE_QUEUE_HOST))


message_broker_credentials = pika.PlainCredentials(MESSAGE_QUEUE_USER, MESSAGE_QUEUE_PASS)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=MESSAGE_QUEUE_HOST, credentials=message_broker_credentials))

channel = connection.channel()

channel.queue_declare(queue=MESSAGE_QUEUE_NAME)


def tweet(message):
    logger.info("About to tweet!")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(status=message)
    logger.info("Message tweeted")

def on_request(ch, method, props, body):
    logger.info("Processing message")


    results = dict(STATUS="", MESSAGE="")

    try:
        message = loads(body)
        # raise KeyboardInterrupt
        tweet(message["MESSAGE"])
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
channel.basic_consume(on_request, queue=MESSAGE_QUEUE_NAME)
channel.start_consuming()
