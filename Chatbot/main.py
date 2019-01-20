#Humanoid RAMAN - 4i Lab IITG
#Import libraries
import os
import sys
import tensorflow as tf
from playsound import playsound as ps

#Import files
import wake_word
import speech
from settings import PROJECT_ROOT
from botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#Triggers - not intended for commercial purposes
triggers = ['./triggers/hello_raman_linux.ppn']

#Hardcoded responses
'''Need to improve'''
def hardcoded(quest):
	'''Function to produce harcoded responses
	
	Loops through hardcoded questions and return corresponding responses

	parameter : quest - input question string
	returns : response
	return type : string
	'''
    if quest == 'who built you':
        return('I was built by Robotics Club I I T G')
    elif quest == 'do you have a girlfriend':
        return('Considering the girls to boys ratio, how do you expect me to have one!')
    elif quest == 'world domination':
        return('Yeah! Definitely!')
    else:
        return(0)

#Replace Papaya
def replace(input):
	'''Function to replace papaya keywords with Raman
	
	Replaces the "papaya" keyword in input text with Raman 

	parameter : input - response string
	returns : altered string
	return type : string
	'''
    if 'papaya' in speech.unpunct(input, "full").lower().split():
        input = input.replace('Papaya', 'Raman')
    return input

#Main program
def chat():
	'''Main function for Raman's Speech Subsystem

	Performs speech-to-text using Speech APIs. Returns programmed responses
	or provide responses using a pre-trained neural network. Performs text-to-speech
	using functions in speech module 
	'''
    corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
    knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
    res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')
    with tf.Session() as sess:
        predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir, result_dir=res_dir, result_file='basic')
       	#This command UI has a single chat session only
        session_id = predictor.session_data.add_session()
        print("Welcome to Raman Speech Synthesis!")
        print("Type exit and press enter to end the conversation.")
        speech.espeak('Welcome user')
        #speech.pspeak('Welcome user')
        #wait for tigger
        while True:
            detect = wake_word.trigger_detect(triggers)
            if detect:
                speech.espeak('Yes')
                #speech.pspeak('Yes')
                #Get input
                question = speech.recog_web()
                print('Input :', question)
                #Check if exit
                if question.strip() == 'exit':
                    print("Thank you for your presence. Goodbye.")
                    speech.espeak("Thank you for your presence. Goodbye")
                    #speech.pspeak("Thank you for your presence. Goodbye")
                    return 0
                #Ask again if error
                while (question == "error"):
                    print('> Can you repeat the question again!')
                    speech.espeak("Can you repeat the question again!")
                    #speech.pspeak("Can you repeat the question again!")
                    question = speech.recog_web()
                #If hardcoded, get output
                out = hardcoded(question)
                #Else, generate output
                if not out:
                    out = predictor.predict(session_id, question)
                #Replace name
                out = replace(out)
                #Provide output
                print("Output :", out)
                speech.espeak(out)
                #speech.pspeak(out)


#Run
if __name__ == '__main__':
    chat()
