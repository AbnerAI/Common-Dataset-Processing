import cv2
import numpy as np
import os

def crop(img):
    kernel5 = np.ones((5,5), np.uint8)
    thresh = cv2.Canny(img, 0, 60)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel5)
    closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel5)
    contours, hierarchy = cv2.findContours(closing.astype(np.uint8),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(contour) for contour in contours]
    i = np.argmax(areas)
    x, y, w, h = cv2.boundingRect(contours[i])

    return img[y:y+h, x:x+w]