"""
videostream.py module, it's job is to start the camera in a thread
allowing it to warm up.
"""
from __future__ import print_function
from .webcamvideostream import WebcamVideoStream
from .fps import FPS
import argparse
import imutils
import cv2
import face_recognition
import os
import time
# location for saving images
INPUT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../facialrecognition/input'))
fps = FPS().start()

class VideoStream():
    """
    A class containing method to save picture captured by webcam.

    Methods
    -------
    stream(self, username):
        created a *threaded* video stream, allow the camera sensor to warmup,
        and start the FPS counter. Displays the webcam when needed, captures
        a picture and saves it.
    """
   
    def stream(self, username):
        """
        created a *threaded* video stream, allow the camera sensor to warmup,
        and start the FPS counter. Displays the webcam when needed, captures
        a picture and saves it.
        """
        vs = WebcamVideoStream(src=0).start()
        # loop over some frames...this time using the threaded stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            rgb_frame = frame[:, :, ::-1]

            # Find all the faces in the current frame of video
           # face_locations = face_recognition.face_locations(rgb_frame)

            #for top, right, bottom, left in face_locations:
                # Draw a box around the face
             #   cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # check to see if the frame should be displayed to our screen
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                path = "{}/{}.jpg".format(INPUT_FOLDER, username)
                cv2.imwrite(path, frame) 
                print("[INFO] frame saved: {}/{}.jpg".format(INPUT_FOLDER, username))
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
    VideoStream().stream('linh')
