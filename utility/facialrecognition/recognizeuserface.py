"""
recognize_user_face.py module, task is to read .pickle file of a user,
and determine if the face is similar or not.
"""

import face_recognition
import argparse
import pickle
import cv2
import os

DETECTION_METHOD = "hog" # Always hog, raspberry pi is too weak to run cnn.

PICKLE_EXTENSION = ".pickle"

INPUT_FOLDER = "./utility/facialrecognition/input"

PICKLE_FOLDER = "./utility/facialrecognition/pickle"

JPG_EXTENSION = ".jpg"

class RecognizeUserFace:
   
    """
    A class to recognize a user's face with the corresponding encoding.
    """
    def read_pickle(self, user):
        """
        Reads pickle file and returns the contents.

        :param user: user that's being encoded
        :type user: string
        :return: data
        :rtype: list
        """
        pickle_file = PICKLE_FOLDER + os.path.sep + user + PICKLE_EXTENSION
        print("Using " + pickle_file + " as the data")
        f = open(pickle_file, "rb").read()
        data = pickle.loads(f)
        return data

    def encode_input_image(self, user):
        """
        Turns the input image to encoding

        :param user: user that's being encoded
        :type user: string
        :return: encodings
        :rtype: list
        """
        input_path = INPUT_FOLDER + os.path.sep + user + JPG_EXTENSION
        print("Using " + input_path + " as input")
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

        :param pickle_data: face encodings from pickle file
        :type pickle_data: list
        :param input_encodings: input face encodings
        :type input_encodings: list
        :return: boolean
        :rtype: boolean
        """
        # Loop through encodings
        for input_encoding in input_encodings:
            # Checks if input matches.
            matches = face_recognition.compare_faces(pickle_data["encodings"],
                input_encoding, tolerance=0.45) # Change tolerance. this needs further testing.

            # Checks if we found a match
            if True in matches:
                return True
            else:
                return False

    def run(self, user):
        """
        Gets pickle, input, and determines if it matches.

        :param user: user that's being encoded
        :type user: string
        :return: boolean
        :rtype: boolean
        """
        pickle_data = self.read_pickle(user)
        input_encodings = self.encode_input_image(user)
        retVal = self.match_input_with_pickle(pickle_data, input_encodings)
        print("face matched: ", retVal)
        return retVal

if __name__ == "__main__":
    RecognizeUserFace().run('linh')
