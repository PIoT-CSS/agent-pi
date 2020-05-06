"""
recognize_user_face.py module, task is to read .pickle file of a user,
and determine if the face is similar or not.
"""

import face_recognition
import argparse
import pickle
import cv2
import os

DETECTION_METHOD = "hog"
PICKLE_EXTENSION = ".pickle"
INPUT_FOLDER = "input"
JPG_EXTENSION = ".jpg"

class RecognizeUserFace:
    """
    A class to recognize a user's face with the corresponding encoding.
    """
    def read_pickle(self, user):
        """
        Reads pickle file and returns the contents.
        """
        pickle_file = user + PICKLE_EXTENSION
        data = pickle.loads(open(pickle_file, "rb").read())

        return data

    def encode_input_image(self, user):
        """
        Turns the input image to encoding
        """
        input_path = INPUT_FOLDER + os.path.sep + user + JPG_EXTENSION
        image = cv2.imread(input_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect the face boundaries and encode it.
        boxes = face_recognition.face_locations(rgb,
                model=DETECTION_METHOD)
        encodings = face_recognition.face_encodings(rgb, boxes)

        return encodings

    def match_input_with_pickle(self, pickle_data, input_encodings):
        """
        Match the input image with known encodings and returns true if there's a match
        """
        # Loop through encodings
        for encoding in input_encodings:
            # Checks if input matches.
            matches = face_recognition.compare_faces(pickle_data["encodings"],
                encoding)

            # Checks if we found a match
            if True in matches:
                return True

    def run(self, user):
        pickle_data = self.read_pickle(user)
        input_encodings = self.encode_input_image(user)
        print(self.match_input_with_pickle(pickle_data, input_encodings))
    
if __name__ == "__main__":
    RecognizeUserFace().run("alex")