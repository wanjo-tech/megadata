# DEPENDS
#   pip install -U pynng
# NOTES
#   zmq(zeromq) => nanomsg(github/nanomsg/nanomsg) => nng(nanomsg-next-gen,github/nanomsg/nng)
#   https://nanomsg.org/gettingstarted/index.html
#   https://github.com/codypiersall/pynng/

from .myeval import *

load_time = now()

get_builtins_default=lambda:{
  'type':lambda v:str(type(v)), # safety
  'api':fwdapi,
  'ping':now(),
  'print':print,
}

#async def tryxp(l,e=print):
#    try: return await try_await(l)
#    except Exception as ex: return ex if True==e else e(ex) if e else None

async def handle_nng(ctx,data,get_builtins):
  #rt = await tryxp(myevalasync(data,{'__builtins__':get_builtins()))
  try:
    rt = await myevalasync(data,{'__builtins__':get_builtins()})
  except Exception as ex:
    rt = ex
  rt = rt.encode() if type(rt) in [str] else o2b(rt) if type(rt) not in [bytes] else rt
  await ctx.asend(rt)

async def my_main_nng_async(address,get_builtins):
  import pynng
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

