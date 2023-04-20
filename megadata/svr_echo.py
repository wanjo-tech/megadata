from mypy import tryx
import asyncio

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New client connected: {addr!r}")

    while True:
        data = await reader.read(1024) # lenth is important?
        if not data or len(data)<1:
            break
        message = tryx(data.decode) or message
        print(f"Received {message!r} from {addr!r}")
        writer.write(data)
        await writer.drain()

    print(f"Client {addr!r} disconnected")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

asyncio.run(main())