"""
module that contains logic for subscribe.
"""
import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from utility.facialrecognition.encode_one import EncodeOne 
import pickle
import hashlib
env_path = './.env'
load_dotenv(dotenv_path=env_path)

##hashes
in_hash_md5 = hashlib.md5()

DATASET_FOLDER = "./utility/facialrecognition/dataset" 
DATASET_EXTENSION = ".jpg"

BROKER_AGENT_IP = str(os.getenv("AGENT_IP"))
PORT = int(os.getenv("PORT"))


class Subscriber:
    """
    A class that contains subscriber logic.
    """

    def __init__(self):
        """
        initialises the topic routes which it will listen to, ip address, port, username.
        """
        self.AUTH_RESP_FR_TOPIC = "AUTH/RESP/FR"
        self.AUTH_RESP_UP_TOPIC = "AUTH/RESP/UP"
        self.RETURN_TOPIC = "RETURN"
        self.broker_address = BROKER_AGENT_IP
        self.port = PORT
        self.USERNAME = "test"

    def on_connect(self, client, userdata, flags, rc):
        """
        subscribe to the topics that were initialised.
        """
        if rc == 0:
            print("connection established to %s, returned code=" %(self.broker_address), rc)
            client.subscribe(self.AUTH_RESP_FR_TOPIC)
            client.subscribe(self.AUTH_RESP_UP_TOPIC)
            client.subscribe(self.RETURN_TOPIC)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        """
        prints out the topic and payload, prints to console different messages
        depending on topic. Also handles saving pictures if topic is facial 
        recognition.
        """
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
            if msg.payload == 'Return':
                print('RETURNED CAR')
            else:
                print("RETURN CAR DENIED")

    def process_message(self, msg):
        """ 
        this is the main receiver code. Processes the message, check if everything 
        arrives succesfuly.
        """
        if len(msg)==200: #is header or end
            msg_in=msg.decode("utf-8")
            msg_in=msg_in.split(",,")
            print("[PROCESS]", msg_in)
            if msg_in[0]=="header": #is it really last packet?
                self.USERNAME = msg_in[1]
                # print("[DEBUG] 1")
                return False
        
        # print("[DEBUG]")
        return True
            

    def on_log(self, client, userdata, level, buf):
        """
        function to run for logging.
        """
        print("log ", buf)
    
    def subscribe(self):
        """
        initialises mqtt client. binds on connect, message and log functions to
        the client. connects to the address and starts loop.
        """
        # initialise MQTT Client
        client = mqtt.Client("tomasterpi")

        # binds functions defined above, on connection, message and log
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log
        print(self.broker_address)

        client.connect(self.broker_address)
        client.loop_forever()
       
