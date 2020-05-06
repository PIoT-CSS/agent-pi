"""
encode_one.py module, task is to encode images of a particular user.
it will get images from the dataset and finds the specific folder
that corresponds to the user.
"""

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

DETECTION_METHOD = "hog" # Raspberry pi can only run hog due to hardware constraints.

DATASET_FOLDER = "dataset" # Folder name containing user images separated by folders.

PICKLE_EXTENSION = ".pickle"

class EncodeOne:
    """
    A class to encode images of a user.
    """
    def get_images_list_from_a_user(self, user):
        """
        Returns image list from a particular user dataset
        """
        images_path = DATASET_FOLDER + os.path.sep + user
        imagePaths = list(paths.list_images(images_path))

        return imagePaths

    def create_encodings_from_list(self, images_list):
        """
        Loops through a user images list and returns an encoding array
        which will be serialized to a .pickle file.
        """

        for(i, imagePath) in enumerate(images_list):
            print("[INFO] processing image {}/{}".format(i + 1, 
                len(images_list)))
            
            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb,
                model=DETECTION_METHOD)
            
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            return encodings

    def turn_encodings_to_pickle(self, encodings, user):
        """
        Create a .pickle file from encodings
        """
        filename = user + PICKLE_EXTENSION
        data = {"encodings": encodings, "names": user}
        f = open(filename, "wb")
        f.write(pickle.dumps(data))
        f.close()

    def run(self, user):
        """
        Init and runs Encode
        """
        images_list = self.get_images_list_from_a_user(user)
        encodings = self.create_encodings_from_list(images_list)
        self.turn_encodings_to_pickle(encodings, user)

if __name__ == "__main__":
    EncodeOne().run("alex")

