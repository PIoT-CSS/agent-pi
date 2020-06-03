import numpy as np
import cv2
import imutils

"""
QRDetection.py module, its functionality is involved in detecting the Engineers employee credentials to verify and record the individual has performed maintenance on the vehicle.

"""


class QRDetection:
    """
    A class to read QR Codes
    """

    def detect(self, image, barcodes):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # compute the Scharr gradient magnitude representation of the images
        # in both the x and y direction using OpenCV 2.4
        if imutils.is_cv2():
            ddepth = cv2.cv.CV_32F
        else:
            ddepth = cv2.CV_32F

        gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

        # subtract the y-gradient from the x-gradient
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)

        # blur and threshold the image
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

        # construct a closing kernel and apply it to the thresholded image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # perform a series of erosions and dilations
        closed = cv2.erode(closed, None, iterations=4)
        closed = cv2.dilate(closed, None, iterations=4)

        # find the contours in the thresholded image
        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # if no contours were found, return None
        if len(cnts) == 0:
            return None

        # otherwise, sort the contours by area and compute the rotated
        # bounding box of the largest contour
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        rect = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(
            rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)

        # return the bounding box of the barcode
        return box

    def read_qr(self, image, barcodes):
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)

            if barcodeData not in found:
                csv.write("{},{}\n".format(datetime.datetime.now(),
                                           barcodeData))
                csv.flush()
                found.add(barcodeData)

            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(
                barcodeType, barcodeData))
