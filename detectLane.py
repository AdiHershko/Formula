import cv2
import numpy as np

MIN_SIZE=1000


def detect_line(image):
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 110, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow('thresh', thresh)
    # Find contours
    ROI_number = 0
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        # Obtain bounding rectangle to get measurements
        x, y, w, h = cv2.boundingRect(c)

        # # Find centroid
        # M = cv2.moments(c)
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])

        # Crop and save ROI
        ROI = original[y:y + h, x:x + w]
        # cv2.imwrite('C:\\images\\cons\\BLACK_{}.png'.format(ROI_number), ROI)
        ROI_number += 1

        # Draw the contour and center of the shape on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 4)
        # cv2.circle(image, (cX, cY), 10, (320, 159, 22), -1)

    # cv2.imwrite('image.png', image)
    # cv2.imwrite('thresh.png', thresh)
    # cv2.waitKey()
    return find_max_contour(cnts)


def find_max_contour(contours):
    if len(contours) == 0 or contours is None:
        return None
    maxContour = contours[0]
    maxSize = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w * h > maxSize:
            maxContour = c
            maxSize = w * h
    if maxSize < MIN_SIZE:
        return None
    return maxContour


# img = cv2.imread('C:\\images\\black.jpg')
# img = img[170:,:]
# # cv2.imshow("cut", np.hstack([img]))
# contour = detect_line(img)
# cv2.waitKey()
