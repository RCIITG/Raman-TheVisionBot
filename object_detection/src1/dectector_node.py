#!/usr/bin/env python
import rospy
def detector_init():
	# Init the node
	rospy.init_node('detector_node')
	
	# Start the node and run it
	tensor = ros_tensorflow_obj()
	tensor.spin()
	
if __name__ == '__main__':
    detector_init()