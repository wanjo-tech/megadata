from megadata.mypy import tryx, now, parallel, hook_quit, argv, argc, sys, os, build_address
#import pynng
import zmq

def on_quit(*a):
  print('quit',a)
  os._exit(0)

hook_quit(on_quit)

address = argv[1]
print(address)

#socket = pynng.Req0()
#socket.dial(address)

def send_once(v):
  # sync mode
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect(address)

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

### python clt_zmq_ab.py "tcp://127.0.0.1:5555"
## 10s, 99/s ??? so slow
