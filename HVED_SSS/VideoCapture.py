import cv2
import numpy as np
import glob2
import re
import base64
import os, shutil, random
from datetime import datetime


path1 = "frames"
path2 = "encodedFrames"
root_frames = os.path.join(os.getcwd(),path1)
root_encodedFrames = os.path.join(os.getcwd(),path2)
slot = 0
#Creating folders
try:
    os.mkdir(root_frames)
    os.mkdir(root_encodedFrames)
    os.mkdir(os.path.join(os.getcwd(),"keys"))
except OSError:
    print("Alert! Directory creation failed")
    
for r,d,f in os.walk(os.path.join(os.getcwd(),'frames')):
    j = len(d)
    break

cap = cv2.VideoCapture(slot) #default = 0 - For Laptop
count = 0

while(True):
    ret, frame = cap.read()
    filename_frames = os.path.join(root_frames,"folder{}".format(j+1))
    try:
        os.mkdir(filename_frames)
    except OSError:
        pass
    filename_frames_frame = os.path.join(filename_frames,"frame{}.jpg".format(count))
    # cv2.imwrite(os.path.join(filename_frames,"frame{}.jpg".format(count)), frame)
    cv2.imwrite(filename_frames_frame, frame)
    count += 1
    cv2.imshow('Capture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

#Code to Encode the image
filename_frames = os.path.join(root_frames,"folder{}".format(j+1))
files = glob2.glob(os.path.join(filename_frames,"*.jpg"))
files = sorted(files, key = lambda x : int(re.findall('\d+', x)[0]))

filename = os.path.join(root_encodedFrames,"encode{}.txt".format(j+1))
new_file = open(filename, 'wb+')

for f in files:
    f = open(f, 'rb')
    enc_str = base64.b64encode(f.read())
    new_file.write(enc_str)
    new_file.write(b'.')
new_file.close()
f.close()

# try:
#     shutil.rmtree(path1)
#     shutil.rmtree(path2)
# except OSError:
#     print("Alert! The directory can't be removed")