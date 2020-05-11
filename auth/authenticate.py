from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import sys
import utility.facialrecognition as facialrecognition
sys.path.append('..')

class Authenticator():

    def authenticate_user_pass(self, username, password):
        #TODO publish to authenticate-request topic
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'user': username, 'pass': password, 'timestamp': now_time, 'location': location})
        
    
    def authenticate_facialrecognition(self):
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.pub

