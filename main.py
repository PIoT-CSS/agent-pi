# main
from mqtt.subscribe import Subscriber
from mqtt.publish import Publisher
from utility.geolocation import Geolocation

def main():
#    sub = Subscriber()
 #   sub.subscribe()
   # pub = Publisher()
   # pub.publish('test')
     geo = Geolocation()
     print(geo.run())

if __name__ == "__main__":
    main()
    
