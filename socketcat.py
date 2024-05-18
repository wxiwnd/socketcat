import asyncio, struct
from packet import DataPacket
from utils import PacketUtils

class SocketCatServer:
    def __init__(self, addr:str, port:int, trustid):
        self.reader = None
        self.writer = None
        self.trustid = trustid
        self.listen_addr:str = addr
        self.listen_port:int = port
 
    def start(self):
        asyncio.run(self.__create_server())

    async def read_and_unpack(self):
        flag = await self.reader.read(1)
        if not flag: return -1
        flag = struct.unpack("B", flag)[0]
        
        if (flag == 0x00):  # 0x00 for HelloPacket
            client_trustid_len = await self.reader.read(1)
            client_trustid_len = struct.unpack("B", client_trustid_len)[0]

            client_trustid = await self.reader.read(client_trustid_len)
            client_trustid = PacketUtils.decrypt(self.trustid, client_trustid)

            if (client_trustid != None):
                client_trustid = client_trustid.decode() 

            return client_trustid # return trustid in str, not bytes

        elif (flag == 0x01):    # 0x01 for DataPacket
            data_length = await self.reader.read(4)
            data_length = struct.unpack("I", data_length)[0]

            data_encrypt = await self.reader.read(data_length)
            data = PacketUtils.decrypt(self.trustid, data_encrypt)

            return data # return data as bytes
        
        else:
            print("Malformed Packet, Closing Connection...")
            return None

    
    
    async def __create_server(self):
        server = await asyncio.start_server(self.__handle_stream, self.listen_addr, self.listen_port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()
    
    async def __handle_stream(self, reader, writer):
        self.reader = reader
        self.writer = writer
        await self.__handle_hello()
    
    async def __handle_hello(self):
        addr = self.writer.get_extra_info('peername')
        client_trustid = await self.read_and_unpack()
        
        if (client_trustid == self.trustid):
            response = DataPacket(self.trustid, b'200').pack()
            self.writer.write(response)
            await self.writer.drain()

            print(f"Connection Established from {addr!r}")
            while True:
                if await self._handle_data() == -1: break # Auth complete, start listen data loop

        else:
            print("Invalid TRUST_ID, Closing Connection...")
            response = DataPacket(self.trustid, b'403').pack()
            self.writer.write(response)
            await self.writer.drain()

        print(f"Connection to {addr!r} Closed")    
        self.writer.close()
        await self.writer.wait_closed() 
            
    
    
    async def _handle_data(self):
        data = await self.read_and_unpack()
        if (data == -1): return data
        
        print(f"Received Data: {data!r}")
        
        return 0







