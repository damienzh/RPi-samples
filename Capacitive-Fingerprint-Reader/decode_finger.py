import pickle
import numpy as np

with open('sample_finger_img.dat', 'rb') as finger:
	buf = pickle.load(finger)

buf_arr = np.asarray(buf, dtype=np.int16)
print (buf_arr)
buf_arr_hex = np.array([hex(x) for x in buf_arr])
img_data = buf_arr_hex[9:-2]
print (img_data.shape)
