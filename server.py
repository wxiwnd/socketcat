import asyncio, struct, hashlib, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

trustid = os.getenv("TRUST_ID")

secret = hashlib.sha256(trustid.encode()).digest()
key = secret[:16]
iv = secret[16:]

async def handle_hello(reader, writer):
    addr = writer.get_extra_info('peername')
    cipher = AES.new(key, AES.MODE_CBC, iv)

    flag = await reader.read(1)
    flag = struct.unpack("B", flag)[0]

    if (flag == 0x00):
        client_trustid_len = await reader.read(1)
        client_trustid_len = struct.unpack("B", client_trustid_len)[0]
        client_trustid = await reader.read(client_trustid_len)
        client_trustid = unpad(cipher.decrypt(
            client_trustid), AES.block_size).decode()
        

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
    cipher = AES.new(key, AES.MODE_CBC, iv)

    flag = await reader.read(1)
    if not flag:
        return -1
    flag = struct.unpack("B", flag)[0]
    if (flag == 0x01):
        data_length = await reader.read(4)
        data_length = struct.unpack("I", data_length)[0]
        print(data_length)

        data_encrypt = await reader.read(data_length)
        data = unpad(cipher.decrypt(
            data_encrypt), AES.block_size).decode()
        print(f"Received Data: {data!r}")
    return 0


async def main():
    print("SocketCat Server, version beta_0001")
    print("All rights not reserved.")

    assert trustid, "TRUST_ID must be set and cannot be empty"    

    server = await asyncio.start_server(
        handle_hello, '0.0.0.0', 20049)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())