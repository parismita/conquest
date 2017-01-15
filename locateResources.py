import findGeometricStuff,numpy,cv2


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
