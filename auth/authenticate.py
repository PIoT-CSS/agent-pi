from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import sys
sys.path.append('..')

class Authenticator():

    def authenticate_user_pass(self, username, password):
        #TODO publish to authenticate-request topic
        pub = Publisher()
        now_time = datetime.datetime.isoformat
        authPayload = {}
        authPayload['user'] = username
        authPayload['pass'] = password
        authPayload['datetime'] = now_time
        authPayload['location'] = Geolocation()
        print("PUBLISH")
        pub.publish(authPayload)

        #TODO subcribe to unlock reponse to authenticate
