import asyncio, struct, os
from packet import HelloPacket, DataPacket
from utils import PacketUtils

# Should use new socketcat class method but lazy to refactor(lack of time)
async def main(address="localhost", port=20049, trustid=os.getenv("TRUST_ID")):
    reader, writer = await asyncio.open_connection(
        address, port)
    
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


    data_packet = DataPacket(trustid, b'Hello,World!')
    datapack = data_packet.pack()
    
    writer.write(datapack)
    await writer.drain()
    print(f'Send data: {datapack!r}')
    writer.write(datapack)
    await writer.drain()
    print(f'Send data: {datapack!r}')
    writer.write(datapack)
    await writer.drain()
    print(f'Send data: {datapack!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

def connect(address, port, trust_id):
    asyncio.run(main(address, port, trust_id))

if __name__ == '__main__':
    asyncio.run(main())
