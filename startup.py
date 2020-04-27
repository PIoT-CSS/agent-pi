# startup
import mqtt.publish as Publisher

def main():
    pub = Publisher()
    pub.publish('test')


if __name__ == "__main__":
    main()
    