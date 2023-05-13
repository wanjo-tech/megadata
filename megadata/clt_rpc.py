from .mypy import *

def clt_ipc(argv):
  print('clt_rpc',argv)
  argc = len(argv)
  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('address=',address)


#>>> rpc(build_address(3388))('Adm','pingx')
#>>> asyncio.run(rpcx(build_address(3388))('Adm','pingx'))

