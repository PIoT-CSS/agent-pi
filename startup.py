# startup
from mqtt.subscribe import Subscriber

def start_up():
    sub = Subscriber()
    sub.subscribe()

if __name__ =="__main__":
    start_up()
