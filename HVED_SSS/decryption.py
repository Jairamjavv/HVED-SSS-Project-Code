import cv2
import os
import ast
import base64
from os.path import isfile, join
from decrypCha import DecrypCha
from PrimeNo.rsa import decrypt


class Decryption():
    def __init__(self):
        for r,d,f in os.walk(os.path.join(os.getcwd(),'frames')):
            self.j = len(d)
            break        
        save_path = "save{}".format(self.j)
        self.save_directory_path = os.path.join(os.getcwd(),save_path)
        try:
            os.mkdir(self.save_directory_path)
        except OSError:
            print("Alert! Directory creation failed")
    
    def do_decryption(self, pri_k):
        enc_key = open(os.path.join(os.getcwd(),"keys","chachaKey{}".format(self.j),"encryptedKey.txt"),'r')
        enc_key = ast.literal_eval(enc_key.read())
        
        # decrypt the key
        chacha_key = decrypt(pri_k,enc_key)
        
        cipher_text = open(os.path.join(os.getcwd(),"encrypted{}".format(self.j),"encrypted.txt"),"rb")
        nonce = open(os.path.join(os.getcwd(),"encrypted{}".format(self.j),"nonce.txt"),"rb")
        cipher_text = cipher_text.read()
        nonce = nonce.read()
        
        d = DecrypCha(cipher_text, nonce, chacha_key)
        encoded = d.decry()
        
        #Decoding
        encoded = encoded.split('.')[:-1]
        
        c = 0

        for i in encoded:
            f = './save{}/frame'.format(self.j)+str(c)+'.jpg'
            fh = open(f, 'wb')
            fh.write(base64.b64decode(i))
            c = c + 1
        fh.close()
        
        #code snippet to merge the frames obtained in the previous snippet
        def convert_frames_to_video(pathIn, pathout, fps):
            frame_arr = []
            files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
            files.sort(key = lambda x: int(x[5:-4]))
            for i in range(len(files)):
                filename = pathIn + files[i]
                img = cv2.imread(filename)
                height, width, layers = img.shape
                size = (width, height)
        #         print(filename)
                frame_arr.append(img)
            out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'XVID'), fps, size)

            for i in range(len(frame_arr)):
                out.write(frame_arr[i])
            out.release()
        
        # pathIn = os.path.join(os.getcwd,'save')
        pathIn = self.save_directory_path+"\\"
        pathOut = './video{}.avi'.format(self.j)
        convert_frames_to_video(pathIn, pathOut, 20.0)
        