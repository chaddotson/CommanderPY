from json import dumps, loads
from unittest import expectedFailure, TestCase

from CommanderPy.common.twitter import TwitterDM, TwitterDMEncoder, TwitterDMDecoder


class TwitterAPIWrapperTests(TestCase):
    @expectedFailure
    def test_does_get_twitter_api(self):
        self.assertTrue(False)

    # TODO: What failures from getting the twitter api?

    @expectedFailure
    def test_does_get_twitter_direct_messages(self):
        self.assertTrue(False)

    # TODO: What failures from getting direct messages?

    @expectedFailure
    def test_does_get_twitter_mentions(self):
        self.assertTrue(False)

    # TODO: What failures from getting mentions?


class TwitterDMEncoderTests(TestCase):
    def test_can_encode_twitter_dm_as_json(self):
        dm = TwitterDM(42, 1, "Someone", "Test")

        converted = dumps(dm, cls=TwitterDMEncoder)

        retrieved = loads(converted)

        self.assertDictEqual(retrieved, dict(ID=42, FROM_ID=1, FROM_SCREEN_NAME="Someone", MESSAGE_TEXT="Test"))


class TwitterDMDecoderTests(TestCase):
    def test_can_decode_twitter_dm_as_json(self):

        jsonstring = """{"ID": 42, "FROM_ID":1, "FROM_SCREEN_NAME":"Someone", "MESSAGE_TEXT":"Test"}"""
        expected = TwitterDM(42, 1, "Someone", "Test")
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
