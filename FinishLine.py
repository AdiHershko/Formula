import cv2
import client
import numpy as np

def DetectColor():
    pass


def detectLine(pixmap):
    pass


def detect_edges(frame):
    # filter for blue lane lines
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # show_image("hsv", hsv)
    lower_orange = np.array([223, 130, 67])
    upper_orange = np.array([161, 67, 5])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    # show_image("stop line", mask)

    edges = cv2.Canny(mask, 200, 400)

    return edges


def stop():
    client.run_action("stop")


if __name__ == '__main__':
    pass