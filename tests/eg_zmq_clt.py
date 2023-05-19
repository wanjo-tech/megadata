from inc_mypy import *

hook_quit(on_quit_default)

import asyncio
if sys.platform=='win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#import zmq
#import zmq.asyncio
#
#ctx = zmq.asyncio.Context()
#
#socket = context.socket(zmq.REQ)
#socket.connect(url)

#endpoint = socket.getsockopt_string(zmq.LAST_ENDPOINT)
#print("endpoint=", endpoint)
#
#ROUTING_ID = socket.getsockopt_string(zmq.ROUTING_ID)
#print("ROUTING_ID=", ROUTING_ID)

def clt_zmq(argv):
  print('clt_ipc',argv)
  address = argv[1]
  print('address=',address)

  import zmq

  # TODO zmq.asyncio
  #import zmq.asyncio
  #ctx = zmq.asyncio.Context()

  # sync mode
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect(address)

  def server(v):
    if type(v) is str: v = v.encode()
    socket.send(v)
    return socket.recv()

  import pickle
  for line in sys.stdin:

    if line.startswith(':'): line = 'lambda' + line
    if line.startswith('lambda'): #
      fc = eval(line)
      #print('debug fc',fc,fc.__code__)
      b = dumps_func(fc)
      #print('debug fc',len(b),b)
      print(server(b))

    # e.g. /"Adm","ping"
    # have fund like /"Adm","ping",*args,**kwargs
    #  or /api("Adm","ping")
    elif line.startswith('/') and not line.startswith('/api'):
        print(server(f'/api({line[1:]})'))

    # super local lines
    # wanjo: play:
    # ;type(ipc(r'\\.\pipe\ipctest','algodata.dao,20220704'))
    # ;server('algodata.dao,20220704')
    # ;server('(api)')('Adm','ping')
    # ;server("""(api('algodata','dfb',20220704))""").shape
    elif line.startswith(';'):
      print( tryx(lambda:eval(line[1:],globals(),{'server':server})) )
      #print(out.keys())

    # e.g.
    # (api("Adm","ping"))
    # /api("Adm","ping")
    # what-so-ever
    else:
      rt = tryx(lambda:server(line))
      print(type(rt),'=>',rt)

if __name__ == '__main__':
    #asyncio.run(main())
    clt_zmq(argv)

