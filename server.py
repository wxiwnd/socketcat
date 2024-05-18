import asyncio, struct, hashlib, os
from packet import DataPacket
from utils import PacketUtils

trustid = os.getenv("TRUST_ID")

async def handle_hello(reader, writer):
    addr = writer.get_extra_info('peername')

    flag = await reader.read(1)
    flag = struct.unpack("B", flag)[0]

    if (flag == 0x00):
        client_trustid_len = await reader.read(1)
        client_trustid_len = struct.unpack("B", client_trustid_len)[0]
        client_trustid = await reader.read(client_trustid_len)

        client_trustid = PacketUtils.decrypt(trustid, client_trustid).decode()

        if (client_trustid == trustid):
            response = DataPacket(trustid, b'200').pack()
            writer.write(response)
            await writer.drain()

            print(f"Connection Established from {addr!r}")
            while True:
                if await handle_data(reader, writer) == -1: break

        else:
            print("Invalid TRUST_ID, Closing Connection...")
            response = DataPacket(trustid, b'403').pack()
            writer.write(response)
            await writer.drain()
    else:
        print("Malformed Hello Packet, Closing Connection...")
    
    print(f"Connection to {addr!r} Closed")    
    writer.close()
    await writer.wait_closed()  
    

async def handle_data(reader, writer):
    flag = await reader.read(1)
    if not flag:
        return -1
    flag = struct.unpack("B", flag)[0]
    if (flag == 0x01):
        data_length = await reader.read(4)
        data_length = struct.unpack("I", data_length)[0]

        data_encrypt = await reader.read(data_length)

        data = PacketUtils.decrypt(trustid, data_encrypt)

        print(f"Received Data: {data!r}")
    return 0


async def main():
    print("SocketCat Server, version v0.0.1")
    print("All rights not reserved.")

    assert trustid, "TRUST_ID must be set and cannot be empty"    

    server = await asyncio.start_server(
        handle_hello, '0.0.0.0', 20049)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nExiting Gracefully...")