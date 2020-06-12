"""
test_mqtt is for testing if mqtt protocol sends data properly
"""

import paho.mqtt.client as mqtt
import time
import json

HELLO_TOPIC = "HELLO"
HELLO_MSG = "Hello World!"

LIST_TOPIC = "LIST"
LIST_MSG = [1, 2, 3]

LOCALHOST = "localhost"

# Init client
client = mqtt.Client("Test")

# Functions to bind subscriber client.
def on_connect(client, userdata, flags, rc):
    """
    Check if MQTT connection has been established.

    :param client: the client instance for this callback
    :type client: Client
    :param userdata: the private user data as
        set in Client() or user_data_set()
    :type userdata: any
    :param flags: response flags sent by the broker
    :type flags: dict
    :param rc: result of connection
    :type rc: integer
    """
    if rc == 0:
        print("Connected to ", LOCALHOST)
    else:
        print("Bad connection")

def on_message(client, userdata, msg):
    """
    Decode the payload and store it.

    :param client: the client instance for this callback
    :type client: Client
    :param userdata: the private user data as set in Client()
        or user_data_set()
    :type userdata: any
    :param msg: an instance of MQTTMessage. This is a class with members
        topic, payload, qos, retain.
    :type msg: MQTTMessage
    """
    payload = msg.payload
    m_decode = msg.payload.decode("utf-8", "ignore")
    print("Payload received from {} topic: {}" \
        .format(msg.topic, str(m_decode)))
    if msg.topic == HELLO_TOPIC:
        HELLO_RESP = str(m_decode)
        assert HELLO_MSG == HELLO_RESP
    elif msg.topic == LIST_TOPIC:
        LIST_RESP = json.load(m_decode)
        assert LIST_MSG == LIST_RESP

def on_disconnect(client, userdata, flags, rc=0):
    """
    Check if MQTT connection has been terminated.

    :param client: the client instance for this callback
    :type client: Client
    :param userdata: the private user data as
        set in Client() or user_data_set()
    :type userdata: any
    :param flags: response flags sent by the broker
    :type flags: dict
    :param rc: result of connection
    :type rc: integer
    """
    print("Disconnected")

def test_mqtt():
    """
    Test MQTT functions by connecting to broker, subscribing to topics
    and publish data to topics and then terminating the connection.
    """
    # Binds functions
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(LOCALHOST) # Connect to broker
    client.loop_start() # Start loop

    client.subscribe(HELLO_TOPIC)
    client.publish(HELLO_TOPIC, HELLO_MSG)

    client.subscribe(LIST_TOPIC)
    client.publish(LIST_TOPIC, json.dumps(LIST_MSG))

    client.loop_stop() # Stop loop
    client.disconnect() # disconnect
