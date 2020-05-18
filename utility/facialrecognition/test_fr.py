import pytest
import pickle
import os
import numpy as np

from encode_one import EncodeOne
from recognizeuserface import RecognizeUserFace

encode = EncodeOne()
fr = RecognizeUserFace()

### Variables for testing EncodeOne ###
alexImagesPath = encode.get_images_list_from_a_user('alex')
alexEncodings = encode.create_encodings_from_list(alexImagesPath)

imagesPathInvalidFace = encode.get_images_list_from_a_user('object')
notFaceEncodings = encode.create_encodings_from_list(imagesPathInvalidFace)

linhImagesPath = encode.get_images_list_from_a_user('linh')
linhEncodings = encode.create_encodings_from_list(linhImagesPath)

### Variables for testing RecognizeUserFace ###

alexPickleData = fr.read_pickle('alex')
linhPickleData = fr.read_pickle('linh')

alexInputEncodings = fr.encode_input_image('alex')
linhPickleData = fr.encode_input_image('linh')

### Begin test for EncodeOne ###

def test_encode_images_path():
    # Test if the path is correct based on user parameter.

    assert 'dataset/alex/alex.jpg' in alexImagesPath
    assert 'dataset/linh/linh.jpg' in linhImagesPath

def test_encoding_valid_face():
    # Test if encodings is created from a valid face.

    # If not empty that means a face was recognized
    assert len(alexEncodings) != 0 
    assert len(linhEncodings) != 0

def test_encoding_invalid_face():
    # This is path to an image that's not a proper face.

    # Test that it would not encode it because no face is found.
    assert len(notFaceEncodings) == 0

def test_two_encodings_is_different():
    # These two encodings should be different because we have different face.

    assert np.array_equal(alexEncodings[0], linhEncodings[0]) == False

def test_encoding_to_pickle():
    # Create pickle file alex.pickle in pickle folder.
    encode.run('alex')

    # Read pickle using recognizeuserface function.
    pickleData = fr.read_pickle('alex')

    # If pickle is succesfully created, pickleData and data should be equal.
    assert np.array_equal(alexEncodings[0], pickleData["encodings"][0])

### Begin test for RecognizeUserFace ###

def test_valid_match():
    match = fr.run('alex')

    # Should be True, run basically matches alex.pickle and alex.jpg as input.
    assert match

def test_invalid_match():
    # Try matching linh.pickle with alex.jpg should return False.
    match = fr.match_input_with_pickle(linhPickleData, alexInputEncodings)

    # Should not match.
    assert match == False