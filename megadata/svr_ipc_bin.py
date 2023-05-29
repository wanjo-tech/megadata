#-*- coding: utf-8 -*-

# server ipc mode (return str or json-str only)

# TODO merge logic with svr_ipcm.py => svr_ipc_bin.py [ipc/ipcm]

from .mypy import *
from .myeval import myeval,myevalasync,fwdapi

white_list = tryx(lambda:load('../tmp/white_list.json'))
black_list = tryx(lambda:load('../tmp/black_list.json')) or []

get_builtins_default = lambda:{
  #'type':type,# directly exposing type is dangerous ;)
  'type':lambda v:str(type(v)), # safer
  'api':fwdapi,
  'ping':now(),
  'print':print,
}

def handle_ipc(param):
    conn,client,get_builtins = param

    # NOTES: client could be None when it came from local...
    assert client is None or len(client)==0 or (white_list is None) or (white_list and client[0] in white_list), f'banned {client}'

    while True:
      data = tryx(conn.recv,lambda ex:(log1('#'),flush1()))
      if data is None:
        tryx(conn.close)
        break

      rt = tryx(lambda:myeval(data,{"__builtins__":get_builtins()},{}),True)

      # rt_eval = tryx(lambda:myeval(data,{"__builtins__":get_builtins()},{}),True)
      # if type(rt_eval) in [list,tuple,dict]:
      #   rt = o2s(rt_eval)
      #   #print('debug rt_eval',data,type(rt_eval),type(rt),rt)
      #   if rt is None or "null"==rt: rt = rt_eval
      # else: rt = rt_eval
      # #print('debug rt_eval',data,type(rt_eval),type(rt),rt)

      if type(rt) not in [str,bytes]:
        rt = tryx(lambda:o2b(rt),True)

      conn.send(rt)

"""
ipc svr as example and quick usage only
mode: thread | asyncio | pool
svr_mode: ipc | ipcm
"""
def my_main_ipc(address,svr_mode='ipc',authkey=None,mode='pool',pool_size=None,get_builtins=get_builtins_default,debug=False):

  print('my_main_ipc()','svr_mode=',svr_mode,'mode=',mode)

  from multiprocessing.connection import Listener
  server = Listener(address=address,authkey=authkey)

  if 'thread'==mode:
    while True:
      conn = tryx(server.accept)
      if conn is None: print('.')
      else: try_async(lambda:handle_ipc((conn,server.last_accepted,get_builtins)))

  elif 'asyncio'==mode:
    while True:
      conn = tryx(server.accept)
      if conn is None: print('.')
      else:
        #print('server.last_accepted',server.last_accepted)
        try_asyncio(lambda:handle_ipc((conn,server.last_accepted,get_builtins)),new=True)

  else:# 'pool' mode

    if svr_mode=='ipcm':# multiprocess-mode
      from multiprocessing import Pool
    else: # multithread-mode
      from multiprocessing.dummy import Pool

    with Pool(os.cpu_count()) as pool:
      while True:
        conn = tryx(server.accept)
        if conn is None: print('.')
        else: pool.map_async(handle_ipc, [(conn,server.last_accepted,get_builtins)])


# quick test on main
if __name__ == '__main__':
  hook_quit()

  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('listening',address)

  try_async(lambda:my_main_ipc(address,'ipc'))

