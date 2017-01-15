import numpy as np
import cv2

def nothing(x):
    pass

def getThresoldValue():
    cv2.namedWindow('Video')
    cv2.createTrackbar('hMax', 'Video', 179, 179,nothing)
    cv2.createTrackbar('hMin', 'Video', 0, 255,nothing)
    cv2.createTrackbar('sMax', 'Video', 254, 255,nothing)
    cv2.createTrackbar('sMin', 'Video', 0, 255,nothing)
    cv2.createTrackbar('vMax', 'Video', 254, 255,nothing)
    cv2.createTrackbar('vMin', 'Video', 0, 255,nothing)
    
    cap = cv2.VideoCapture(0)
    
    while (True):
        ret,frame = cap.read()
        hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        hMin = cv2.getTrackbarPos('hMin','Video')
        sMin = cv2.getTrackbarPos('sMin','Video')
        vMin = cv2.getTrackbarPos('vMin','Video')
        hMax = cv2.getTrackbarPos('hMax','Video')
        sMax = cv2.getTrackbarPos('sMax','Video')
        vMax = cv2.getTrackbarPos('vMax','Video')

        mask = cv2.inRange(hsv,(hMin,sMin,vMin),(hMax,sMax,vMax))
        cv2.imshow('Video',mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print ("Success")
            break

    minValues = np.array([hMin,sMin,vMin])
    MaxValues = np.array([hMax,sMax,vMax])

    return (minValues,MaxValues)
