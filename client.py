import asyncio, struct, hashlib, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

trustid = os.getenv("TRUST_ID")

secret = hashlib.sha256(trustid.encode()).digest()
key = secret[:16]
iv = secret[16:]


async def main():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 20049)
    
    # Cipher Init

    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Build Hello Packet
    hello_flag = struct.pack("B", 0x00)
    
    # Encrypt TRUST_ID
    hello_trustid = cipher.encrypt(pad(trustid.encode(), AES.block_size))
    hello_trustid_len = struct.pack("B", len(hello_trustid))
    hello_packet = hello_flag + hello_trustid_len + hello_trustid


    # BUild Data Packet
    data_flag = struct.pack("B", 0x01)
    original_data = "HelloWorld"

    # Encrypt the Data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print(AES.block_size)
    data = cipher.encrypt(pad(original_data.encode(), AES.block_size))
    data_len = struct.pack("I", len(data))
    data_packet = data_flag + data_len + data


    writer.write(hello_packet)
    await writer.drain()

    writer.write(data_packet)
    await writer.drain()
    writer.write(data_packet)
    await writer.drain()
    writer.write(data_packet)
    await writer.drain()
    writer.write(data_packet)
    await writer.drain()

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(main())
