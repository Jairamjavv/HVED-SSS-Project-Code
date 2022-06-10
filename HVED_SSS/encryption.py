from fileinput import filename
import os
import json
from datetime import datetime
from PrimeNo.generate_primes import generate_primes
from PrimeNo.rsa import generate_keypair, encrypt, decrypt
from encryCha import EncrypCha

class Encryption():
    def __init__(self):
        path1 = "frames"
        path2 = "encodedFrames"
        for r,d,f in os.walk(os.path.join(os.getcwd(),'frames')):
            self.j = len(d)
            break
        self.root_frames = os.path.join(os.getcwd(),path1)
        self.root_encodedFrames = os.path.join(os.getcwd(),path2)
        self.filename = os.path.join(self.root_encodedFrames,"encode{}.txt".format(self.j))
    
    def makeDirs(self, dirList):
        for i in dirList:
            try:
                os.mkdir(os.path.join(os.getcwd(),i))
            except OSError:
                print("Alert! Directory creation failed")
                
    def do_encryption(self):
        # Code to generate Prime Numbers
        p = generate_primes(n=16)[0]
        q = generate_primes(n=16)[0]     
        
        #Code to Encrypt
        key = os.urandom(16)
        
        self.makeDirs(["encrypted{}".format(self.j),os.path.join("keys","keys{}".format(self.j)),os.path.join("keys","chachaKey{}".format(self.j))])
        
        file_in = open(self.filename,'rb')
        enc_file = open(os.path.join(os.getcwd(),"encrypted{}".format(self.j),"encrypted.txt"),'wb')
        nonce_file = open(os.path.join(os.getcwd(),"encrypted{}".format(self.j),"nonce.txt"),'wb')
        
        e = EncrypCha()
        json_object = e.encry(file_in.read())
        enc_file.write(json.loads(json_object)["cipher_text"].encode())
        nonce_file.write(json.loads(json_object)["nonce"].encode())
        key = json.loads(json_object)["key"]
        
        #Generating Private and Public Key
        public_key, private_key = generate_keypair(p, q)
        pub_k = open(os.path.join(os.getcwd(),"keys","keys{}".format(self.j),"public_key.txt"),'w')
        pri_k = open(os.path.join(os.getcwd(),"keys","keys{}".format(self.j),"private_key.txt"),'w')
        pub_k.write(str(public_key[0]))
        pri_k.write(str(private_key[0])+"-")
        pri_k.write(str(private_key[1]))
        pub_k.close()
        pri_k.close()
        
        chacha_encrypted_key = str(encrypt(public_key, key))

        cke = open(os.path.join(os.getcwd(),"keys","chachaKey{}".format(self.j),"encryptedKey.txt"),'w')
        cke.write(chacha_encrypted_key)
        cke.close()
        file_in.close()
        enc_file.close()
        
        return private_key