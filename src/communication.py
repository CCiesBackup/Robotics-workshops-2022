#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import ssl
from typing import Tuple, Any

from MessageModelManager import OutgoingMessages
from MessageProcessingException import MessageProcessingException


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    # DO NOT EDIT THE METHOD SIGNATURE

    def __init__(self, mqtt_client, logger, explorer):
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
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        # Add your client setup here
        self.client.username_pw_set('202', password='psguk8hU7n')
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.topics = {'general': 'explorer/202', 'planet': "", 'tests': 'comtest/202'}
        self.client.loop_start()
        self.client.subscribe(self.topics['general'], qos=2)
        self.msg_models = OutgoingMessages()
        self.planet_name = ""
        self.exam_mode = True

    # DO NOT EDIT THE METHOD SIGNATURE
    def on_connect(self, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_disconnect(self):
        print("disconnected from the server")

    def on_message(self, client, data, message):
        print("Omg, we've actually received a message!!!")
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))
        print(f"Following data has been received: {payload}")
        self.logger.debug(json.dumps(payload, indent=2))
        message_type = payload[0]["type"]
        payload_from_value = payload[0]["from"]
        if payload_from_value == "server":
            if message_type == "planet":
                self.process_planet_ready_payload(payload[0])
                return
            if message_type == "notice":
                self.process_testPlanet_payload(payload[0])
                return
            if message_type == "path":
                self.process_path_payload(payload[0])
                return
            if message_type == "pathSelect":
                self.process_pathSelect_payload(payload[0])
                return
            if message_type == "pathUnveiled":
                self.process_pathUnveiled_payload(payload[0])
                return
            if message_type == "target":
                self.process_target_payload(payload[0])
                return
            if message_type == "targetReached":
                self.process_done_payload(payload[0])
                return
            if message_type == "done":
                self.process_done_payload(payload[0])
                return
            if message_type == "syntax":
                self.process_syntax_payload(payload[0])
                return
            else:
                self.process_unknown_payload(payload[0])
        elif payload_from_value == "debug":
            if self.exam_mode:
                print("Received a debug message in the process of the exam. Weird occurrence...")
            else:
                self.process_syntax_payload(payload[0])
        else:
            self.process_unknown_payload(payload[0])

    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.
    def send_message(self, topic, message):
        print(f" sent {message} to {topic} ")
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))
        encoded_message = json.dumps(message).encode('utf-8')
        self.client.publish(topic, payload=encoded_message, qos=2, retain=False)

    def send_ready(self):
        self.send_message(self.topics['general'], self.msg_models.ready())
        if not self.exam_mode:
            self.send_message(self.topics['tests'], self.msg_models.ready())

    def send_test_planet(self, planet_name):
        self.exam_mode = False
        self.planet_name = planet_name
        self.client.subscribe(self.topics['tests'], qos=2)
        self.send_message(self.topics['general'], self.msg_models.test_planet(planet_name))

    def send_path(self, start_x, start_y, start_d, end_x, end_y, end_d, path_status):
        self.send_message(self.topics['planet'],
                          self.msg_models.path_msg(start_x, start_y, start_d, end_x, end_y, end_d, path_status))
        if not self.exam_mode:
            self.send_message(self.topics['tests'],
                              self.msg_models.path_msg(start_x, start_y, start_d, end_x, end_y, end_d, path_status))

    def send_path_select(self, start_x, start_y, start_d):
        self.send_message(self.topics['planet'], self.msg_models.path_select(start_x, start_y, start_d))
        if not self.exam_mode:
            self.send_message(self.topics['tests'], self.msg_models.path_select(start_x, start_y, start_d))

    def send_target_reached(self, text):
        self.send_message(self.topics['general'], self.msg_models.target_reached(text))
        if not self.exam_mode:
            self.send_message(self.topics['tests'], self.msg_models.target_reached(text))

    def send_exploration_completed(self, text):
        self.send_message(self.topics['general'], self.msg_models.exploration_completed(text))
        if not self.exam_mode:
            self.send_message(self.topics['tests'], self.msg_models.exploration_completed(text))

    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"
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
        print(f"Ok, test planet set! Testing on the planet: {payload['payload']['planetName']} ")

    def process_planet_ready_payload(self, payload):
        self.planet_name = payload["payload"]["planetName"]
        self.topics['planet'] = "planet/" + payload["payload"]["planetName"] + "/202"
        print(f"Subscribing to the topic: {self.topics['planet']}")
        self.client.subscribe(self.topics['planet'], qos=2)

        set_off_position = (payload["payload"]["startX"], payload["payload"]["startY"])
        set_off_orientation = payload["payload"]["startOrientation"]
        self.explorer.current_position = set_off_position
        self.explorer.current_orientation = set_off_orientation

    def process_path_payload(self, payload):
        start_x = payload["payload"]["startX"]
        start_y = payload["payload"]["startY"]
        start_direction = payload["payload"]["startDirection"]
        end_x = payload["payload"]["endX"]
        end_y = payload["payload"]["endY"]
        end_direction = payload["payload"]["endDirection"]
        start = ((start_x, start_y), start_direction)
        end = ((end_x, end_y), end_direction)
        weight = (-1) if payload["payload"]["pathStatus"] == "blocked" else payload["payload"]["pathWeight"]
        self.explorer.add_path_intern(start, end, weight)

    def process_pathSelect_payload(self, payload):
        self.explorer.set_path_select(payload["payload"]["startDirection"])

    def process_pathUnveiled_payload(self, payload):
        # The functioning of pathUnveiled and path messages is similar, the only difference
        # is that in pathUnveiled we overwrite some existing data
        # whereas path is just a confirmation, we insert some data into the database for the first time
        # data[path] = data # path
        # data[path] = data2 --> data has been superseded by data2 as in #pathUnveiled;
        # the inner functioning
        # is the same, therefore there is no need to implement another function
        # this one is there for clarity (:
        self.process_path_payload(payload)

    def process_done_payload(self, payload):
        if payload["type"] == "done":
            self.client.loop_stop()
            self.client.disconnect()
            print("有一天我会回来……然后我会称霸整个世界!!!!")
            print("Task completed, connection closed!")

        else:
            self.explorer.rebuke()

    def process_unknown_payload(self, payload):
        print(f" payload of type: {payload['type']} received - processing mismatch! ")
        print("The payload: ")
        print(payload)
        # throw new MessageProcessingException();
        raise MessageProcessingException()

    def process_syntax_payload(self, payload):
        for string in payload["payload"].values():
            print(string)
