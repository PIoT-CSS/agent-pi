import mqtt.publish as Publisher

def publish_data(payload):
    pub = Publisher
    pub.publish_data('test')