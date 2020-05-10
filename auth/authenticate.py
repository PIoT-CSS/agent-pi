from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import sys
sys.path.append('..')

class Authenticator():

    def authenticate_user_pass(self, username, password):
        #TODO publish to authenticate-request topic
        pub = Publisher()
        now_time = datetime.datetime.now().isoformat()
        location = Geolocation().run()
        pub.publish({'user': username, 'pass': password, 'timestamp': now_time, 'location': location})

        #TODO subcribe to unlock reponse to authenticate
