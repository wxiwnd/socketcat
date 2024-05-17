import asyncio, struct, os
from packet import HelloPacket, DataPacket

trustid = os.getenv("TRUST_ID")

async def main():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 20049)
    
    hello_packet = HelloPacket(trustid)
    writer.write(hello_packet.pack())
    await writer.drain()

    data_packet = DataPacket(trustid, "Hello,World!")
    datapack = data_packet.pack()
    
    writer.write(datapack)
    await writer.drain()
    writer.write(datapack)
    await writer.drain()
    writer.write(datapack)
    await writer.drain()

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(main())
