#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
from typing import Tuple

from MessageModelManager import OutgoingMessages


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    # DO NOT EDIT THE METHOD SIGNATURE
    def _init_(self, mqtt_client, logger, explorer):
        """
        Initializes communication module, connect to server, subscribe, etc.
        :param mqtt_client: paho.mqtt.client.Client
        :param logger: logging.Logger
        """
        self.explorer = explorer
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
        self.planet_name = ""


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
        type = payload[0]["type"]
        if type == "planet":
            self.process_planet_ready_payload(payload[0])
        if type =="notice":
            self.process_testPlanet_payload(payload[0])
        if type == "path":
            self.process_path_payload(payload[0])
        if type == "pathSelect":
            self.process_pathSelect_payload(payload[0])
        if type == "pathUnveiled":
            self.process_pathUnveiled_payload(payload[0])
        if type == "target":
            self.process_target_payload(payload[0])
        if type == "targetReached":
            self.process_done_payload(payload[0])
        if type == "done":
            self.process_done_payload(payload[0])
        if type == "syntax":
            self.process_syntax_payload(payload[0])
        # YOUR CODE FOLLOWS (remove pass, please!)


    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.
    def send_message(self, topic, message):
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))
        encoded_message = json.dumps(message).encode('utf-8')
        self.client.publish(topic, payload=encoded_message, qos=2, retain=False)



    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"

    def send_ready(self):
        self.send_message(self.topics['general'], self.msg_models.ready())


    def send_test_planet(self, planet_name):
        self.send_message(self.topics['general'], self.msg_models.test_planet(planet_name))

    def send_path(self, start_x, start_y, start_d, end_x, end_y, end_d, path_status):
        self.send_message(self.topics['planet'],
                          self.msg_models.path_msg(start_x, start_y, start_d, end_x, end_y, end_d, path_status))

    def send_path_select(self,startX, startY, startD):
        self.send_message(self.topics['planet'], self.msg_models.path_select(startX, startY, startD))

    def send_target_reached(self,text):
        self.send_message(self.topics['general'], self.msg_models.target_reached(text))

    def send_exploration_completed(self,text):
        self.send_message(self.topics['general'], self.msg_models.exploration_completed(text))

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

    def process_target_payload(self, payload):
        target_x = payload["payload"]["targetX"]
        target_y = payload["payload"]["targetY"]
        target = Tuple[target_x, target_y]
        self.explorer.set_target(target)

    def process_testPlanet_payload(self, payload):
        if payload["payload"]["planetName"] != self.planet_name:
            raise ValueError

    def process_planet_ready_payload(self, payload):
        local_payload = payload["payload"]
        self.topics['planet'] = "planet/" + local_payload["payload"]["planetName"] + "/202"
        self.client.subscribe(self.topics['planet'], qos=2)


    def process_path_payload(self, payload):
        start_x = payload["payload"]["startX"]
        start_y = payload["payload"]["startY"]
        start_direction = payload["payload"]["startDirection"]
        end_x = payload["payload"]["endX"]
        end_y = payload["payload"]["endY"]
        end_direction =["payload"]["endDirection"]
        start = Tuple[start_x, start_y, start_direction]
        end = Tuple[end_x, end_y, end_direction]


    def process_pathSelect_payload(self, payload):
        if payload["payload"]["StartDirection"] != self.explorer.get_directions:

    def process_pathUnveiled_payload(self, payload):


    def process_done_payload(self, payload):
        pass

    def process_unknown_payload(self, payload):
        pass

    def process_syntax_payload(self, payload):
        pass
