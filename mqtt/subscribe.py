import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from utility.facialrecognition.encoding.encode_one import EncodeOne 
import pickle
import hashlib
env_path = './.env'
load_dotenv(dotenv_path=env_path)

##hashes
in_hash_md5 = hashlib.md5()

DATASET_FOLDER = "./utility/facialrecognition/encoding/dataset" 
DATASET_EXTENSION = ".jpg"

BROKER_AGENT_IP = str(os.getenv("AGENT_IP"))
PORT = int(os.getenv("PORT"))


class Subscriber:

    def __init__(self):
        self.AUTH_RESP_FR_TOPIC = "AUTH/RESP/FR"
        self.AUTH_RESP_UP_TOPIC = "AUTH/RESP/UP"
        self.RETURN_TOPIC = "RETURN"
        self.broker_address = BROKER_AGENT_IP
        self.port = PORT
        self.USERNAME = "test"

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established to %s, returned code=" %(self.broker_address), rc)
            client.subscribe(self.AUTH_RESP_FR_TOPIC)
            client.subscribe(self.AUTH_RESP_UP_TOPIC)
            client.subscribe(self.RETURN_TOPIC)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        payload = msg.payload
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        # TODO: when payload arrives, initiate AUTH
        if msg.topic == 'AUTH/RESP/FR':
            if self.process_message(payload):
                print("USERNAME", self.USERNAME)
                save_img = "{}/{}/{}{}".format(DATASET_FOLDER, self.USERNAME, self.USERNAME, DATASET_EXTENSION)
                print("[WRITING] ", msg.payload)
                with open(save_img, "wb") as fh:
                    fh.write(payload)
                print("Image Received")
                #create encoding
                enc = EncodeOne()
                enc.run(self.USERNAME)
        elif msg.topic == 'AUTH/RESP/UP':
            print('AUTH/RESP/UP Unlocked!')
        elif msg.topic == 'RETURN':
            print('RETURNED CAR')

    def process_message(self, msg):
        """ 
            This is the main receiver code
        """
        if len(msg)==200: #is header or end
            msg_in=msg.decode("utf-8")
            msg_in=msg_in.split(",,")
            print("[PROCESS]", msg_in)
            if msg_in[0]=="header": #is it really last packet?
                self.USERNAME = msg_in[1]
                print("[DEBUG] 1")
                return False
        
        print("[DEBUG]")
        return True
            

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

        client.connect(self.broker_address)
        client.loop_forever()
        
