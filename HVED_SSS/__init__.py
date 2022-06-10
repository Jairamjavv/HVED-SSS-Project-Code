import os
from encryption import Encryption
from decryption import Decryption

enc = Encryption()
enc.do_encryption()

pri_k = open(os.path.join(os.getcwd(),"keys","private_key.txt"),'r')
pri_k = pri_k.read().split("-")
pri_k = (int(pri_k[0]), int(pri_k[1]))
dec = Decryption()
dec.do_decryption(pri_k)