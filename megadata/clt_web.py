from .mypy import tryx,sys,wc
def clt_web(argv,timeout=20):
  if len(argv)>1 and '://' in argv[1]:
    address = argv[1]
  else:
    port = tryx(lambda:int(argv[1]),False) or '80'
    host = tryx(lambda:argv[2],False) or '127.0.0.1'
    protocol = tryx(lambda:str(argv[3]),False) or 'http'
    address = f'{protocol}://{host}:{port}'
  print(f'clt_web{argv} to {address}')
  send_once = lambda v:wc(address, v, timeout=timeout)
  for line in sys.stdin: print(send_once(line))

if __name__ == '__main__':
  from .mypy import argv
  clt_web(argv)
