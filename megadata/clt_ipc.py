from .mypy import *


hook_quit(on_quit_default)

def clt_ipc(argv):
  print('clt_ipc',argv)
  argc = len(argv)
  address = build_address(argv[1], argv[2] if argc>2 else None)
  print('address=',address)

  # out={} # reusing has bug yet, todo
  #server= lambda v: ipc(address, v, out=out)
  def server(v):
    #return ipc(address,v,out=out)
    return ipc(address,v)

  import pickle
  for line in sys.stdin:

    if line.startswith('lambda'): # TMP TEST RPC
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

