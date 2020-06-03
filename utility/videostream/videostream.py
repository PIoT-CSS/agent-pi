"""
videostream.py module, it's job is to start the camera in a thread
allowing it to warm up.
"""
from __future__ import print_function
# from .webcamvideostream import WebcamVideoStream
# from .fps import FPS
from webcamvideostream import WebcamVideoStream
from fps import FPS
import argparse
import imutils
import cv2
import face_recognition
import os
import time
from qrdetection import QRDetection
from pyzbar import pyzbar

# construct the argument parse and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcode.csv",
                help="/videostream/barcode.csv")
args = vars(ap.parse_args())

# location for saving images
INPUT_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../facialrecognition/input'))
fps = FPS().start()


class VideoStream():
    """
    A class containing method to save picture captured by webcam.
    """

    def stream(self, username, purpose):
        """
        created a *threaded* video stream, allow the camera sensor to warmup,
        and start the FPS counter. Displays the webcam when needed, captures
        a picture and saves it.

        :param username: isername that's using the camera
        :type username: string
        """
        vs = WebcamVideoStream(src=0).start()
        # loop over some frames...this time using the threaded stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            rgb_frame = frame[:, :, ::-1]

            if purpose == "qrdetect":
                # Open CSV to save details from QR Code
                csv = open(args["output"], "w")
                found = set()
                barcodes = pyzbar.decode(frame)

                # Detect QR Code
                qr = QRDetection()
                box = qr.detect(frame)
                if box is not None:
                    cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
                    scan = qr.qr_read(frame, barcodes)

                cv2.imshow("Frame", frame)
                cv2.waitKey(0)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            elif purpose == "facialrecognition":
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
    VideoStream().stream('linh', 'qrdetect')
