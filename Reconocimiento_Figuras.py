# Python opencv OCR, ALPR, ANPR license plate recognize

# https://www.youtube.com/watch?v=mSOgAnHC8hE

import cv2
import numpy as np

cap= cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing) 
cv2.createTrackbar("L-S", "Trackbars", 68, 255, nothing) 
cv2.createTrackbar("L-V", "Trackbars", 154, 255, nothing) 
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing) 
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing) 
cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

while cap.isOpened():
    ret, im= cap.read()
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    
    lower_red = np.array([l_h,l_s,l_v])
    upper_red = np.array([u_h,u_s,u_v])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel)

    #res = cv2.bitwise_and(im, im, mask=mask)

    #erosion = cv2.erode(mask, kernel, iterations = 1)
    #dilation = cv2.dilate(mask, kernel, iterations = 1)
    
    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Contornos
    contours, ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] 

        if area > 400:
            cv2.drawContours(im, [approx], 0, (0,0,0), 5)

        elif len(approx) == 3:
            cv2.putText(im, "Triangle", (x,y), font, 1, (0,0,0))

        elif len(approx) == 4:
            cv2.putText(im, "Rectangle", (x,y), font, 1, (0,0,0))

        elif len(approx) == 4:
            cv2.putText(im, "Pentagon", (x,y), font, 1, (0,0,0))
        
        elif 6 < len(approx) < 15:
            cv2.putText(im, "Ellipse", (x,y), font, 1, (0,0,0))

        else:
            cv2.putText(im, "Circle", (x,y), font, 1, (0,0,0))
    
    cv2.imshow('Frame', im)
    cv2.imshow('mask', mask)
    cv2.imshow('kernel', kernel)

    #if ret == False:
    #   break

    cv2.imshow('imagen', im)

    if cv2.waitKey(1) == 27:
        break
    
cap.release()
cv2.destroyAllWindows

## Incluir deteccion de pulsacion de tecla

## Incluir trabajar en paralelo con open cv

