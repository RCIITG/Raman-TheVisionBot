
import os
import sys
import string
import tensorflow as tf
import speech_recognition as sr

r = sr.Recognizer()
r.energy_threshold = 3000
punct = '''()-[]{}'"\<>/@#$%^&*_~'''
punct_full = '''().,:!-[]{}'"\<>/@#$%^&*_~'''

from settings import PROJECT_ROOT
from botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#Function to unpunctuate the text for espeak
def unpunctuate(text, punct_list):
	edit = ""
	for char in text:
		if char not in punct_list:
			edit = edit + char
	return edit

#Function to convert for espeak
def espeak(text):
	out = "'" + text + "'"
	out = "espeak " + out
	return out

#Function to recognise the Speech
def recog():
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source, duration=0.5)
		print("Say something!")
		audio = r.listen(source)
		print('done')
		return (r.recognize_google(audio))
		

def bot_ui():
	corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
	knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
	res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')
	with tf.Session() as sess:
		predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir, result_dir=res_dir, result_file='basic')
       		# This command UI has a single chat session only
		session_id = predictor.session_data.add_session()
		print("Welcome to Chat with ChatLearner!")
		print("Type exit and press enter to end the conversation.")
		# Waiting from standard input.
		sys.stdout.write("> ")
		sys.stdout.flush()
		question = recog()
		while question:
			if question.strip() == 'exit':
				print("Thank you for your presence. Goodbye.")
				os.system(espeak("Thank you for your presence. Goodbye."))
				break
			out = predictor.predict(session_id, question)
			#replacing Papaya with Raman
			#scheck = unpunctuate(out, punct_full).lower()
			if 'papaya' in unpunctuate(out, punct_full).lower().split():
				out = out.replace('Papaya', 'Raman')
			if question == 'who built you':
				out = 'I was built by Robotics Club I I T G'
			print(out)
			os.system(espeak(unpunctuate(out, punct)))
			print("> ", end="")
			sys.stdout.flush()
			question = recog()

if __name__ == "__main__":
    bot_ui()
