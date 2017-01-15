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

def findCentroid(cnt):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (np.array([cx,cy]))
