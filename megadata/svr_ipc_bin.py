#-*- coding: utf-8 -*-

# server ipc mode (return str or json-str only)

# TODO merge logic with svr_ipcx.py => svr_ipc_bin.py [ipc/ipcx]

from .mypy import *
from .myeval import myeval,myevalasync,fwdapi

white_list = tryx(lambda:load('../tmp/white_list.json'))
black_list = tryx(lambda:load('../tmp/black_list.json')) or []

#my_encode = lambda rt: o2s(rt) if type(rt) is not str else rt

get_builtins = lambda:{
  #'type':type,# expose type is dangerous ;)
  'type':lambda v:str(type(v)),
  'api':fwdapi,
  'ping':now(),
  'print':print,
}

import pickle
def handle_ipc(param):
    loop = new_event_loop()
    conn,client = param
    assert client is None or len(client)==0 or (white_list is None) or (white_list and client[0] in white_list), f'banned {client}'

    # TODO if closed
    while True:
      #data = tryx(conn.recv,print)
      data = tryx(conn.recv)
      if data is None:
        #print('break')
        tryx(conn.close)
        break

      #print('TMP DEBUG handle_ipc',data)

      #rt_eval = tryx(lambda:myeval(data,{"__builtins__":get_builtins()},{}),True)
      rt_eval = loop.run_until_complete(try_await(tryx(lambda:myevalasync(data,{"__builtins__":get_builtins()},{}),True)))

      #print('TMP DEBUG rt_eval',rt_eval)

      if type(rt_eval) in [list,tuple,dict]:
        #rt = my_encode(rt_eval)
        rt = o2s(rt_eval)
        #print('debug rt_eval',data,type(rt_eval),type(rt),rt)
        if rt is None or "null"==rt: rt = rt_eval
      else: rt = rt_eval
      #print('debug rt_eval',data,type(rt_eval),type(rt),rt)

      if type(rt) not in [str,bytes]:
        rt = tryx(lambda:pickle.dumps(rt),True)

      # https://docs.python.org/3/library/multiprocessing.html
      conn.send(rt)

      # TODO print() will delay 25%
      # TODO --silent
      #print(f'{client}=>{len(rt) if len(rt)>999 else rt_eval}')

    # TODO no-close if reuse is True, for now no auto close...
    #tryx(conn.close)
    #return rt

def on_quit(*a):
  print('on_quit',a)
  os._exit(0)

def my_main_ipc(address,svr_mode='ipc',authkey=None,mode='pool',pool_size=None):

  print('my_main_ipc()','svr_mode=',svr_mode,'mode=',mode)

  from multiprocessing.connection import Listener
  server = Listener(address=address,authkey=authkey)

  if 'thread'==mode:
    while True:
      conn = tryx(server.accept)
      if conn is None: print('.')
      else: try_async(lambda:handle_ipc((conn,server.last_accepted)))

  elif 'asyncio'==mode:
    while True:
      conn = tryx(server.accept)
      if conn is None: print('.')
      else: try_asyncio(lambda:handle_ipc((conn,server.last_accepted)),new=True)

  else:# pool mode

    if svr_mode=='ipcx':# multiprocess-mode
      from multiprocessing import Pool
    else: # multithread-mode
      from multiprocessing.dummy import Pool

    with Pool(os.cpu_count()) as pool:
      while True:
        conn = tryx(server.accept)
        if conn is None: print('.')
        else: pool.map_async(handle_ipc, [(conn,server.last_accepted)])

def start_stdin():
  #for line in sys.stdin: print(myeval(line))
  loop = new_event_loop()
  for line in sys.stdin:
    if line.startswith(';'): # test god mode...
      print('=>', tryx(lambda:eval(line[1:])) )
      # TODO...
      #print( loop.run_until_complete(try_await(tryx(lambda:myevalasync(line[1:])) )))
    else: # test craft mode
      #r = myeval(line,{"__builtins__":get_builtins()},{})
      r = loop.run_until_complete(try_await(tryx(lambda:myevalasync(line,{"__builtins__":get_builtins()},{}))))
      print(type(r),r)

# quick test on main
if __name__ == '__main__':
  hook_quit(on_quit)

  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('listening',address)

  try_async(lambda:my_main_ipc(address,'ipc'))

