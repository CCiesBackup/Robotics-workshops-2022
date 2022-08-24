import json
import paho.mqtt.client as mqtt
import ssl

import communication


class CommunicationFactory:
    singleton = None
    @classmethod
    def getInstance(cls, client, logger, explorer):
        # Please initialize the communication module only through this class!!!

        # To prevent the users from creating more than one instance of the communication class
        if cls.singleton is None:
            cls.singleton = communication.Communication(client, logger, explorer)
        return cls.singleton

