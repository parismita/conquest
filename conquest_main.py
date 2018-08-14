import numpy as np
import cv2
import math,sys     
import serial as ser
import time

##################################################################################################################################################
global Ki, Kd, Kp, last_time, integrat, prev_err
Ki=1
Kd=1
Kp=1
integrat=0
last_time=0
prev_err=0

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
    
    cap = cv2.VideoCapture(1)
    
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

    return (minValues,MaxValues,mask)

################################################################################################################################################

def locateObstacle(oMin , oMax):
    mask, cntSet = detectContours(oMin , oMax)
    return mask


################################################################################################################################################
def locateMap(mMin , mMax):
    peri_max=0
    mask, cntSet = detectContours(mMin , mMax)
    for cnt in cntSet:
        peri = cv2.arcLength(cnt, True)
        if(peri_max<peri):
            peri_max=peri
            cnt_max=cnt
    poly = cv2.approxPolyDP(cnt_max, 0.15 * peri_max, True)
    print poly,"poly"
    return poly

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
    if tcCenter == [-1,-1]:
        print "no tcCenter"
        dist = sys.maxint
    resCenter = res[0]
    dist = (resCenter[0]-tcCenter[0])**2 + (resCenter[0] - tcCenter[0])**2
    if res[1] == 1:
        dist = dist*2
    return (dist)

##################################################################################################################################################

def locateTC():
    cap = cv2.VideoCapture(1)
    ret,frame = cap.read()
    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    mask = cv2.inRange(hsv,tcMin,tcMax)

    tcCenter = findCentroid(mask)
    return tcCenter

##################################################################################################################################################

def detectContours(objMin,objMax):
    minCntArea = 50

    cap = cv2.VideoCapture(1)
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

def pid(error,integrat,last_time,prev_err,Ki = 1,Kp=1,Kd=1):
    integrat = integrat + error
    derivative = error - prev_err
    cur_time = time.time()
    output=error*Kp + (Kd*derivative/(cur_time-last_time)) + (Ki*integrat*(cur_time-last_time))
    last_time=cur_time
    prev_err=error
    return output,integrat,last_time,prev_err

#####################################################################################################################################################

def run(target) :
    cap = cv2.VideoCapture(1)
    integrat=0
    last_time=0
    prev_err=0
    while(True):
        ret,frame = cap.read()
        hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
        botCentre, error ,bothead = locateBot(hsv,target)
        output,integrat,last_time,prev_err = pid(error,integrat,last_time,prev_err)
        output1=str(bothead)+str(output)
        if(np.linalg.norm(botCentre - target) < 15):
            output1 = output1 + 'r'
            break
        reset_output_buffer()
        ser.write(output1)

######################################################################################################################################################

def locateBot(img,target):
    mask1 = cv2.inRange(img,bfMin,bfMax)
    mask2 = cv2.inRange(img,bbMin,bbMax)
    botFront = findCentroid(mask1)
    botBack = findCentroid(mask2)
    botCentre = botFront
    botCentre = np.add(botFront,botBack)/2
    d1 = np.linalg.norm(botFront - target)  
    d2 = np.linalg.norm(botBack - target)
    if(d1 < d2):
        error = findError(botCentre,botFront, target)
        return botCentre,error,'f'
    else:
        error = findError(botCentre,botBack, target)
        return botCentre,error,'b'

########################################################################################################################################################

def findError(botCentre,botFront,target):
    a = np.array([1,0])
    bot_drn = botFront - botCentre
    target_drn = target - botCentre
    cosine_angle1 = np.dot(bot_drn, a)/(np.linalg.norm(bot_drn)*np.linalg.norm(a))
    cosine_angle2 = np.dot(a, target_drn)/(np.linalg.norm(a)*np.linalg.norm(target_drn))
    angle1 = np.degrees(np.arccos(cosine_angle1))
    angle2 = np.degrees(np.arccos(cosine_angle2))
    angle_dif = angle1 - angle2
    return angle_dif

####################################################################################################################################################################

###locating town center

global tcMin, tcMax
tcMin , tcMax, _ = getThresoldValue('town')
global tcCenter
tcCenter=locateTC()
resMin , resMax, _ = getThresoldValue('resources')
ser.Serial('/dev/ttyACM0')

bfMin , bfMax,_ = getThresoldValue('bot front')
bbMin , bbMax ,_ = getThresoldValue('bot end')

resources = locateResources(resMin , resMax)

#print resources

###locating town center


    
############################################################################################
############################################################################################

