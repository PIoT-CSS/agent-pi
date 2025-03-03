"""
videostream.py module, it's job is to start the camera in a thread
allowing it to warm up.
"""
from __future__ import print_function
from .webcamvideostream import WebcamVideoStream
from .fps import FPS
#from webcamvideostream import WebcamVideoStream
#from fps import FPS
import imutils
import cv2
import face_recognition
import os
import time
import datetime
from pyzbar import pyzbar
import json
import argparse


# location for saving images
INPUT_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../facialrecognition/input'))
fps = FPS().start()


class VideoStream():
    """
    A class containing method to save picture captured by webcam, & qrdetection
    """

    def stream(self, username, purpose):
        """
        created a *threaded* video stream, allow the camera sensor to warmup,
        and start the FPS counter. Displays the webcam when needed, captures
        a picture and saves it or can detect the qrcode, read the data from it and saves it.

        :param username: username that's using the camera
        :type username: string
        """
        vs = WebcamVideoStream(src=0).start()

        if purpose == 'qr':
            self.qr_detect(vs)
        elif purpose == 'fr':
            self.facial_recognition(vs, username)

    def qr_detect(self, vs):
        """
        playback stream, for the user to scan QRCode. The content of the QRCode is saved in json format,
        and then close the stream. 

        :param vs: videostream object
        :type VideoStream: VideoStream
        """
        # loop over some frames...this time using the threaded stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            # Open CSV to save details from QR Code
            found = set()
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                if barcodeData not in found:
                    with open('qrcode.json', 'w') as outfile:
                        json.dump(barcodeData, outfile)
                        found.add(barcodeData)

            cv2.imshow("Frame", frame)
            fps.update()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        
        
    
    def facial_recognition(self, vs, username):
        """
        playback stream, for the user to scan face. Save image users face for face recognition,
        and then close the stream. 

        :param vs: videostream object
        :type VideoStream: VideoStream
        :param username: username that's using the camera
        :type username: string
        """
        # loop over some frames...this time using the threaded stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            cv2.imshow("Frame", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                path = "{}/{}.jpg".format(INPUT_FOLDER, username)
                cv2.imwrite(path, frame)
                print(
                    "[INFO] frame saved: {}/{}.jpg".format(INPUT_FOLDER, username))
                time.sleep(5)
                break
            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

if __name__ == "__main__":
    VideoStream().stream('linh', 'qr')
