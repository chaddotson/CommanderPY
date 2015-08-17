from json import JSONDecoder, JSONEncoder, loads
from json.decoder import WHITESPACE

import tweepy
from tweeter import logger, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET


def get_twitter_api(consumer_key, consumer_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)


class TwitterDM(object):
    def __init__(self, from_id, from_screen_name, message_text):
        self.from_id = from_id
        self.from_screen_name = from_screen_name
        self.message_text = message_text

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class TwitterDMEncoder(JSONEncoder):

    def encode(self, obj):

        if isinstance(obj, TwitterDM):
            obj_as_dict = dict(FROM_ID=obj.from_id,
                               FROM_SCREEN_NAME=str(obj.from_screen_name),
                               MESSAGE_TEXT=str(obj.message_text))

            return JSONEncoder.encode(self, obj_as_dict)

        return JSONEncoder.encode(self, obj)


class TwitterDMDecoder(JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        obj_as_dict = JSONDecoder.decode(self, s, _w)
        return TwitterDM(obj_as_dict.get("FROM_ID", None),
                         obj_as_dict.get("FROM_SCREEN_NAME", None),
                         obj_as_dict.get("MESSAGE_TEXT", None))


def tweet(message):
    logger.info("About to tweet!")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(status=message)
    logger.info("Message tweeted")