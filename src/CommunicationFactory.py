import json
import paho.mqtt.client as mqtt
import ssl

import communication


class CommunicationFactory:
    @classmethod
    def getInstance(cls, logger):
        client = mqtt.Client(client_id="202", clean_session=False, protocol=mqtt.MQTTv31)

        return communication.Communication(client, logger)