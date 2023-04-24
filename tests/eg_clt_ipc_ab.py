# TODO argv

import sys

sys.path.insert(0,'..')
print('sys.path',sys.path)

from multiprocessing.connection import Client

from megadata.mypy import tryx, now, parallel, hook_quit, argv, argc, sys, os, build_address, ipc, ipcx, on_quit_default

#def on_quit(*a):
#  print('quit',a)
#  os._exit(0)
#hook_quit(on_quit)

hook_quit(on_quit_default)

address = build_address(argv[1], argv[2] if argc>2 else None)
print(address)

#def send_once(v):
#  conn = Client(address)
#  conn.send(v)
#  rt = conn.recv()
#  conn.close()
#  return rt

def send_once(v):
  rt = ipc(address,v)
  #print(address,'<=',v,'=>',rt)
  return rt

def test_send(v):
  rt = tryx(lambda:send_once(f'({now()})'))
  #print(rt)
  return rt

test_max = 999
def yield_arg():
  for v in range(1,test_max):
    yield v

t0=now()
parallel( test_send, yield_arg() )
t1=now()
t_ = t1-t0
print(t_, t_/test_max)

#for line in sys.stdin: print(send_once(line))

