import json
import paho.mqtt.client as mqtt
import ssl

import communication


class CommunicationFactory:
    singleton = None
    @classmethod
    def getInstance(cls, client, logger, explorer):
        # Please initialize the communication module only through this method!!!

        # To prevent the users from creating more than one instance of the communication class
        if cls.singleton is None:
            cls.singleton = communication.Communication(client, logger, explorer)
        return cls.singleton

    @classmethod
    def get_initialized_instance(cls):
        if cls.singleton is not None:
            return cls.singleton
        else:
            raise TypeError("Module not initialized. Use the getInstance method instead!")

