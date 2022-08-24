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
        self.explorer = ExplorationManager()
        self.communication = Communication(client, mock_logger, self.explorer)

    def test_message_ready(self):
        ## fail!


        """
        This test should check the syntax of the message type "ready"
        """
        self.fail('implement me!')

    def test_message_path(self):
        """
        This test should check the syntax of the message type "path"
        """
        self.fail('implement me!')

    def test_message_path_invalid(self):
        """
        This test should check the syntax of the message type "path" with errors/invalid data
        """
        self.fail('implement me!')

    def test_message_select(self):


        self.fail('implement me!')

    def test_message_complete(self):
        """
        This test should check the syntax of the message type "explorationCompleted" or "targetReached"
        """
        self.fail('implement me!')


if __name__ == "__main__":
    unittest.main()
