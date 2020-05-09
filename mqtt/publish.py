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

'''
methods
- connect()
- disconnect()
- subscribe()
- publish ()
'''


class Publisher:

    def __init__(self):
        self.topic = "test"
        self.broker_address = BROKER_MASTER_IP
        self.port = PORT

    def on_publish(self, client, userdata, result):
        print("data published \n")
        pass

    def on_disconnect(self, client, userdata, rc):
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("client disconnected OK")

    def publish(self, payload):
        # setting topic to publish to
        topic = "test"
        id = "id"
        payload_new = {'pi-id' : id, 'payload': payload}

        # create new instance
        client = mqtt.Client("tomasterpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect

        # set broker address of raspberry pis
        # connect to pi
        client.connect(self.broker_address, self.port)

        # Publish to topic
        client.publish(self.topic, json.dumps(payload_new))
        client.disconnect()

