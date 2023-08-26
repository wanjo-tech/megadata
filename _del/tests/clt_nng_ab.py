from megadata.mypy import tryx, now, parallel, hook_quit, argv, argc, sys, os, build_address
import pynng

def on_quit(*a):
  print('quit',a)
  os._exit(0)

hook_quit(on_quit)

address = argv[1]
print(address)

def send_once(v):
  socket = pynng.Req0()
  socket.dial(address)

  if type(v) is str: v = v.encode()
  socket.send(v)
  return socket.recv()

def test_send(v):
  tryx(lambda:send_once(f'({now()})'))
  #return rt

def yield_arg():
  for v in range(1,999):
    yield v

t0=now()
parallel( test_send, yield_arg() )
t1=now()
print(t1-t0)

#for line in sys.stdin: print(send_once(line))

### python clt_nng_ab.py "ipc:///tmp/wtf.ipc"
### 15s
