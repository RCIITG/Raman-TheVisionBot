
import numpy as np
import rospy
from std_msgs.msg import String
import cv2
from cv2 import aruco
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
params = aruco.DetectorParameters_create()
font = cv2.FONT_HERSHEY_COMPLEX
cap= cv2.VideoCapture(0)



def coordinate_publisher():
    pub = rospy.Publisher('coordinate_publisher', String, queue_size=10)
    rospy.init_node('coordinate_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters= params)
        detected = aruco.drawDetectedMarkers(frame, corners)
        # hello_str = get_coordinate()
        if np.all(ids != None):
            for i in range(len(ids)):
            	cv2.putText(detected, str(ids[i][0]),
	                            tuple((corners[i][0][0]+corners[i][0][2])/2),
	                            font, 0.5, (0, 250,0), 1, 4)
	        center_coordinate=(corners[i][0][0]+corners[i][0][2])/2
            rospy.loginfo(str(center_coordinate[0])+" "+str(center_coordinate[1]))
            msg_publish=str(center_coordinate[0])+" "+str(center_coordinate[1])
        else:
            rospy.loginfo("No detection")            
            msg_publish="No detection"
        
        pub.publish(msg_publish)
        rate.sleep()
        cv2.imshow("detection",frame)
        key=cv2.waitKey(1) & 0xFF
        if key==27:
	        cap.release()
	        cv2.destroyAllWindows()
	        break
       


if __name__ == '__main__':
    try:
        coordinate_publisher()
    except rospy.ROSInterruptException:
        pass

