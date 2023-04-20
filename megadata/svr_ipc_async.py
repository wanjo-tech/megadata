# using asyncio to write a telnet server 

#######
from asyncio import start_server,run as asyncio_run,get_running_loop,wait_for

async def on_conn(reader, writer):
    addr = writer.get_extra_info('peername')
    print('on conn:',addr)
    #writer.write(b'ok\r\n')
    #await writer.drain()
    while True:
        writer.reset()
        try:
            data = await reader.read()
            #data = await wait_for(reader.read(), timeout=2)
        except Exception as e:
            print('wait_for',e)
            data = None
            #break
        if not data:
            print('data',data)
            continue
        message = data.decode()

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")

        writer.write(data)
        await writer.drain()

        print("Close the client socket")
    writer.close()

async def main():
    #loop = get_running_loop()
    #server = await loop.create_server(on_conn, '127.0.0.1', 8888)
    async with await start_server(
        on_conn,'127.0.0.1',3344
        ) as server:
        await server.serve_forever()

asyncio_run(main())