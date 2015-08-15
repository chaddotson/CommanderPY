from unittest import TestCase

from mock import patch
from pika.exceptions import AMQPConnectionError

from CommanderPy.common.rabbit import MessageQueueBlockingPublisher


class RabbitTests(TestCase):
    @patch("CommanderPy.common.rabbit.core.BlockingConnection")
    def test_can_handle_connection_error(self,  queue_mock):

        queue_mock.side_effect = AMQPConnectionError
        # force pika.exceptions.AMQPConnectionError

        with self.assertRaises(AMQPConnectionError):
            mq = MessageQueueBlockingPublisher("something", "user", "pass")




