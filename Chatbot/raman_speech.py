#Humanoid RAMAN - 4i Lab IITG
#Import libraries
import os
import sys
import string
import tensorflow as tf
import speech_recognition as sr
from multiprocessing import Pool

r = sr.Recognizer()
r.energy_threshold = 3000
punct = '''()-[]{}'"\<>/@#$%^&*_~'''
punct_full = '''().,:!-[]{}'"\<>/@#$%^&*_~'''

audio = None

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
def our_function(x):
	global audio
	r.recognize(audio)

#Function to recognise the Speech
def recog():
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source, duration=0.5)
		print("Say Something!")
		output = r.listen(source)
		return output

def recog2():
	print('done')
	try:
		answer = pool.apply_async(our_function, [12])
		timer = answer.get(timeout = 10)
	except:
		print('error after exception')
		answer = "error"
	return(answer)

#Some hardcoded answers
def hardcoded(quest):
	if quest == 'who built you':
		return('I was built by Robotics Club I I T G')
	elif quest == 'do you have a girlfriend':
		return('Considering the girls to boys ratio, how do you expect me to have one!')
	elif quest == 'world domination':
		return('Yeah! Definitely!')
	elif quest == 'error':
		return(1)
	else:
		return(0)

def bot_ui():
	corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
	knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
	res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')
	with tf.Session() as sess:
		predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir, result_dir=res_dir, result_file='basic')
       		# This command UI has a single chat session only
		session_id = predictor.session_data.add_session()
		print("Welcome to Raman Speech Synthesis!")
		print("Type exit and press enter to end the conversation.")
		os.system("espeak 'Welcome USER'")
		# Waiting from standard input.
		sys.stdout.write("> ")
		sys.stdout.flush()
		global audio
		audio = recog()
		question = recog2()

		while question:
			if question.strip() == 'exit':
				print("Thank you for your presence. Goodbye.")
				os.system(espeak("Thank you for your presence. Goodbye."))
				break
			while hardcoded(question) == 1:
				print('> Can you repeat the question again!')
				os.system('espeak "Can you repeat the question again!"')
				audio = recog2()
				question = recog2()
			out = hardcoded(question)
			if not out:
				out = predictor.predict(session_id, question)
			#replacing Papaya with Raman
			if 'papaya' in unpunctuate(out, punct_full).lower().split():
				out = out.replace('Papaya', 'Raman')
			print(out)
			os.system(espeak(unpunctuate(out, punct)))
			print("> ", end="")
			sys.stdout.flush()
			audio = recog()
			question = recog2()


if __name__ == "__main__":
    bot_ui()
