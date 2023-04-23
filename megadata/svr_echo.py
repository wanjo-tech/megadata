import asyncio
import socket

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New client connected: {addr!r}")
    while True:
        data = await reader.read(1024)
        if not data:break
        print(f"Received {data!r} from {addr!r}")
        writer.write(data)
        await writer.drain()

    print(f"Client {addr!r} disconnected")
    writer.close()

async def main():
    #loop = asyncio.get_running_loop()
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

async def start_named_pipe_server(pipe_name):
    if not pipe_name.startswith(r"\\.\\pipe\\"):
        pipe_name = r"\\.\\pipe\\" + pipe_name

    loop = asyncio.get_running_loop()
    #server = await loop.create_server(lambda: asyncio.StreamReaderProtocol(asyncio.StreamReader()), pipe_name)
    server = await loop.create_server(handle_echo, pipe_name, family=socket.AF_PIPE)
    async with server:
        await server.serve_forever()

from multiprocessing.connection import Listener
async def handle_pipe(conn):
    print('handle_pipe')
    while True:
        try:
            data = conn.recv()
            # 处理数据
            print(data)
            conn.send(data)
        except EOFError:
            break
from .mypy import tryx,try_asyncio,o2s,build_address
def handle_conn(conn,svr):
    print('handle_conn',svr)
    while True:
        try:
            data = conn.recv()
            # 处理数据
            print('data',data)
            conn.send(data)
        except EOFError:
            break
def main():
    address = build_address('wtf')
    print (address)
    listener = Listener(address, family='AF_PIPE')
    while True:
        # conn = listener.accept()
        # print('conn')
        # asyncio.create_task(handle_pipe(conn))
        conn = tryx(listener.accept)
        print('conn',conn)
        if conn is None: print('.')
        else: try_asyncio(lambda:handle_conn(conn,listener.last_accepted),new=True)

if __name__ == "__main__":
    #pipe_name = r"my_pipe"
    #asyncio.run(start_named_pipe_server(pipe_name))
    #asyncio.run(main())
    main()


"""
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
"""
