#!/bin/python

"""
This script is responsible for checking twitter for direct messages and putting the source/message on the queue.
"""

from argparse import ArgumentParser
from ConfigParser import RawConfigParser
from json import dumps
from logging import getLogger
from logging.config import dictConfig

from CommanderPy.common.persistance import PersistentDict
from CommanderPy.common.twitter import get_twitter_api, TwitterMentionEncoder, TwitterMention

from CommanderPy.common.rabbit import MessageQueueBlockingPublisher
from CommanderPy.settings import DefaultConfiguration as settings


logger = getLogger(__name__)


def get_args():
    parser = ArgumentParser(description='Get Twitter DMs')
    parser.add_argument('settings_file', help='ConfigParser compatible settings file.')
    parser.add_argument('persistance_file', help='File to save state to.')
    return parser.parse_args()


def get_messages(twitter_api, last_mention_id=None):

    if last_mention_id is None:
        return twitter_api.mentions_timeline()

    else:
        return twitter_api.mentions_timeline(last_mention_id)


def main():
    args = get_args()

    dictConfig(settings.LOGGING)

    config = RawConfigParser()
    config.read(args.settings_file)

    message_queue_host = config.get("MESSAGE_QUEUE", "HOST")
    message_queue_user = config.get("MESSAGE_QUEUE", "USER")
    message_queue_pass = config.get("MESSAGE_QUEUE", "PASS")
    message_queue_name = config.get("MESSAGE_QUEUE", "NAME")

    state = PersistentDict(args.persistance_file)

    api = get_twitter_api(
        config.get("TWITTER", "CONSUMER_KEY"),
        config.get("TWITTER", "CONSUMER_SECRET"),
        config.get("TWITTER", "ACCESS_KEY"),
        config.get("TWITTER", "ACCESS_SECRET"))

    messages = get_messages(api, state.get('last_mention_id', None))

    logger.info("Fetched %d twitter mentions", len(messages) if messages is not None else 0)

    publisher = MessageQueueBlockingPublisher(message_queue_host, message_queue_user, message_queue_pass)

    for message in messages:
        mention = TwitterMention(message.id, message.user.id, message.user.screen_name, message.text)
        publisher.publish(message_queue_name, message=dumps(mention, cls=TwitterMentionEncoder))

    if len(messages) > 0:
        state['last_mention_id'] = messages[-1].id

    state.sync()


if __name__ =="__main__":
    main()
