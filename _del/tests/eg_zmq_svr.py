from inc_mypy import *
hook_quit(on_quit_default)

###################################################

# TODO https://github.com/aio-libs/aiozmq

#from .myeval import myeval,myevalasync,fwdapi
from megadata.myeval import myeval,myevalasync,fwdapi

url = 'tcp://*:5555'
# windows not support ipc:// but nng do ??
#url = 'ipc:///tmp/wtf.ipc'

import asyncio
if sys.platform=='win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()

get_builtins_default = lambda:{
  #'type':type,# directly exposing type is dangerous ;)
  'type':lambda v:str(type(v)), # safer
  'api':fwdapi,
  'ping':now(),
  'print':print,
}

import pickle
async def main(get_builtins=get_builtins_default):
    sock = ctx.socket(zmq.REP)
    sock.bind(url)

    while True:
        data = await sock.recv()
        try:
          rt_eval = await myevalasync(data,{"__builtins__":get_builtins()},{})
        except Exception as ex:
          rt_eval = {'errmsg':str(ex)}

        if type(rt_eval) in [list,tuple,dict]:
          rt = o2s(rt_eval)
          if rt is None or "null"==rt: rt = rt_eval
        else: rt = rt_eval
        if type(rt) not in [str,bytes]:
          rt = tryx(lambda:pickle.dumps(rt),True)
        if type(rt) is str:
          await sock.send_string(rt)
        else:
          await sock.send(rt)

if __name__ == '__main__':
    asyncio.run(main())

