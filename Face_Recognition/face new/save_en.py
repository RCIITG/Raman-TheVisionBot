import encoding as en
import numpy as np
[encode,name] = en.face_encode()
np.save('encodings', encode)
np.save('names', name)