import asyncio, struct, os

trustid = os.getenv("TRUST_ID")

async def main():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 20049)

    hello_flag = struct.pack("B", 0x00)
    hello_trustid_len = struct.pack("B", len(trustid))
    hello_packet = hello_flag + hello_trustid_len + trustid.encode()


    data_flag = struct.pack("B", 0x01)
    data = "HelloWorld"
    data_len = struct.pack("I", len(data))
    data_packet = data_flag + data_len + data.encode()

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
