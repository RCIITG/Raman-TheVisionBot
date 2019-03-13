def face_encode():
	import face_recognition, cv2, glob
	known_face_encodings = []
	known_face_names = []
	for img in glob.glob("images/*.jpg"):
		a_image = face_recognition.load_image_file(img)
		a_face_encoding = face_recognition.face_encodings(a_image)[0]
		name = img.replace('images/','')
		name = name.replace('.jpg','')
		known_face_encodings.append(a_face_encoding)
		known_face_names.append(name)
	return known_face_encodings, known_face_names