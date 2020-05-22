"""
module to start mqtt publisher.
"""
# main
from mqtt.subscribe import Subscriber
from mqtt.publish import Publisher
from utility.geolocation import Geolocation

def main():
    """
    starts mqtt publisher.
    """
    # sub = Subscriber()
     #sub.subscribe()
     pub = Publisher()
     pub.publish('alex', 'FR')
     #geo = Geolocation()
     #print(geo.run())

if __name__ == "__main__":
    main()
    
