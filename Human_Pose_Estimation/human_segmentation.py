
import pyrealsense2 as rs
import numpy as np
import numpy as np
import cv2

# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 2 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

x,y,w,h=1,0,0,0

# Streaming loop
try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)
        #print np.size(aligned_frames)
        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        #type(aligned_depth_frame.get_data())
        color_frame = aligned_frames.get_color_frame()

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.array(aligned_depth_frame.get_data())
        img = np.array(color_frame.get_data())
        #print np.shape(img)
        #print np.shape(depth_image)
        #print np.shape(color_frame)
        #print np.shape(aligned_depth_frame)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            #print x,y, w, h
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            continue

        #print "afetr loop"
        print x,y
        #x=x+h/2
        #y=y+w/2


        cv2.imshow('img',img)


        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        hsv = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)
        #pixel=depth_colormap[x,y]
        # print x,y
        pixel2=hsv[y,x]
        #print np.shape(hsv)

 	# Remove background - Set pixels further than clipping_distance to grey
        grey_color = 0
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels

        hsv_h_3d = np.dstack((hsv[:,:,0],hsv[:,:,0],hsv[:,:,0]))
        hsv_s_3d = np.dstack((hsv[:,:,1],hsv[:,:,1],hsv[:,:,1]))
        hsv_v_3d = np.dstack((hsv[:,:,2],hsv[:,:,2],hsv[:,:,2]))
        bg_removed = np.where((hsv_v_3d>(pixel2[2]+7)) | (hsv_v_3d<(pixel2[2]-7)) |(hsv_h_3d<(pixel2[0]-7)) |(hsv_h_3d>(pixel2[0]+7))|(hsv_s_3d<(pixel2[1]-7)) |(hsv_s_3d>(pixel2[1]+7))|(depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, img)

        images = np.hstack((bg_removed, depth_colormap))
        cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
	pipeline.stop()
	cv2.destroyAllWindows()
