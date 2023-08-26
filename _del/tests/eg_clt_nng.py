import common

#from megadata.mypy import *
from megadata.myeval import *
import asyncio

DATE = "DATE"

def clt_nng(argv):
  print('clt_ipc',argv)
  address = argv[1]
  print('address=',address)

  server = lambda v:nng(address,v)

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
    clt_nng(argv)

