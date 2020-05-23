"""
module to startup mqtt subscriber.
"""
# startup
from mqtt.subscribe import Subscriber

def start_up():
    """
    starts mqtt subscriber.
    """
    sub = Subscriber()
    sub.subscribe()

if __name__ == "__main__":
    start_up()
