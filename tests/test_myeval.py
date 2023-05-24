if __name__ == '__main__':

  # python tests\test_myeval.py
  # /api('Adm','pingx')
  # Adm.ping

  import sys,os

  #print("__package__",__package__)
  #print("__file__",__file__)

  sys.path.insert(0, '..')

  path = os.path.dirname(os.path.dirname(__file__))
  sys.path.insert(0, path)

  print('sys.path',sys.path)

  import megadata
  print('megadata.load_time=',megadata.load_time)
  print('megadata.module_version=',megadata.module_version)
  ################################################################

  from megadata.myeval import *
 
  #def server(v):
  #  #return ipc(address,v,out=out)
  #  return ipc(address,v)

  def server(v):
    o_globals = {"__builtins__":{
      'type':type,
      'api':fwdapi,
      'now':now(),'help':'nothing to help u unless u read the source codes'
    }}
    #return tryx(lambda:myeval(v,o_globals))
    return run_until_complete(myevalasync(v,o_globals))


  """ e.g.
  /now
  /help
  (help)
  ["Adm.ping"]
  Adm.ping
  /api('Adm','ping')
  (type(type))
  lambda:api('Adm','pingx')
  """
  if sys.flags.interactive:
    print('interactive mode')
    #server(dumps_func(lambda:__builtins__))
    #server(dumps_func(lambda:api.__code__))
    pass
  else:
    for line in sys.stdin:
      if line.startswith('lambda'): # TMP TEST RPC
        fc = eval(line)
        #print('debug fc',fc,fc.__code__)
        rt = server(dumps_func(fc))
        print('=>',type(rt),f'=>{rt}')
      else:
        rt = server(line)
        print('=>',type(rt),f'=>{rt}')
 
