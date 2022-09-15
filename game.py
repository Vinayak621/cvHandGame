import math
import random
import time
import numpy as np
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
cap=cv2.VideoCapture(0)

# initial game circle values
cap.set(3, 1280)
cap.set(4, 720)
color=(0 , 0, 255)
counter=0
score=0
timeS=time.time()
totalTime=10



detector =HandDetector(detectionCon=0.8,maxHands=1)
#polynomial calculation for dist in cms
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62,  59,  57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coeff=np.polyfit(x, y, 2)
#game variables
cx, cy=250, 250

while True:
    success, img= cap.read()
    if time.time()-timeS<totalTime:
        hands = detector.findHands(img,draw=False)
        if hands:
        #0 says that only one hand is used
            lmList = hands[0]['lmList']
        #x and y and width and height of the hand
            x, y, w, h=hands[0]['bbox']
            x1, y1, z1 = lmList[5]
            x2, y2, z2 = lmList[17]

            dist = int(math.sqrt((y2-y1)**2+(x2-x1)**2))
            A, B, C = coeff
            distCM = A*dist**2+B*dist+C
            if(distCM<40):
                if x<cx<x+w and y<cy<y+h:
                    counter=1
                cvzone.putTextRect(img, f'{int(distCM)}cm', (x+5,y-10))
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,0),3)
        if counter:
            counter+=1
            color=(0, 255, 0)
            if counter==3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color=(0, 0, 255)
                score+=1
                counter=0

        cv2.circle(img,(cx,cy),30,color,cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (1,1,1), cv2.FILLED)

        cvzone.putTextRect(img, f'Time:{int(totalTime-(time.time()-timeS))}', (1000,75),scale=3,offset=20)
        cvzone.putTextRect(img, f'Score:{str(score).zfill(2)}', (90, 75), scale=3, offset=20)
    else:
        cvzone.putTextRect(img, f'Game Over', (400,400),scale=5,offset=30, thickness=7)
        cvzone.putTextRect(img, f'Game points:{score}', (450, 500), scale=3, offset=30, thickness=7)
        cvzone.putTextRect(img, 'Press r to restart', (460, 575), scale=2, offset=10, thickness=7)


    cv2.imshow("Image", img)
    key=cv2.waitKey(1)

    if key==ord('r'):
        timeS=time.time()
        score=0