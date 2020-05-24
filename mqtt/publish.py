"""
module that contains publish logic.
"""
import paho.mqtt.client as mqtt
import json
import logging
import os
from dotenv import load_dotenv
load_dotenv()
env_path="./.env"
load_dotenv(dotenv_path=env_path)

BROKER_MASTER_IP = str(os.getenv("MASTER_IP"))
PORT = int(os.getenv("PORT"))

class Publisher:
    """
    Class that contains publish logic. when given a payload and route
    it will publish to the correct route.
    
    Methods
    -------
    __init__(self):
        initialises routes that it will publish to, ip address of MP and port.
    on_publish(self, client, userdata, result):
        function to run on successful publish
    on_disconnect(self, client, userdata, rc):
        function to run on disconnect, contains clean up code, and stops the running of the client.
    publish(self, paylod, auth):
        initialises client and binds functions, publish received payload to MP and disconnects.
    """

    def __init__(self):
        """
        initialises routes that it will publish to, ip address of MP and port.
        """
        self.AUTH_FR_TOPIC = "AUTH/FR"
        self.AUTH_UP_TOPIC = "AUTH/UP"
        self.BROKER_ADDRESS = BROKER_MASTER_IP
        self.BROKER_PORT = PORT

    def on_publish(self, client, userdata, result):
        """
        function to run on successful publish
        """
        print("piot data published \n")
        print(result)
        print(userdata)
        pass

    def on_disconnect(self, client, userdata, rc):
        """
        function to run on disconnect
        """
        # logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("client disconnected OK")

    def publish(self, payload, topic):
        """
        initialises client and binds functions, publish received payload to MP and disconnects.
        """
        # create new instance
        client = mqtt.Client("tomasterpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect

        # set broker address of raspberry pis
        # connect to pi
        client.connect(self.BROKER_ADDRESS, self.BROKER_PORT)

        # Publish to topic
        if topic == 'UP':
            client.publish(self.AUTH_UP_TOPIC, json.dumps(payload))
            client.disconnect()
        elif topic == 'FR':
            client.publish(self.AUTH_FR_TOPIC, json.dumps(payload))
            client.disconnect()
        elif topic == 'RETURN':
            client.publish('RETURN', json.dumps(payload))
            client.disconnect()

