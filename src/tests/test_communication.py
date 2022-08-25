#!/usr/bin/env python3

import unittest.mock
import paho.mqtt.client as mqtt
import uuid

from ExplorationManager import ExplorationManager
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
        explorer = ExplorationManager()
        self.communication = Communication(client, mock_logger, explorer)
        self.outgoing = OutgoingMessages()

    def test_message_ready(self):

        dicti = self.outgoing.ready()
        keys = list(dicti.keys())
        self.assertEqual(keys[0], "from")
        self.assertEqual(keys[1], "type")

    def test_message_path(self):
        dicti = self.outgoing.path_msg(1, 1, 1, 1, 1, 1, "free")
        keys = list(dicti.keys())
        intern_keys = list(dicti["payload"].keys())
        self.assertEqual(intern_keys[0], "startX")
        self.assertEqual(intern_keys[1], "startY")
        self.assertEqual(intern_keys[2], "startDirection")
        self.assertEqual(intern_keys[3], "endX")
        self.assertEqual(intern_keys[4], "endY")
        self.assertEqual(intern_keys[5], "endDirection")
        self.assertEqual(intern_keys[6], "pathStatus")
        self.assertEqual(keys[0], "from")
        self.assertFalse(keys[0] == "server")
        self.assertEqual(keys[1], "type")
        self.assertEqual(keys[2], "payload")


    def test_message_path_invalid(self):
        dicti = self.outgoing.path_msg(1, 1, 1, 1, 1, 1, "blocked")
        keys = list(dicti.keys())
        intern_keys = list(dicti["payload"].keys())
        self.assertEqual(intern_keys[0], "startX")
        self.assertEqual(intern_keys[1], "startY")
        self.assertEqual(intern_keys[2], "startDirection")
        self.assertEqual(intern_keys[3], "endX")
        self.assertEqual(intern_keys[4], "endY")
        self.assertEqual(intern_keys[5], "endDirection")
        self.assertEqual(intern_keys[6], "pathStatus")
        self.assertEqual(keys[0], "from")
        self.assertEqual(keys[1], "type")
        self.assertEqual(keys[2], "payload")


    def test_message_select(self):
        dicti = self.outgoing.path_select(1, 1, 1)
        keys = list(dicti.keys())
        intern_keys = list(dicti["payload"].keys())
        self.assertEqual(intern_keys[0], "startX")
        self.assertEqual(intern_keys[1], "startY")
        self.assertEqual(intern_keys[2], "startDirection")
        self.assertEqual(keys[0], "from")
        self.assertFalse(keys[0] == "server")
        self.assertEqual(keys[1], "type")
        self.assertEqual(keys[2], "payload")


    def test_message_complete(self):
        dicti = self.outgoing.exploration_completed("Dupa")
        keys = list(dicti.keys())
        intern_keys = list(dicti["payload"].keys())
        self.assertEqual(intern_keys[0], "message")
        self.assertEqual(keys[0], "from")
        self.assertEqual(keys[1], "type")
        self.assertEqual(keys[2], "payload")

    def test_target_reached(self):
        dicti = self.outgoing.target_reached("Dupa")
        keys = list(dicti.keys())
        intern_keys = list(dicti["payload"].keys())
        self.assertEqual(intern_keys[0], "message")
        self.assertEqual(keys[0], "from")
        self.assertEqual(keys[1], "type")
        self.assertEqual(keys[2], "payload")


if __name__ == "__main__":
    unittest.main()
