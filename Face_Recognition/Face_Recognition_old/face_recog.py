import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

# Use this to add new user's face
# ret,img = video_capture.read()
# cv2.imwrite('User.jpg', img)

User_image = face_recognition.load_image_file("User.jpg")
User_face_encoding = face_recognition.face_encodings(User_image)[0]

face_locations = []
face_encodings = []
face_names = []

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)

    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([User_face_encoding], face_encoding)
        name = "Unknown"

        if match[0]:
            name = "User"

        face_names.append(name)


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 3
        right *= 3
        bottom *= 3
        left *= 3

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 3, bottom - 3), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()