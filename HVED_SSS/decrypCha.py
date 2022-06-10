import json
from base64 import b64decode
from tokenize import PlainToken

# import the ChaCha20 Cipher
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

class DecrypCha:    
    def __init__(self, cipher_text, nonce, key):
        try:
            # self.b64 = json.loads(json_data)
            # self.nonce = b64decode(self.b64['nonce'])
            # self.cipher_text = b64decode(self.b64['cipher_text'])
            # self.key = b64decode(self.b64['key'])
            self.nonce = b64decode(nonce)
            self.cipher_text = b64decode(cipher_text)
            self.key = b64decode(key)
        except(ValueError, KeyError):
            print("Incorrect Decryption")
            
    def decry(self):
        try:
            cipher = ChaCha20.new(key=self.key, nonce=self.nonce)
            plaintxt = cipher.decrypt(self.cipher_text)   
            return plaintxt.decode()
        except(ValueError, KeyError):
            print("Incorrect Decryption")         