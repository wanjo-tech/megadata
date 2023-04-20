import sys
sys.path.append('..')

from mypy import *

port = argv[1]
host = argv[2] if argc>2 else '127.0.0.1'

#ipc_entry = (host,port)

ipc_entry = build_address(port,host)
print('ipc_entry',ipc_entry)

s = "/api('Adm','ping')"

async def main():
  rt = await ipc(ipc_entry,s)
  print('rt=',rt)
  return rt

asyncio_run(main())
