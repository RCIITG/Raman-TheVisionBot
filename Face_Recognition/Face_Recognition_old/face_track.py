'''
To-Do
-Documentation
-Add bounding box to the second face based on tha keypoints of p0_0 and p0_1
 
 Normalise pixel values using histogram distribution and use SIFT for face recognition
 Normalise->SIFT->Keypoints
 Color Swaps-look at YOLO
'''
import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
cap=cv2.VideoCapture(0)

ret,img = cap.read()
cv2.imwrite('sample.jpg', img)
old_frame=cv2.imread('sample.jpg')
gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for(x,y,w,h) in faces:
    old_frame = cv2.rectangle(old_frame,(x,y),(x+w,y+h),(255,0,0),2)
    
cv2.imshow('img',old_frame)
cv2.waitKey(0)


# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 200,
                       qualityLevel = 0.03,
                       minDistance = 0.005,
                       blockSize = 10 )               #tune param

# optical flow using Lucas-Kanade
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


if len(faces)==1:
    faces_x=faces[0][0]
    faces_y=faces[0][1]
    faces_w=faces[0][2]
    faces_h=faces[0][3]
    #face_1 is the image of extracted face
    all_faces=old_frame[faces_y:faces_y+faces_h, faces_x:faces_x+faces_w]
    cv2.imshow('face',all_faces)
    cv2.waitKey(0)
    all_faces_gray = cv2.cvtColor(all_faces, cv2.COLOR_BGR2GRAY)
    # Take first frame and find corners in it
    p0 = cv2.goodFeaturesToTrack(all_faces_gray, mask = None, **feature_params)
    p0 = p0+np.array([[faces_x,faces_y]], dtype=np.float32)
elif len(faces)==2:
    faces_x1=faces[0][0]
    faces_y1=faces[0][1]
    faces_w1=faces[0][2]
    faces_h1=faces[0][3]
    #face_1 is the image of extracted face
    face_1=old_frame[faces_y1:faces_y1+faces_h1, faces_x1:faces_x1+faces_w1]
    cv2.imshow('face1',face_1)
    cv2.waitKey(0)
    face_1_gray = cv2.cvtColor(face_1, cv2.COLOR_BGR2GRAY)
    p0_0 = cv2.goodFeaturesToTrack(face_1_gray, mask = None, **feature_params)
    p0_0 = p0_0+np.array([[faces_x1,faces_y1]], dtype=np.float32)
    
    faces_x2=faces[1][0]
    faces_y2=faces[1][1]
    faces_w2=faces[1][2]
    faces_h2=faces[1][3]
    #face_1 is the image of extracted face
    face_2=old_frame[faces_y2:faces_y2+faces_h2, faces_x2:faces_x2+faces_w2]
    cv2.imshow('face2',face_2)
    cv2.waitKey(0)
    face_2_gray = cv2.cvtColor(face_2, cv2.COLOR_BGR2GRAY)
    p0_1 = cv2.goodFeaturesToTrack(face_2_gray, mask = None, **feature_params)
    p0_1 = p0_1+np.array([[faces_x2,faces_y2]], dtype=np.float32)

    p0=np.concatenate((np.array(p0_0),np.array(p0_1)),axis=0)
    
#---------------------------------------------------------------------------
# Combine two images
if len(faces) is 2:
    img1=face_1
    img2=face_2


    h1, w1 = np.shape(img1)[0],np.shape(img1)[1]
    h2, w2 = np.shape(img2)[0],np.shape(img2)[1]

    vis = np.zeros((max(h1, h2), w1+w2),np.uint8)
    
    img1_gray=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2_gray=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    
    for i in range(h1):
        for j in range(w1):
            vis[i][j]=img1_gray[i][j]
    for i in range(h2):
            for j in range(w1,w1+w2):
                vis[i][j]=img2_gray[i][j-w1]

    cv2.imshow('test', vis)
    cv2.waitKey(0)
    all_faces=vis
    faces_w=all_faces.shape[1]
    faces_h=all_faces.shape[0]
    
#---------------------------------------------------------------------------


# Create some random colors
color = np.random.randint(0,255,(200,3))


#old_frame   -  prev frame
#old_gray    -  old frame grayscale
#face_i       -  face_i image
#face_i_gray  -  face_i grayscale
#p0          -  coordinates of interest points in face_i image (not in old_frame)  
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

mask = np.zeros_like(old_frame)

while(1):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    # good_new = p1
    # good_old = p0
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        
        # mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
      	frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        # frame = cv2.circle(frame,(a,b),5,(255,0,0),-1)
    img = cv2.add(frame,mask)
    rect_x = np.mean(p0.reshape(p0.shape[0],-1)[:,0])-faces_w/2
    rect_y = np.mean(p0.reshape(p0.shape[0],-1)[:,1])-faces_h/2
    cv2.rectangle(img, ((int)(rect_x), (int)(rect_y)), ((int)(rect_x+faces_w), (int)(rect_y+faces_h)), (0, 255, 0), 2)

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()

