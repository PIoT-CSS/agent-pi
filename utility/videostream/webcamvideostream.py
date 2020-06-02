from threading import Thread
import cv2

class WebcamVideoStream:
    """
    A class that contains methods to manage the webcam.
    """
    def __init__(self, src=0):
        """
        initialize the video camera stream and read the first frame
        from the stream
        """
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        """
        starts the thread
        """
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        """
        runs a loop to update the frame stored. stops if stopped is true
        """
        while True:
            if self.stopped:
                return
            
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """
        return the frame stored by update.
        """
        return self.frame
    
    def stop(self):
        """
        stop the webcam
        """
        self.stopped = True
