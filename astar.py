import cv2,conquest_main
import numpy as np


#tast
#get frame size and obstracle and resources size
#find x=frame size/60



#how to make contours line show, how to make grid show
def listPathPoints1(start,end):
    stx=start[0]
    sty=start[1]
    enx=end[0]
    eny=end[1]
    l=[]
    vx=(enx-stx)
    vy=(eny-sty)
    if (vx==0 and vy==0):
        return start
    d=int(math.sqrt((stx-enx)**2+(sty-eny)**2))
    cos=vx/math.sqrt(vx**2+vy**2)
    sin=vy/math.sqrt(vx**2+vy**2)
    i=1
    while(i<d):
        l.append([int(stx+cos*i),int(sty+sin*i)])
        i=i+1
    return l




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


