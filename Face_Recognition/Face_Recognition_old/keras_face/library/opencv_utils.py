import numpy as np
import cv2
import os

def detect_face_from_img_path(frontal_face_model_file_path, image_path):
    if not os.path.exists(frontal_face_model_file_path):
        print('failed to find face detection opencv model: ', frontal_face_model_file_path)

    face_cascade = cv2.CascadeClassifier(frontal_face_model_file_path)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    print('faces detected: ', len(faces))
    indx = 0
    for (x, y, w, h) in faces:
        detected_face = img[y:y+h, x:x+w]
        cv2.imwrite("face_"+str(indx)+"_"+image_path[image_path.rfind('/')+1:], detected_face)
        cv2.imshow('img', detected_face)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        indx = indx + 1

def main():
    frontal_face_model_file_path = '../../demo/opencv-files/haarcascade_frontalface_alt.xml'

    detect_face_from_img_path(
        frontal_face_model_file_path,
        '../../demo/data/opencv-images/Guining.jpg')

    detect_face_from_img_path(
        frontal_face_model_file_path,
        '../../demo/data/opencv-images/Guining_Test.jpg')


if __name__ == '__main__':
    main()
