import json
from base64 import b64encode
from tokenize import PlainToken

# import the ChaCha20 Cipher
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

class EncrypCha:
    def __init__(self):
        pass
    
    def generate_random_bytes(self, key_size=32):
        return get_random_bytes(key_size)
    
    def generate_cipher(self):
        self.key=self.generate_random_bytes()
        return ChaCha20.new(key=self.key)
    
    def encry(self, text_string):
        cipher = self.generate_cipher()
        # cipher_text = cipher.encrypt(bytes(text_string, 'UTF-8'))
        cipher_text = cipher.encrypt(text_string)
        
        # cipher_text = cipher.encrypt(memoryview(bytearray(text_string, 'UTF-8')))
        nonce = b64encode(cipher.nonce).decode('utf-8')
        ct = b64encode(cipher_text).decode('utf-8')
        result = json.dumps({
            'nonce':nonce,
            'cipher_text':ct,
            'key': b64encode(self.key).decode('utf-8')
        })
        return result