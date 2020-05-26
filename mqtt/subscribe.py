"""
module that contains logic for subscribe.
"""
import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from utility.facialrecognition.encode_one import EncodeOne
from auth.authenticate import Authenticator
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
        initialises the topic routes which it will listen to, 
        ip address, port, username.
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

        :param client: the client instance for this callback
        :type client: Client
        :param userdata: the private user data as
        set in Client() or user_data_set()
        :type userdata: any
        :param flags: response flags sent by the broker
        :type flags: dict
        :param rc: result of connection
        :type rc: integer
        """
        if rc == 0:
            print("connection established to %s, returned code=" \
                %(self.broker_address), rc)
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

        :param client: the client instance for this callback
        :type client: Client
        :param userdata: the private user data as set in Client()
        or user_data_set()
        :type userdata: any
        :param msg: an instance of MQTTMessage. This is a class with members
        topic, payload, qos, retain.
        :type msg: MQTTMessage
        """
        payload = msg.payload
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))

        if payload == 'Unlocked':
            print(msg.topic + ' Unlocked!')
        else:
            if msg.topic == 'AUTH/RESP/FR':
                if payload == 'Car unlock failed':
                    print('AUTH/RESP/FR denied!')
                elif self.process_message(payload):
                    print("USERNAME", self.USERNAME)
                    directory = DATASET_FOLDER+"/"+self.USERNAME+"/"
                    save_img = "{}{}{}".format(directory,
                                            self.USERNAME,
                                            DATASET_EXTENSION)
                    print("[WRITING] ", msg.payload)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(save_img, "wb") as fh:
                        fh.write(payload)
                    print("Image Received")
                    #create encoding
                    enc = EncodeOne()
                    enc.run(self.USERNAME)
                    Authenticator().perform_facialrecognition(self.USERNAME)
            elif msg.topic == 'AUTH/RESP/UP':
                print('AUTH/RESP/UP denied!')
            elif msg.topic == 'RETURN':
                if msg.payload == 'Returned':
                    print('RETURNED CAR')
                else:
                    print("RETURN CAR DENIED")

    def process_message(self, msg):
        """
        this is the main receiver code. Processes the message, check if
        everything arrives succesfuly.
        
        :param msg: message that was published
        :type msg: json, string, bytes
        :return: boolean
        :rtype: boolean
        """
        if len(msg)==200: #is header or end
            msg_in=msg.decode("utf-8")
            msg_in=msg_in.split(",,")
            print("[PROCESS]", msg_in)
            if msg_in[0]=="header": #is it really last packet?
                self.USERNAME = msg_in[1]
                return False
        
        return True
            

    def on_log(self, client, userdata, level, buf):
        """
        function to run for logging.

        :param client: the client instance for this callback
        :type client: Client
        :param userdata: the private user data as set in Client() or
        user_data_set()
        :type userdata: any
        :param level: severity of the message
        :type level: MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
        MQTT_LOG_ERR, MQTT_LOG_DEBUG
        :param buf: message buffer
        :type buf: bytes
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
       
