import cv2,conquest_main
import numpy as np


#tast
#get frame size and obstracle and resources size
#find x=frame size/60



#how to make contours line show, how to make grid show





#make groups of size x
#plot the groups in a image to verify
#make algo a* on 60*60 squares
#find path 
#find centroid of the position got and connect them
#####error minimization function to make the curve smooth##########my not be needed


capture = cv2.VideoCapture(0)

while 1:
	img = capture.read()
	frame_size = img[1].shape
	#print frame_size


