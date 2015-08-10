"""
This script is responsible for checking twitter for direct messages and putting the source/message on the queue.
"""

from argparse import ArgumentParser
from ConfigParser import RawConfigParser
from json import dumps
from logging import getLogger
from logging.config import dictConfig
from werkzeug.utils import import_string

from common.persistance import PersistentDict
from common.twitter import get_twitter_api, TwitterDM, TwitterDMEncoder
from common.rabbit import BasicBlockingPublisher


logger = getLogger(__name__)


def get_args():
    parser = ArgumentParser(description='Get Twitter DMs')
    parser.add_argument('settings_file', help='ConfigParser compatible settings file.')
    parser.add_argument('persistance_file', help='File to save state to.')
    return parser.parse_args()


def get_messages(twitter_api, last_dm_id=None):
    if last_dm_id is None:
        return twitter_api.direct_messages()

    else:
        return twitter_api.direct_messages(last_dm_id)


if __name__ =="__main__":

    settings = import_string('settings.DefaultConfiguration')
    settings = dictConfig(settings.LOGGING)

    args = get_args()

    config = RawConfigParser()
    config.read(args.settings_file)

    MESSAGE_QUEUE_HOST = config.get("MESSAGE_QUEUE", "HOST")
    MESSAGE_QUEUE_USER = config.get("MESSAGE_QUEUE", "USER")
    MESSAGE_QUEUE_PASS = config.get("MESSAGE_QUEUE", "PASS")
    MESSAGE_QUEUE_NAME = config.get("MESSAGE_QUEUE", "NAME")

    state = PersistentDict(args.persistance_file)

    api = get_twitter_api(
        config.get("TWEETER", "CONSUMER_KEY"),
        config.get("TWEETER", "CONSUMER_SECRET"),
        config.get("TWEETER", "ACCESS_KEY"),
        config.get("TWEETER", "ACCESS_SECRET"))

    messages = get_messages(api, state.get('last_dm_id', None))

    logger.info("Fetched %d twitter direct messages", len(messages) if messages is not None else 0)

    publisher = BasicBlockingPublisher(MESSAGE_QUEUE_HOST, MESSAGE_QUEUE_USER, MESSAGE_QUEUE_PASS)

    for message in messages:
        dm = TwitterDM(message.sender.id, message.sender.screen_name, message.text)
        publisher.publish(MESSAGE_QUEUE_NAME, message=dumps(dm, cls=TwitterDMEncoder))

    if len(messages) > 0:
        state['last_dm_id'] = messages[-1].id

    state.sync()
