import videostream.videostream as VideoStream
from pyzbar import pyznar
import argparse
import cv2

"""
QRDetection.py module, its functionality is involved in detecting the Engineers employee credentials to verify and record the individual has performed maintenance on the vehicle.

"""
class QRDetection:
    """
    A class to read QR Codes
    """
    def __init__(self):
        self.VideoStream = VideoStream()

    def detect(self):
        #INIT TODO

    def run(self):
        #INIT TODO

if __name__ == "__main__":
    QRDetection().run()