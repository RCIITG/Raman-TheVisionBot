import frame
import numpy as np
encode = np.load('encodings.npy')
name = np.load('names.npy')
frame.face_loc(encode,name)