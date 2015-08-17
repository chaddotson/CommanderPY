from logging import getLogger

from .core import TwitterDM
import tweepy

logger = getLogger(__name__)


class TwitterAPIWrapper(object):
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_key = access_key
        self._access_secret = access_secret
        self._api = self._get_twitter_api()

    def _get_twitter_api(self):
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_key, self._access_secret)
        return tweepy.API(auth)

    def get_direct_messages(self, **kwargs):
        messages = self._api.direct_messages()

        direct_messages = []

        for message in messages:
            dm = TwitterDM(id, message.sender.id, message.sender.screen_name, message.text)

            direct_messages.append(dm)

        return direct_messages

    def update_status(self, message):
        logger.info("About to tweet!")
        self._api.update_status(status=message)
        logger.info("Message tweeted")
