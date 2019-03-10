#Humanoid RAMAN - 4i Lab IITG
#Import libraries
import speech_recognition as sr
import os
import cloud_speech
import pyttsx3

#Import cloud speech library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account

#Credentials file
credentials = service_account.Credentials.from_service_account_file('/home/otoshuki/Projects/raman.json')
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=""

#Create recognizer instance
rec = sr.Recognizer()

RATE = 16000
CHUNK = int(RATE / 10)
enging = pyttsx3.init()

#Recognition using Google Web
def recog_web():
	'''Function to perform speech-to-text conversion
	
	Uses Google Web Speech API to perform speech-to-text. PyAudio used for
	audio streaming.

	returns : text converted from input speech
	return type : string
	'''
	try:
        #Get the input
		with sr.Microphone() as source:
			rec.adjust_for_ambient_noise(source, duration=0.5)
			print("Say")
			audio = rec.listen(source, timeout = 3.0)
			print('Heard')
			answer = rec.recognize_google(audio)
			rec.operation_timeout = 5
    #If no input
	except:
		answer = 'error'
	return answer

#Recognition using Google Cloud
def recog_cloud():
	'''Function to perform speech-to-text conversion
	
	Uses Google Cloud Speech API to perform speech-to-text. PyAudio used for
	audio streaming. Iterates through server responses

	returns : 		responses : stream_recognize object
					out :		text converted from input speech
	return type : 	responses :	object
					out :		string
	'''
	language_code = 'en-US'
	client = speech.SpeechClient(credentials=credentials)
	config = types.RecognitionConfig(
		encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
	streaming_config = types.StreamingRecognitionConfig(config=config,
		interim_results=True)
	print("Say")
	with cloud_speech.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()
		requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)
		print('Requests')
		responses = client.streaming_recognize(streaming_config, requests)
		print('Speak')
        # Now, put the transcription responses to use.
		out = cloud_speech.listen_print_loop(responses)
	return responses, out



def espeak(text):
	'''Function to perform text-to-speech conversion
	
	Uses Linux's espeak command to produce the audio output from text

	parameter : text - the string for text-to-speech conversion
	returns : string of text in espeak command format
	return type : string
	'''
	out = "'" + text + "'"
	out = "espeak " + out
	os.system(out)
	return out

def pspeak(text,voice = None,rate = 110,volume = 0.7):
	'''Function to perform text-to-speech conversion
	
	Uses pyttsx3 library to produce the audio output from text

	parameter : text 	- the string for text-to-speech conversion
				voice 	- speech synthesizer voice id
				rate 	- intgers speech rate in wpm
				volume 	- floating point in the range 0.0 to 1.0 inclusive
	'''
	engine.setProperty('rate', rate)
	engine.setProperty('volume', volume)
	if voice != None:
		engine.setProperty('voice', voice)
	engine.say(text)
	engine.runAndWait()

def listVoices():
	'''Function to provide list of voices available for pyttsx3
	
	returns : list of ids of voices available
	'''
	ids = []
	voices = engine.getProperty('voices')
	for voice in voices:
		print("Voice ID :",voice.id)
		print("Age :", voice.age, "Gender :", voice.gender)
		ids.append(voice.id)
	return ids

def unpunct(text, punct_type):
	'''Function to unpunctuate input text to be used with espeak
	
	Loops through the text and adds alpha-numeric characters to edit string

	parameter : text - the string to unpunctuate
				punct_type - "half" or "full" strings for different punctuation lists
	returns : unpunctuated string
	return type : string
	'''
	edit = ""
	if punct_type == "half":
		punct = '''()-[]{}'"\<>/@#$%^&*_~'''
	elif punct_type == "full":
		punct = '''().,:!-[]{}'"\<>/@#$%^&*_~'''
	for char in text:
		if char not in punct:
			edit = edit + char
	return edit

if __name__ == "__main__":
	listVoices()
