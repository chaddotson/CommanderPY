
from unittest import TestCase

from common.twitter import get_twitter_api, TwitterDM, TwitterDMEncoder, TwitterDMDecoder

# def get_twitter_api(consumer_key, consumer_secret, access_key, access_secret):
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_key, access_secret)
#     return tweepy.API(auth)
#

from json import dumps, loads
from unittest import TestCase


class TwitterDMEncoderTests(TestCase):
    def test_can_encode_twitter_dm_as_json(self):
        dm = TwitterDM(1, "Someone", "Test")

        converted = dumps(dm, cls=TwitterDMEncoder)

        retrieved = loads(converted)

        self.assertDictEqual(retrieved, dict(FROM_ID=1, FROM_SCREEN_NAME="Someone", MESSAGE_TEXT="Test"))

class TwitterDMDecoderTests(TestCase):
    def test_can_decode_twitter_dm_as_json(self):

        jsonstring = """{"FROM_ID":1, "FROM_SCREEN_NAME":"Someone", "MESSAGE_TEXT":"Test"}"""
        expected = TwitterDM(1, "Someone", "Test")
        got = loads(jsonstring, cls=TwitterDMDecoder)

        self.assertEqual(got, expected)

        # converted = dumps(dm, cls=TwitterDMEncoder)
        #
        # retrieved = loads(converted)
        #
        # self.assertDictEqual(retrieved, dict(FROM_ID=1, FROM_SCREEN_NAME="Someone", MESSAGE_TEXT="Test"))
        #

#
#
# class TwitterTestFixure(TestCase):
#     def test_can_get_twitter_api(self):
#
#
#     def test_can_create_twitter_dm_object(self):
#         self.assertTrue(False)
#
#     def test_can_encode_twitter_dm_text_message(self):
#         self.assertTrue(False)
#
