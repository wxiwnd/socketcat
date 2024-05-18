import hashlib, struct
import abc

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad



class Packet(abc.ABC):
    def __init__(self, trustid, data=None):
        secret = hashlib.sha256(trustid.encode()).digest()
        self.trustid = trustid
        self.key = secret[:16]
        self.iv = secret[16:]
        self.original_data = data
    
    @abc.abstractmethod
    def pack():
        pass




class HelloPacket(Packet):
    def pack(self):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        hello_flag = struct.pack("B", 0x00) # 0x00 for hello packet
        hello_trustid = cipher.encrypt(pad(self.trustid.encode(), AES.block_size))
        hello_trustid_len = struct.pack("B", len(hello_trustid))

        hello_packet = hello_flag + hello_trustid_len + hello_trustid

        return hello_packet

class DataPacket(Packet):
    def pack(self):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        data_flag = struct.pack("B", 0x01)  # 0x01 for data packet
        data = cipher.encrypt(pad(self.original_data, AES.block_size))
        data_len = struct.pack("I", len(data))
        data_packet = data_flag + data_len + data

        return data_packet