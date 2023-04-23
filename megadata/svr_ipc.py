#-*- coding: utf-8 -*-

if __name__ == '__main__':
  from svr_ipc_bin import my_main_ipc,on_quit,start_stdin
  #from mypy import *
  from mypy import hook_quit,build_address,try_async,try_asyncio,argc,argv
  #from megadata.svr_ipc_bin import my_main_ipc,on_quit,start_stdin

  hook_quit(on_quit)

  async_call = try_asyncio # 5.225,4.4727
  # trying since 20220925
  #async_call = try_async # 5.7353,4.76

  # NOTES:
  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('listening',address)
  async_call(lambda:my_main_ipc(address,mode='asyncio'))

  # e.g. python svr_ipc.py a1 . a2 .
  if argc>3:
    address2 = build_address(argv[3], argv[4] if argc>4 else None)
    print('listening',address2)
    async_call(lambda:my_main_ipc(address2))

  start_stdin()
