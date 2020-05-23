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
sys.path.append('..')

PICKLE_EXTENSION = '.pickle'
class Authenticator():
    """
    Manages authentication using password and facial recognition.

    Methods
    -------
    authenticate_user_pass(self, username, password):
        When user chooses to authenticate with password, this function will be used.
        Sends MP the username and password with location of the car.
    authenticate_facialrecognition(self, username):
        If user chooses facial recognition, it will request user picture from MP. user captures
        their face, runs facial recognition module and returns True/False.
    """

    def authenticate_user_pass(self, username, password):
        #TODO publish to authenticate-request topic
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'username': username, 'pass': password, 'agentid':Database().get_id(), 'timestamp': now_time, 'location': location}, 'UP')
        
    
    def authenticate_facialrecognition(self, username):
        # print("[DEBUG] initiate video stream")
        #vs = VideoStream()
        #vs.stream(username)
    #If exists, check if booked, then authenticate
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'username': username, 'timestamp': now_time, 'location': location, 'type': 'Encode Face'}, 'FR')
        print("[DEBUG] initiating videostream")
        vs = VideoStream()
        vs.stream(username)
        fr = RecognizeUserFace()
        return fr.run(username)

