

from unittest import TestCase


class TwitterTests(TestCase):
    def test_can_handle_connection_error(self):

        # force pika.exceptions.AMQPConnectionError

        self.assertTrue(False)
