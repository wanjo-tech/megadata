print('python -m megadata ipc port host')

import sys

sys.path.insert(0,'..')
print('sys.path',sys.path)

from megadata.mypy import argv
from megadata.clt_ipc import clt_ipc

clt_ipc(argv)


########

#from megadata.mypy import *
#
#hook_quit(on_quit_default)
#
#port = argv[1]
##host = argv[2] if argc>2 else '127.0.0.1'
#host = argv[2] if argc>2 else None
#
##ipc_entry = (host,port)
#
#ipc_entry = build_address(port,host)
#print('ipc_entry',ipc_entry)
#
##s = "/ping"
#s = "/api('Adm','ping')"
#s = "/api('Adm','pingx')"
#s = "Adm.pingx"
#
#async def main():
#  #rt = ipc(ipc_entry,s)
#  rt = await ipcx(ipc_entry,s)
#  print('rt=',rt)
#  return rt
#
#asyncio_run(main())
