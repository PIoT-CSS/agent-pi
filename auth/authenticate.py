"""
module manages authentication process with mqtt.
"""
from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import sys
from utility.facialrecognition.recognizeuserface import RecognizeUserFace
from utility.videostream.videostream import VideoStream
from data.database import Database
import pickle
import time
import os

# location for saving images
QRCODE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../utility/videostream/qrcode.json'))

# Pickle Extension
PICKLE_EXTENSION = '.pickle'
class Authenticator():
    """
    Manages authentication using password and facial recognition.
    """

    def authenticate_user_pass(self, username, password):
        """
        When user chooses to authenticate with password, this function will be used.
        Sends MP the username and password with location of the car.

        :param username: user name that's being authenticated
        :type username: string
        :param password: password that's being authenticated
        :type password: string
        """
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'username': username, 
                     'pass': password, 
                     'agentid':Database().get_id(), 
                     'timestamp': now_time, 
                     'location': location}, 'UP')
        
    
    def authenticate_facialrecognition(self, username):
        """
        If user chooses facial recognition, 
        it will request user picture from MP. user captures
        their face, runs facial recognition module and returns True/False.

        :param username: user name that's being authenticated
        :type username: string
        :return: boolean
        :rtype: boolean
        """
        #If exists, check if booked, then authenticate
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        agentId = Database().get_id()
        pub.publish({'username': username, 'timestamp': now_time, 
                     'location': location, 'agentid':agentId,
                     'type': 'Encode Face'}, 'FR')
        return True

    def perform_facialrecognition(self, username):
        vs = VideoStream()
        vs.stream(username)
        fr = RecognizeUserFace()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        agentId = Database().get_id()
        if fr.run(username):
            pub = Publisher()
            pub.publish({'username': username, 'timestamp': now_time, 
                'location': location, 'agentid':agentId,
                'type': 'Unlock'}, 'FR')
            return True
        return False

    def id_engineer(self):
        vs = VideoStream()
        vs.stream('Engineer','qr')
        payload = json.loads(QRCODE_PATH)
        if payload:
            pub = Publisher()
            pub.publish(json.dumps(payload), 'ENG')
            return True
        else:
            return False