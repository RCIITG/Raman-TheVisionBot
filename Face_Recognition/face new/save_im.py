def save(Keywords):
	#Keywords = Keywords.split(".")
	if Keywords is Keywords:
		import face_recognition, cv2
		video_capture = cv2.VideoCapture(0)
		for i in range(1,5):
			print("Himanshu!!")
			ret, frame = video_capture.read()
			#if face not detected print face not detected
			try:
				image = face_recognition.face_encodings(frame)[0]
				cv2.imwrite(naam, frame)
				cv2.imshow('Video', frame)
			except:
				print("I can't see your face properly")
			naam = "images/" + Keywords + str(i) + ".jpg"
			

		#one more thing left to try to not run the loop over alredy saved images
		video_capture.release()
		cv2.destroyAllWindows()
		import save_en as s
		s.save()	
		