import struct, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class PacketUtils:
    @staticmethod
    def decrypt(trustid, data):
        secret = hashlib.sha256(trustid.encode()).digest()
        key = secret[:16]
        iv = secret[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        try:
            return unpad(cipher.decrypt(data), AES.block_size)
        except:
            print("Decrypt Failed")
        return None