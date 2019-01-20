#Humanoid RAMAN - 4i Lab IITG
#Import libraries
import os
import struct
import sys
import pyaudio

#Add python library to system path
sys.path.append(os.path.join(os.path.dirname(__file__), '../Porcupine/binding/python'))
from porcupine import Porcupine

#Set machine type
machine = 'x86_64'
library_path = os.path.join(os.path.dirname(__file__), '../Porcupine/lib/linux/%s/libpv_porcupine.so' % machine)
model_file_path = os.path.join(os.path.dirname(__file__), '../Porcupine/lib/common/porcupine_params.pv')
sensitivity = 0.5
sample_rate = 0

def trigger_detect(keyword_paths):
	'''Function to detect trigger words
	
	Takes trigger words list as argument. Uses PyAudio for audio streaming.
	Uses Porcupine library to detect the trigger.
	
	Parameters : keyword_paths - a list of keyword paths
	returns : the index of keyword detected
    return type : int
	'''
    if len(keyword_paths) == 1:
        keyword_path = keyword_paths[0]
    else:
        sensitivities = [0.5 for i in range(len(keyword_paths))]
    porcupine = None
    pa = None
    audio_stream = None
    record = []
    done = 0
    try:
        if len(keyword_paths) == 1:
            porcupine = Porcupine(
                library_path = library_path,
                model_file_path =  model_file_path,
                keyword_file_path = keyword_path,
                sensitivity = sensitivity)
        else:
            porcupine = Porcupine(
                library_path = library_path,
                model_file_path =  model_file_path,
                keyword_file_paths = keyword_paths,
                sensitivities = sensitivities)

        pa = pyaudio.PyAudio()
        global sample_rate
        sample_rate = porcupine.sample_rate
        audio_stream = pa.open(
            rate = porcupine.sample_rate,
            channels = 1,
            format = pyaudio.paInt16,
            input = True,
            frames_per_buffer = porcupine.frame_length,
            input_device_index = None)
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            record.append(pcm)
            if len(keyword_paths) == 1:
                if result:
                    print("Keyword Detected")
                    return result
            else:
                if result >= 0:
                    print("Keyword Detected")
                    return result

    except KeyboardInterrupt:
            print('stopping ...')
    finally:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()


if __name__ == '__main__':
    recorded = trigger_detect()
