if __name__ == '__main__':

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
  from megadata.clt_ipc import *
  clt_ipc(argv)

