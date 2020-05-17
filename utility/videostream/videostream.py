from __future__ import print_function
from .webcamvideostream import WebcamVideoStream
from .fps import FPS
import argparse
import imutils
import cv2
import face_recognition

# location for saving images
INPUT_FOLDER = "../facialrecognition/input"
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
class VideoStream():
   
    def stream(self, username):
        # loop over some frames...this time using the threaded stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            rgb_frame = frame[:, :, ::-1]

            # Find all the faces in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)

            for top, right, bottom, left in face_locations:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # check to see if the frame should be displayed to our screen
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite("{}/{}.jpg".format(INPUT_FOLDER, username), frame) 
                print("[INFO] frame saved: {}/{}.jpg".format(INPUT_FOLDER, username))
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
