import os
import sys
import warnings

# Remove '' and current working directory from the first entry
# of sys.path, if present to avoid using current directory
# in pip commands check, freeze, install, list and show,
# when invoked as python -m pip <command>
if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python pip-*.whl/pip install pip-*.whl
if __package__ == "":
    # __file__ is pip-*.whl/pip/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/pip'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

#print(sys.path)

# tmp, will improve later
def main(argv):
  typ = argv[0]
  if typ=='ipc':
    from megadata.clt_ipc import clt_ipc
    clt_ipc(argv)
  elif typ=='web':
    from megadata.clt_web import clt_web
    clt_web(argv)
  else:
    print(f'not yet support {typ}')

if __name__ == "__main__":
  from megadata.mypy import argv

  # python -m megadata clt ipcft .
  main(argv[1:])

#else:
#  print(__name__,argv)

#  class argchain:
#    def __init__(self,*args,**kwargs):
#      import argparse
#      self.argparser = argparse.ArgumentParser()
#      self(*args,**kwargs)
#
#    def __call__(self,*args,**kwargs):
#      if len(args)>0 or len(kwargs)>0:
#        self.argparser.add_argument(*args,**kwargs)
#      return self
#
#    def dict(self):
#      return self.argparser.parse_args().__dict__

#  main(argchain
#      ('clt',type=str,help='sub command')
#      ('port',help='port or named pipe',type=str)
#      ('host,help='port',type=str)
#      ('[authkey],help='authkey',type=str)
#      .dict())

