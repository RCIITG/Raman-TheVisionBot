## Face Detection and Tracking

The Face Tracking uses Kanade-Lucas-Tomasi algorithm to detect and track faces.
Face Detection is done by using Haar Cascades, which detects frontal faces.
Shi-Tomasi corner detection is used to give best corner points in the face.
Lucas-Kanade Optical FLow is used to track the corner points detected earlier.

## Face Recognition

Face Recognition task was performed using through the Keras implementation of DeepFace and VGG16 + Siamese