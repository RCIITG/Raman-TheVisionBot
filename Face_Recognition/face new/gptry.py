def face_loc(known_face_encodings, known_face_names):
	import face_recognition, cv2, json
	import serial
	import struct
	video_capture = cv2.VideoCapture(2)
	face_locations = []
	face_encodings = []
	face_names = []
	ard = serial.Serial('/dev/ttyACM0', 9600)
	process_this_frame = True
	#To set the frame rate
	video_capture.set(3,510)
	video_capture.set(4,510)
	video_capture.set(5,45)

	while True:
		ret, frame = video_capture.read()
		small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
		rgb_small_frame = small_frame[:, :, ::-1]

		if process_this_frame:
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
			face_names = []
			for face_encoding in face_encodings:
				matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance = 0.47)
				name = "Unknown_to_me"
				if True in matches:
					first_match_index = matches.index(True)
					name = known_face_names[first_match_index]
					#To remove the image index of a person like name1 = name
					name = filter(lambda x: x.isalpha(), name)

				face_names.append(name)
				
		process_this_frame = not process_this_frame
		loc = open("loc.txt","w+")
		'''loc.write("")
		loc = open("loc.txt","a+")'''
		Feat = {
		"loc": [],
		"name": [],
		"area": []
		}

		for (top, right, bottom, left), name in zip(face_locations, face_names):
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

			area = abs((top - bottom)*(left - right))
			location = int((right+ left)/4)
			if location > 254:
				location = 254
			print(location)
			#location = str(location)
			#location = location.replace('L','')
			'''loc.write(location)
			loc.write(" " + name + ",")'''
			Feat["loc"].append(location)
			Feat["name"].append(name)
			Feat["area"].append(area)

			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
			cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
			center_x = (left+right)/2
			
		i=0
		for x, (t, r, b, l) in zip(Feat["area"], face_locations):
		 	if x == max(Feat["area"]):
		 		mapped = mapper(center_x, 0, frame.shape[1], 0, 254)
		 		print(frame.shape)
		 		ard.write(struct.pack('>B', 254-mapped))
		 	i = i + 1

		with loc as text:
			text.write(json.dumps(Feat))
		loc.close()
		cv2.imshow('Video', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	video_capture.release()
	cv2.destroyAllWindows()

def mapper(val, min1, max1, min2, max2):
	span1 = max1 - min1
	span2 = max2 - min2
	new = min2 + (val - min1)*(span2/span1)
	return new