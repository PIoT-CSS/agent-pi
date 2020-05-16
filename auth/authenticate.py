from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import sys
from utility.facialrecognition.recognizeuserface import RecognizeUserFace
from utility.videostream.videostream import VideoStream
import pickle
import time
sys.path.append('..')

PICKLE_EXTENSION = '.pickle'
class Authenticator():

    def authenticate_user_pass(self, username, password):
        #TODO publish to authenticate-request topic
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'username': username, 'pass': password, 'timestamp': now_time, 'location': location}, 'UP')
        
    
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
            if fr.run(username):
                return True

            return False

