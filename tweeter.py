#!/usr/bin/env python

import commands
import os
import sys
import tweepy
import pika



from json import load, loads, dumps
from logging import basicConfig, getLogger, INFO

logger = getLogger(__name__)
logger.setLevel(INFO)

basicConfig()


tweeter_settings = dict()

with open("tweeter_settings.json") as f:
    tweeter_settings.update(load(f))

twitter_settings = tweeter_settings.get("TWITTER")

CONSUMER_KEY = twitter_settings.get("CONSUMER_KEY")
CONSUMER_SECRET = twitter_settings.get("CONSUMER_SECRET")
ACCESS_KEY = twitter_settings.get("ACCESS_KEY")
ACCESS_SECRET = twitter_settings.get("ACCESS_SECRET")

queue_settings = tweeter_settings.get("MESSAGE_QUEUE")

MESSAGE_QUEUE_HOST = queue_settings.get("HOST")
MESSAGE_QUEUE_USER = queue_settings.get("USER")
MESSAGE_QUEUE_PASS = queue_settings.get("PASS")
MESSAGE_QUEUE_NAME = queue_settings.get("NAME")

logger.info("Connecting to message queue on {0}".format(MESSAGE_QUEUE_HOST))


message_broker_credentials = pika.PlainCredentials(MESSAGE_QUEUE_USER, MESSAGE_QUEUE_PASS)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=MESSAGE_QUEUE_HOST, credentials=message_broker_credentials))

channel = connection.channel()

channel.queue_declare(queue=MESSAGE_QUEUE_NAME)


def tweet(message):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(message)

def on_request(ch, method, props, body):
    logger.info("Processing message")


    results = dict(STATUS="", MESSAGE="")

    try:
        message = loads(body)
        tweet(message["MESSAGE"])
        results["STATUS"] = "OK"
    except Exception as e:
        results["STATUS"] = "ERROR"
        results["MESSAGE"] = e.message

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=dumps(results))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=MESSAGE_QUEUE_NAME)
channel.start_consuming()
