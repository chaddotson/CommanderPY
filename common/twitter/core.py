from json import JSONEncoder
import tweepy


def get_twitter_api(consumer_key, consumer_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)


class TwitterDM(object):
    def __init__(self, from_id, from_scren_name, message_text):
        self.from_id = from_id
        self.from_screen_name = from_scren_name
        self.message_text = message_text


class TwitterDMEncoder(JSONEncoder):

    def encode(self, obj):

        if isinstance(obj, TwitterDM):
            obj_as_dict = dict(From_id=obj.from_id,
                               from_screen_name=str(obj.from_screen_name),
                               message_text=str(obj.message_text))

            return JSONEncoder.encode(self, obj_as_dict)

        return JSONEncoder.encode(self, obj)
