import cv2
import mediapipe as mp
import math
import time
import numpy as np
h=480
w=480
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
mod=mpHands.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1)
def handsFinder(image,draw=True):
    imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    results = mod.process(imageRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
    return image


def findPosition(img, handNo=0,draw=True):
    xList = []
    yList = []
    bbox = []
    lmList = []
    imageRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = mod.process(imageRGB)
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            #h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            xList.append(cx)
            yList.append(cy)
            lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList), max(yList)
        bbox = xmin, ymin, xmax, ymax
        if draw:
            cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
    return lmList