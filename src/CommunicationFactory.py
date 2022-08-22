import json
import paho.mqtt.client as mqtt
import ssl

import communication


class CommunicationFactory:
    @classmethod
    def getInstance(cls, client, logger, explorer):
        # It looks weird but it really makes sense.
        # It would make even more sense if I wasn't bound by the templates (:
        # The client and some parts of the communication are implemented in the main method
        # And I'm not allowed to touch it
        # Having said that, I do really care about reducing the unnecessary coupling
        return communication.Communication(client, logger, explorer)

    