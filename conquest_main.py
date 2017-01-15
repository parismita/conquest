import numpy as np
import cv2


##########################################################################################
#####################################---MAIN---###########################################

resMin , resMax = getThresoldValue()
tcMin , tcMax = getThresoldValue()
bfMin , bfMin = getThresoldValue()
bbMin , bbMin = getThresoldValue()

resources = locateResources(resMin , resMax)

###locating town center
cap = cv2.VideoCapture(0)
ret,frame = cap.read()

##########################################################################################
##########################################################################################
