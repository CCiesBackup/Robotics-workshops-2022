#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl

from MessageModelManager import OutgoingMessages


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    # DO NOT EDIT THE METHOD SIGNATURE
    def __init__(self, mqtt_client, logger):
        """
        Initializes communication module, connect to server, subscribe, etc.
        :param mqtt_client: paho.mqtt.client.Client
        :param logger: logging.Logger
        """
        # DO NOT CHANGE THE SETUP HERE
        self.client = mqtt_client
        self.logger = logger
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.on_message = self.safe_on_message_handler
        # Add your client setup here
        self.client.username_pw_set('202', password='psguk8hU7n')
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.topics = {'general': 'explorer/202', 'planet': "", 'tests': 'comtest/202'}
        self.client.loop_start()
        self.client.subscribe(self.topics['general'], qos=2)
        self.msg_models = OutgoingMessages()


    # DO NOT EDIT THE METHOD SIGNATURE
    def on_message(self, client, data, message):
        """

        planetname = data[0]
        "pathSelected"
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))
        self.logger.debug(json.dumps(payload, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        pass

    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.
    def send_message(self, topic, message):
        """
        Sends given message to specified channel
        :param top: String
        :param message: Object
        :return: void
        """
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        pass

    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"

    def send_ready(self):
        self.send_message(self.topics['general'], self.msg_models.ready())

    def send_test_planet(self, planet_name):
        self.send_message(self.topics['general'], self.msg_models.test_planet(planet_name))


    def safe_on_message_handler(self, client, data, message):
        """
        Handle exceptions thrown by the paho library
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise


class Message:
    pass