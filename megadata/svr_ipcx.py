#-*- coding: utf-8 -*-


if __name__ == '__main__':
  from Application import build_address,argv,argc,try_async,hook_quit,sys
  from svr_ipc_bin import my_main,on_quit,start_stdin
  hook_quit(on_quit)
  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('listening',address)

  try_async(lambda:my_main(address,'ipcx'))
  start_stdin()
