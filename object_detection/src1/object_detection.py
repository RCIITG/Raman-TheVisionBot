#!/usr/bin/env python
#ROS node libs
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image 
from std_msgs.msg import Int16
from cv_bridge import CvBridge, CvBridgeError

#  Gen lib
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
import cv2
#from PIL import Image
from matplotlib import pyplot as plt
sys.path.append('..')
from utils import label_map_util

from utils import visualization_utils as vis_util
#ROS NODE
rospy.init_node('detector_node')
rospy.loginfo('  ## Starting ROS Tensorflow interface ##')

MODEL_NAME=os.path.dirname(os.path.realpath(__file__))+'/../include/ssd_mobilenet_v1_coco_11_06_2017'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(os.path.dirname(os.path.realpath(__file__))+'/../include/', 'mscoco_label_map.pbtxt')


# ## Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=90, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
# Definite input and output Tensors for detection_graph
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Each box represents a part of the image where a particular object was detected.
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represent how level of confidence for each of the objects.
# Score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
config = tf.ConfigProto()
config.log_device_placement = True
config.gpu_options.allow_growth = True
try:
  with detection_graph.as_default():
    sess=tf.Session(graph=detection_graph,config=config)
    rospy.loginfo('  ## Tensorflow session open: Starting inference... ##')
except ValueError:
  rospy.logerr('   ## Error when openning session. Please restart the node ##')
  rospy.logerr(ValueError)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)
def img_callback(image_msg):
  now=rospy.get_rostime()
  # Get image as np
  image_np = _cv_bridge.imgmsg_to_cv2(image_msg, "bgr8")
  image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
  (boxes, scores, classes, num) = sess.run(
  [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
  # Visualization of the results of a detection.
  vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)
  try:
    _img_publisher.publish(_cv_bridge.cv2_to_imgmsg(image_np, "bgr8"))
    rospy.loginfo("  Publishing inference at %s FPS", 1.0/float(rospy.Time.now().to_sec() -now.to_sec()))
    now =rospy.Time.now()
  except CvBridgeError as e:
    rospy.logerr(e)   

#matplotlib nbagg
#cap = cv2.VideoCapture(0)
#br=CvBridge()
#cap=rospy.Subscriber("/usb_cam/image_raw",Image,br.imgmsg_to_cv2);

# Define subscribers
subs_topic = '/cv_camera/image_raw'
try:
  subs_topic = rospy.get_param(rospy.get_name()+'/camera_topic')
except:
  rospy.logwarn(' ROS was unable to load parameter '+ rospy.resolve_name(rospy.get_name()+'/camera_topic'))
_sub=rospy.Subscriber( subs_topic , Image, img_callback, queue_size=1, buff_size=2**24)
# Define publishers
out_img_topic = '/image_objects_detect'
try:
  out_img_topic = rospy.get_param(rospy.get_name()+'/out_img_topic')
except:
  rospy.logwarn(' ROS was unable to load parameter '+ rospy.resolve_name(rospy.get_name()+'/out_img_topic'))
_img_publisher=rospy.Publisher( out_img_topic , Image, queue_size=0)
_cv_bridge=CvBridge()
now=rospy.Time.now()



""" while True:
      image_valid ,image_np = cap.read()
      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
      #image_np = load_image_into_numpy_array(image)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
      (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)
      cv2.imshow('image', image_np)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''OPENCV_WINDOW = "Raw Image window";
pub=rospy.Publisher("/edge_detector/raw_image", 1)
cv::namedWindow(OPENCV_WINDOW);
#rospy.init_node('imag_pub', anonymous=True)
#rate = rospy.Rate(0.5) # 1 Hz
out_image = bridge.cv2_to_imgmsg(img, "bgr8")
pub.Publisher(out_image)'''
cap.release()
cv2.destroyAllWindows()"""

rospy.spin()