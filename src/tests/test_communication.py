#!/usr/bin/env python3

import unittest.mock
import paho.mqtt.client as mqtt
import uuid

from MessageModelManager import OutgoingMessages
from communication import Communication

"""
IMPORTANT: THOSE TESTS ARE NOT REQUIRED FOR THE EXAM AND USED ONLY FOR DEVELOPMENT
ASK YOUR TUTOR FOR SPECIFIC DETAILS ABOUT THIS!
"""


class TestRoboLabCommunication(unittest.TestCase):
    @unittest.mock.patch('logging.Logger')
    def setUp(self, mock_logger):
        """
        Instantiates the communication class
        """
        client_id = '202-' + str(uuid.uuid4())  # Replace YOURGROUPID with your group ID
        client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                             clean_session=False,  # We want to be remembered
                             protocol=mqtt.MQTTv311  # Define MQTT protocol version
                             )

        # Initialize your data structure here
        self.communication = Communication(client, mock_logger)

    def test_message_ready(self):
        outgoing = OutgoingMessages()
        dicti = outgoing.ready()
        keys = list(dicti.keys())
        print(keys)
        print(keys[0])
        self.assertEqual(keys[0], "from")
        print(keys[1])
        self.assertEqual(keys[1], "type")
        self.fail('implement me!')

    def test_message_path(self):
        outgoing = OutgoingMessages()
        dicti = outgoing.path(1, 1, 1, 1, 1, 1)
        keys = list(dicti.keys())
        print(keys)
        print(keys[0])
        print(keys[1])
        print(keys[2])
        print(keys[0] == "from")
        self.assertEqual(keys[0], "from")
        self.assertFalse(keys[0] == "server")
        print(keys[1] == "type")
        self.assertEqual(keys[1], "type")
        print(keys[2] == "payload")
        self.assertEqual(keys[2], "payload")
        self.fail('implement me!')

    def test_message_path_invalid(self):
        outgoing = OutgoingMessages()
        dicti = outgoing.path_invalid(1, 1, 1, 1, 1, 1)
        keys = list(dicti.keys())
        print(keys)
        print(keys[0])
        print(keys[1])
        print(keys[2])
        print(keys[0] == "from")
        self.assertEqual(keys[0], "from")
        print(keys[1] == "type")
        self.assertEqual(keys[1], "type")
        print(keys[2] == "payload")
        self.assertEqual(keys[2], "payload")
        self.fail('implement me!')

    def test_message_select(self):
        outgoing = OutgoingMessages()
        dicti = outgoing.path_select(1, 1, 1)
        keys = list(dicti.keys())
        print(keys)
        print(keys[0])
        print(keys[1])
        print(keys[2])
        print(keys[0] == "from")
        self.assertEqual(keys[0], "from")
        self.assertFalse(keys[0] == "server")
        print(keys[1] == "type")
        self.assertEqual(keys[1], "type")
        print(keys[2] == "payload")
        self.assertEqual(keys[2], "payload")
        self.fail('implement me!')

    def test_message_complete(self):
        outgoing = OutgoingMessages()
        dicti = outgoing.complete()
        keys = list(dicti.keys())
        print(keys)
        print(keys[0])
        print(keys[1])
        print(keys[2])
        print(keys[0] == "from")
        self.assertEqual(keys[0], "from")
        print(keys[1] == "type")
        self.assertEqual(keys[1], "type")
        print(keys[2] == "payload")
        self.assertEqual(keys[2], "payload")
        self.fail('implement me!')


if __name__ == "__main__":
    unittest.main()
