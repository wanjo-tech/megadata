#-*- coding: utf-8 -*-


if __name__ == '__main__':
  from .mypy import *
  from .svr_ipc_bin import my_main_ipc,get_builtins_default
  from .myeval import start_stdin
  hook_quit()
  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('listening',address)

  try_async(lambda:my_main_ipc(address,svr_mode='ipcm',mode='pool'))
  start_stdin(get_builtins_default)
