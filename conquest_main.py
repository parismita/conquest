import numpy as np
import cv2
import math,sys

##################################################################################################################################################

def nothing(x):
    pass

##################################################################################################################################################

def getThresoldValue(name):
    cv2.namedWindow(name)
    cv2.createTrackbar('hMax', name, 179, 179,nothing)
    cv2.createTrackbar('hMin', name, 0, 255,nothing)
    cv2.createTrackbar('sMax', name, 254, 255,nothing)
    cv2.createTrackbar('sMin', name, 0, 255,nothing)
    cv2.createTrackbar('vMax', name, 254, 255,nothing)
    cv2.createTrackbar('vMin', name, 0, 255,nothing)
    
    cap = cv2.VideoCapture(0)
    
    while (True):
        ret,frame = cap.read()
        hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        hMin = cv2.getTrackbarPos('hMin',name)
        sMin = cv2.getTrackbarPos('sMin',name)
        vMin = cv2.getTrackbarPos('vMin',name)
        hMax = cv2.getTrackbarPos('hMax',name)
        sMax = cv2.getTrackbarPos('sMax',name)
        vMax = cv2.getTrackbarPos('vMax',name)

        mask = cv2.inRange(hsv,(hMin,sMin,vMin),(hMax,sMax,vMax))
        cv2.imshow(name,mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print ("Success")
            break

    minValues = np.array([hMin,sMin,vMin])
    MaxValues = np.array([hMax,sMax,vMax])

    return (minValues,MaxValues)
################################################################################################################################################
def locateObstacle(oMin , oMax):
    mask, cntSet = detectContours(oMin , oMax)

    oCen = []

    for cnt in cntSet:
        centroid = findCentroid(cnt)
        
        peri = cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, 0.15 * peri, True)
        o = [centroid]
        oCen.append(o)

    return oCen

##################################################################################################################################################

def locateResources(resMin , resMax):
    mask, cntSet = detectContours(resMin , resMax)

    resList = []

    for cnt in cntSet:
        centroid = findCentroid(cnt)
        
        peri = cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, 0.15 * peri, True)

        if len(poly)==4:
            resType = 1
            res = [centroid,resType]
            resList.append(res)
        elif len(poly)==3:
            resType = 2
            res = [centroid,resType]
            resList.append(res)

    lis = sorted(resList, key = distFromTC)
    return lis
            
##################################################################################################################################################

def distFromTC(res):
    tcCenter = locateTC()
    if tcCenter[0] == -1:
        print "no tcCenter"
        dist = sys.maxint
    resCenter = res[0]
    dist = ((resCenter[0]-tcCenter[0])**2 + (resCenter[0] - tcCenter[0])**2)**0.5
    return (dist*2)

##################################################################################################################################################

def locateTC():
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    mask = cv2.inRange(hsv,tcMin,tcMax)

    tcCenter = findCentroid(mask)
    return tcCenter

##################################################################################################################################################

def detectContours(objMin,objMax):
    minCntArea = 50

    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    mask = cv2.inRange(hsv,objMin,objMax)

    (mask, cntSet, _) = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in cntSet:
        if (cv2.contourArea(cnt)<minCntArea):
            cntSet = np.delete(cntSet,cnt)


    cv2.drawContours(mask,cntSet,-1,(255,255,255), 1)
    cv2.imshow('mask',mask)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

    return (mask, cntSet)

##################################################################################################################################################

def findCentroid(cnt):
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        #if centroid found
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    else:
        #assuming no centroid
        cx = -1
        cy = -1
    return (np.array([cx,cy]))

##################################################################################################################################################

resMin , resMax = getThresoldValue('resources')
global tcMin, tcMax
tcMin , tcMax = getThresoldValue('town')
##    bfMin , bfMin = getThresoldValue()
##    bbMin , bbMin = getThresoldValue()

resources = locateResources(resMin , resMax)
#print resources

###locating town center



############################################################################################
############################################################################################


