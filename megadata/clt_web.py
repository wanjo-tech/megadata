from megadata.mypy import tryx, now, parallel, hook_quit, argv, argc, sys, os,wc

def clt_web(argv):
  print('clt_web',argv)
  def on_quit(*a):
    print('quit',a)
    os._exit(0)

  hook_quit(on_quit)

  port = tryx(lambda:int(argv[1]),False) or '80'

  host = tryx(lambda:argv[2],False) or '127.0.0.1'
  protocol = tryx(lambda:int(argv[3]),False) or 'http'

  address = f'{protocol}://{host}:{port}'

  print(address)

  def send_once(v):
    rt = wc(address, v, timeout=20)
    return rt

  def yield_arg():
    for v in range(1,9999):
      yield v

  for line in sys.stdin: print(send_once(line))

if __name__ == '__main__':
  clt_web(argv)
