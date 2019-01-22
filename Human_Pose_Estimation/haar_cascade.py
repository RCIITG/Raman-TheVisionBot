import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)
while(True):
	ret,img=cap.read()
	face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
	    cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	    
	cv.imshow('img',img)
	if cv.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv.destroyAllWindows()
