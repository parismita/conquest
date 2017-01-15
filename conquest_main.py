import numpy as np
import findGeometricStuff
import getThresholdValue
import locateResources
import cv2


##########################################################################################
#####################################---MAIN---###########################################


resMin , resMax = getThresoldValue()
##    tcMin , tcMax = getThresoldValue()
##    bfMin , bfMin = getThresoldValue()
##    bbMin , bbMin = getThresoldValue()

resources = locateResources(resMin , resMax)

    ###locating town center
cap = cv2.VideoCapture(0)
ret,frame = cap.read()
hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
mask = cv2.inRange(hsv,tcMin,tcMax)

tcCenter = findCentroid(mask)


##########################################################################################
##########################################################################################

