import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)

BROKER_AGENT_IP = str(os.getenv("AGENT_IP"))
PORT = int(os.getenv("PORT"))


class Subscriber:

    def __init__(self):
        self.topic = "test"
        self.broker_address = BROKER_AGENT_IP
        self.port = PORT

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established to %s, returned code=" %(self.broker_address), rc)
            client.subscribe(self.topic)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        # TODO: when payload arrives, initiate AUTH

    def on_log(self, client, userdata, level, buf):
        print("log ", buf)

    def subscribe(self):
        # initialise MQTT Client
        client = mqtt.Client("tomasterpi")

        # binds functions defined above, on connection, message and log
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log
        print(self.broker_address)
        # client.username_pw_set(user, password)
        client.connect(self.broker_address)
        client.loop_forever()
