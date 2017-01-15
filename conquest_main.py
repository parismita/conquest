import numpy as np
import cv2

##########################################################################################
##########################################################################################

def nothing(x):
    pass

##########################################################################################
########################---getThresholdValue---###########################################

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

##########################################################################################
##########################---detectContours---############################################

def detectContours(objMin,objMax):
    minCntArea = 20

    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    mask = cv2.inRange(hsv,objMin,objMax)

    (_, cntSet, _) = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cntSet:
        if (cv2.contourArea(cnt)<minCntArea):
            cntSet.remove(cnt)

    cv2.drawContours(mask,cntSet,-1,(0,255,0), 3)
    cv2.imshow('mask',mask)

    if cv2.waitKey(0) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()

    return (mask, cntSet)

##########################################################################################
##########################---findCentroid---##############################################

def findCentroid(cnt):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (np.array([cx,cy]))

##########################################################################################
##########################---locateResources---###########################################

def locateResources(resMin , resMaxin):
    mask, cntSet = detectContours(resMin , resMaxin)

    resList = []

    for cnt in cntSet:
        centroid = findCentroid(cnt)
        
        peri = cv2.arcLength(cnt, True)
        poly = cv2.approxPolyDP(cnt, 0.15 * peri, True)

        if len(poly)==4:
            resType = 'f'
            res = [centroid,resType]
            resList.append(res)
        elif len(poly)==3:
            resType = 'w'
            res = [centroid,resType]
            resList.append(res)

##########################################################################################
#####################################---MAIN---###########################################

def main():
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

if __name__ == '__main__':
    main()
