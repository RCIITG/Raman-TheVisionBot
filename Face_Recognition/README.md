The Face Tracking uses Kanade-Lucas-Tomasi algorithm to detect and track faces.
Face Detection is done by using Haar Cascades, which detects frontal faces.
Shi-Tomasi corner detection is used to give best corner points in the face.
Lucas-Kanade Optical FLow is used to track the corner points detected earlier.

Cons:
Doesn't work under Occlusion and Low Light.