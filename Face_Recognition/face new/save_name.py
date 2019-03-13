def save(Keywords):
	#Keywords = Keywords.split(".")
	if Keywords is "sure":
		import face_recognition, cv2
		import numpy as np
		import tables
		video_capture = cv2.VideoCapture(0)
		encode = tables.open_file('encodings.npy', mode='a')
		name = tables.open_file('names.py', mode='a')
		#encode = np.load('encodings.npy')
		#name = np.load('names.npy')
		print("HI!!")
		known_face_encodings = []
		known_face_names = []
		known_face_encodings.append(encode[0])
		known_face_names.append(name)
		for i in range(1,20):
			print("Himanshu!!")
			ret, frame = video_capture.read()
			#a_image = face_recognition.frame
			a_face_encoding = face_recognition.face_encodings(frame)
			naam = "Mark" + str(i)
			known_face_encodings.append(a_face_encoding)
			known_face_names.append(naam)
			cv2.imshow('Video', frame)
		np.save('encodings', known_face_encodings)
		np.save('names', known_face_names)
		video_capture.release()
		cv2.destroyAllWindows()