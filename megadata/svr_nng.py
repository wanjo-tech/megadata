# INSTALL 
# pip install -U pynng

# NOTES: 
# zmq(zeromq) => nanomsg(github.com/nanomsg/nanomsg) => nng(nanomsg-next-gen,github.com/nanomsg/nng)
# https://nanomsg.org/gettingstarted/index.html
# https://github.com/codypiersall/pynng/

#from megadata.myeval import *
from .myeval import *

load_time = now()

import pynng

get_builtins_default=lambda:{
  'type':lambda v:str(type(v)), # safer
  'api':fwdapi,
  'ping':now(),
  'print':print,
}

async def handle_nng(ctx,data,get_builtins):
  try:
    rt = await myevalasync(data,{'__builtins__':get_builtins()})
  except Exception as ex:
    rt = {'errmsg':str(ex)}
  rt = rt.encode() if type(rt) in [str] else o2b(rt) if type(rt) not in [bytes] else rt
  await ctx.asend(rt)
  #return rt

async def my_main_nng_async(address,get_builtins):
  if type(address) in [tuple,list]: # assume from build_address()
    #print(type(address),address)
    len_address = len(address)
    host = address[0]
    port = address[1]
    protocol = address[2] if len_address>2 else 'tcp'
    address = f'{protocol}://{host}:{port}'
  print('address=',address)
  with pynng.Rep0(listen=address) as socket:
    while await sleep_async(0, result=True):
      ctx = socket.new_context()
      data = await ctx.arecv()
      asyncio.create_task(handle_nng(ctx, data, get_builtins))

def my_main_nng(address,get_builtins=get_builtins_default):
    asyncio_run(my_main_nng_async(address,get_builtins))

