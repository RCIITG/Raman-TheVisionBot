import numpy as np 
import serial
import cv2
import math
import subprocess 
import time 

cap = cv2.VideoCapture(1)

hue_min=0; hue_max=0; sat_min=0; sat_max=255; val_min=0; val_max=128
cap_region_x_begin=0.3 
cap_region_y_end=0.8 
blurValue = 21


channels = {'hue': None, 'saturation': None, 'value': None, 'laser': None}


cv2.namedWindow('image')
prev = 0

def nothing(x) :
    pass 
    
# cv2.createTrackbar('hue_min', 'image', 0, 255, nothing)
# cv2.createTrackbar('hue_max', 'image', 0, 255, nothing)
# cv2.createTrackbar('sat_min', 'image', 0, 255, nothing)
# cv2.createTrackbar('sat_max', 'image', 0, 255, nothing)
# cv2.createTrackbar('val_min', 'image', 0, 255, nothing)
# cv2.createTrackbar('val_max', 'image', 0, 255, nothing)


def calculateFingers(res,drawing): 
    
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):  # avoid crashing.   (BUG not found)

            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            return True, cnt
    return False, 0


def threshold_image(channel):
    if channel == "hue":
        minimum = hue_min
        maximum = hue_max
    elif channel == "saturation":
        minimum = sat_min
        maximum = sat_max
    elif channel == "value":
        minimum = val_min
        maximum = val_max

    (t, tmp) = cv2.threshold(channels[channel], maximum, 0, cv2.THRESH_TOZERO_INV)

    (t, channels[channel]) = cv2.threshold(tmp, minimum, 255, cv2.THRESH_BINARY)


    if channel == 'hue':
        # only works for filtering red color because the range for the hue is split
        channels['hue'] = cv2.bitwise_not(channels['hue'])
    
    return channels[channel]

while(True) :
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = cv2.bilateralFilter(frame, 5, 50, 100)

    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)
   
    # hue_min  = cv2.getTrackbarPos('hue_min', 'image')
    # hue_max = cv2.getTrackbarPos('hue_max', 'image')
    # sat_min  = cv2.getTrackbarPos('sat_min', 'image')
    # sat_max = cv2.getTrackbarPos('sat_max', 'image')
    # val_min = cv2.getTrackbarPos('val_min', 'image')
    # val_max = cv2.getTrackbarPos('val_max', 'image')

    channels['hue'] = h
    channels['saturation'] = s
    channels['value'] = v
    threshold_image("hue")
    threshold_image("saturation")
    threshold_image("value")

    channels['laser'] = cv2.bitwise_and(channels['hue'], channels['value'])
    channels['laser'] = cv2.bitwise_and(channels['saturation'],channels['laser'])
    cv2.imshow('frame', channels['laser'])
    img = channels['laser'][0:int(cap_region_y_end * frame.shape[0]),int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]
    
    blur = cv2.GaussianBlur(img, (blurValue, blurValue), 0)
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
    (_,cnts,_) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    if len(cnts) > 0 :
        c = max(cnts, key=cv2.contourArea)
  
        hull = cv2.convexHull(c)
        drawing = np.zeros([384,320,3], np.uint8)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)  
        cv2.drawContours(drawing, [c], 0, (0, 0, 255), 3) 
        cv2.imshow('image', drawing)   
        isFinishCal,cnt = calculateFingers(c,drawing)
        

        # if((cnt-prev) != 0) :
        if(cnt == 4) :
                subprocess.call(['echo', 'Gesture 5 detected'], shell=False)
                prev = cnt

        # if((cnt-prev) != 0) :
        if(cnt == 3) :
                subprocess.call(['echo', 'Gesture 4 detected'], shell=False)
                prev = cnt

        # if((cnt-prev) != 0) :
        if(cnt == 2) :
                subprocess.call(['echo', 'Gesture 3 detected'], shell=False)
                prev = cnt

        # if((cnt-prev) != 0) :
        if(cnt == 1) :
                subprocess.call(['echo', 'Gesture 2 detected'], shell=False)
                prev = cnt

        cv2.putText(img,'cnt',(10,250), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2,cv2.LINE_AA)
        print cnt+1
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break 

cap.release()
cv2.destroyAllWindows()
