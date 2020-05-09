# main
from mqtt.publish import Publisher

def main():
    pub = Publisher()
    pub.publish('test')


if __name__ == "__main__":
    main()
    
