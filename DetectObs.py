import cv2
import sys
import numpy as np
import random
from enum import Enum

MIN_SIZE=100


class Side(Enum):
    LEFT = 0
    RIGHT = 1


def snap(data, i):
    nparr = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    name = f'{random.random()}.jpg'
    cv2.imwrite(f'C:\\images\\{name}', image)


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


def find_obs(image, lower, upper, name):
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    cv2.imshow(f'images-{name}', np.hstack([image, output]))
    cv2.imshow(f'gray-{name}', np.hstack([gray]))
    cv2.imshow(f'blur-{name}', np.hstack([blur]))
    cv2.waitKey()
    ret, im = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    draw(contours, image, name)
    return find_max_contour(contours)


def draw(contours, image, name):
    if len(contours) == 0 or contours is None:
        return
    i=0
    for c in contours:
        # Obtain bounding rectangle to get measurements
        x, y, w, h = cv2.boundingRect(c)

        # Crop and save ROI
        ROI = image[y:y + h, x:x + w]
        cv2.imwrite(f'C:\\images\\cons\\{name}_{i}.png', ROI)
        i=i+1


def detect_obst(image):
    # nparr = np.frombuffer(data, dtype=np.uint8)
    # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height, width = image.shape[:2]
    boundaries = [
        ([110, 0, 130], [233, 118, 255], 'purple'),  # purple
        ([176, 0, 135], [255, 135, 228], 'pink'), # pink
        ([83, 112, 15], [220, 250, 150], 'green'), # green
        # ([103, 86, 65], [145, 133, 128])
    ]
    countors=[]
    # loop over the boundaries
    for (lower, upper, name) in boundaries:
        countors.append(find_obs(image, lower, upper, name))
    max_con = find_max_contour(countors)
    return max_con



img = cv2.imread('C:\\images\\purple.jpg', cv2.IMREAD_COLOR)
img = img[170:,:]
cv2.imshow("cut", np.hstack([img]))
# cv2.waitKey()
detect(img)
