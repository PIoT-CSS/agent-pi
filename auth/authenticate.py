from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import sys
import utility.facialrecognition as RecognizeUserFace
sys.path.append('..')

class Authenticator():

    def authenticate_user_pass(self, username, password):
        #TODO publish to authenticate-request topic
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'user': username, 'pass': password, 'timestamp': now_time, 'location': location}, 'UP')
        
    
    def authenticate_facialrecognition(self, username):
        #Check if the encoding exists 
        try:
            pickle_file = username + PICKLE_EXTENSION
            data = pickle.loads(open(pickle_file, "rb").read())
            pub = Publisher()
            now_time = datetime.datetime.now().isoformat()
            location = Geolocation().run()
            pub.publish({'user': username, 'timestamp': now_time, 'location': location, 'type': "Check"}, 'FR')
            fr = RecognizeUserFace()
            fr.run(username)            
        except:
        #If exists, check if booked, then authenticate
            pub = Publisher()
            now_time = datetime.datetime.now().isoformat()
            location = Geolocation().run()
            pub.publish({'user': username, 'timestamp': now_time, 'location': location, 'type': 'Encode Face'}, 'FR')
            fr = RecognizeUserFace()
            fr.run(username)

