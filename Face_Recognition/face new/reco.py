import frame
import numpy as np
#load the encodings saved from running the code save_en
encode = np.load('encodings.npy')
name = np.load('names.npy')
#run the face reco for each frame
frame.face_loc(encode,name)