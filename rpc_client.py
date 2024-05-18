import asyncio, struct, os
import json
from packet import HelloPacket, DataPacket
from utils import PacketUtils

trustid = os.getenv("TRUST_ID")

async def main():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 20049)
    
    hello_packet = HelloPacket(trustid)
    writer.write(hello_packet.pack())
    await writer.drain()

    # Wait for response
    flag = await reader.read(1)
    flag = struct.unpack("B", flag)[0]
    if (flag == 0x01):
        data_length = await reader.read(4)
        data_length = struct.unpack("I", data_length)[0]
        data_encrypt = await reader.read(data_length)
        data = PacketUtils.decrypt(trustid, data_encrypt)

        print(f'Receive: {data!r}')

        if (data == b'403'):
            print("Forbidden")

    query_data = {"func_name" : 'TestFunction', 'func_args' : ['arg1', 2] , 'func_kwargs' : {'test' : 't'}}
    query_json = json.dumps(query_data)
    data_packet = DataPacket(trustid, query_json.encode())
    datapack = data_packet.pack()

    writer.write(datapack)
    await writer.drain()
    print(f'Send data: {datapack!r}')
    flag = await reader.read(1)
    flag = struct.unpack("B", flag)[0]
    if (flag == 0x01):
        data_length = await reader.read(4)
        data_length = struct.unpack("I", data_length)[0]
        data_encrypt = await reader.read(data_length)
        data = PacketUtils.decrypt(trustid, data_encrypt)

        print(f'Receive: {data!r}')

asyncio.run(main())