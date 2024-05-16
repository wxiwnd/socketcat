import asyncio, struct, os

trustid = os.getenv("TRUST_ID")

async def handle_hello(reader, writer):
    addr = writer.get_extra_info('peername')

    flag = await reader.read(1)
    flag = struct.unpack("B", flag)[0]

    if (flag == 0x00):
        client_trustid_len = await reader.read(1)
        client_trustid_len = struct.unpack("B", client_trustid_len)[0]
        client_trustid = await reader.read(client_trustid_len)
        client_trustid = client_trustid.decode()

        if (client_trustid == trustid):
            print(f"Connection Established from {addr!r}")
            while True:
                if await handle_data(reader, writer) == -1: break
                

        else:
            print("Invalid TRUST_ID, Closing Connection...")


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

        data = await reader.read(data_length)
        
        print(f"Received Data: {data!r}")
    return 0


async def main():
    print("Socket Cat Server, version alpha_0001")
    print("All rights not reserved.")

    assert trustid, "TRUST_ID must be set and cannot be empty"    

    server = await asyncio.start_server(
        handle_hello, '127.0.0.1', 20049)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())