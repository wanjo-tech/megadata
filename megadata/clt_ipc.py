from mypy import *

def on_quit(*a):
  print('on_quit',*a)
  os._exit(0)
hook_quit(on_quit)

def clt_ipc(argv):
  argc = len(argv)
  address = build_address(argv[1], argv[2] if argc>2 else None)

  out={}
  server= lambda v: ipc(address, v, out=out)

  import pickle
  for line in sys.stdin:

    if line.startswith('lambda'): # TMP TEST RPC
      fc = eval(line)
      #print('debug fc',fc,fc.__code__)
      print(server(dumps_func(fc)))

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
    elif line.startswith(';'):
      print( tryx(lambda:eval(line[1:])) )
      #print(out.keys())

    # e.g.
    # (api("Adm","ping"))
    # /api("Adm","ping")
    # what-so-ever
    else:
      rt = tryx(lambda:server(line))
      print(type(rt),'=>',rt)

if __name__ == '__main__':
  clt_ipc(argv)
