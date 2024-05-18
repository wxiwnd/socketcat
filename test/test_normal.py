import asyncio, struct, os
import sys, pytest
sys.path.append("..")
from packet import HelloPacket, DataPacket
from utils import PacketUtils


# Build an invalid TRUST_ID
trustid = os.getenv("TRUST_ID")


@pytest.mark.asyncio
async def test_trustid_invalid():
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
        print(data_length)

        data_encrypt = await reader.read(data_length)
        data = PacketUtils.decrypt(trustid, data_encrypt)

    assert data == b'200' # Hello Successfully

    data = DataPacket(trustid, b'Hello, World!').pack()
    writer.write(data)
    await writer.drain()

