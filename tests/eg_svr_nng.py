from megadata.myeval import *

load_time = now()

hook_quit()

# story: 
# zmq(zeromq) => nanomsg(github.com/nanomsg/nanomsg) => nng(nanomsg-next-gen,github.com/nanomsg/nng)
# https://nanomsg.org/gettingstarted/index.html
# https://github.com/codypiersall/pynng/

# isntall
# pip install -U pynng

# example
# https://github.com/codypiersall/pynng/blob/master/examples/reqprep.py

import logging
import datetime
import pynng

DATE = "DATE"

o_globals = {"__builtins__":{
    'api':fwdapi,
    'useapi':useapi,
    'now':now(),'help':'nothing to help u unless u read the source codes'
    }}

# TODO KeyboardInterrupt => quit

async def handle_data(ctx,data):

    try:
      print(data);flush1()
      #log1('#');flush1()
      rt = await myevalasync(data,o_globals)
      # failed myeval (loop already started)
      #rt = myeval(data,o_globals)
    except Exception as ex:
      rt = {'errmsg':str(ex)}

    #print('debug1',type(rt),rt)
    #rt = rt.encode() if type(rt) in [str] else o2s(rt).encode() if type(rt) not in [bytes] else rt

    # 2023-05-27 nng using o2b for testing?
    rt = rt.encode() if type(rt) in [str] else o2b(rt) if type(rt) not in [bytes] else rt

    #print('debug2',type(rt),rt)
    print(type(rt),rt)

    # type_rst = type(rst)
    # if type_rst is str: rt = rst.encode()
    # elif type_rst in [dict,list,tuple]: rt = o2s(rst).encode()
    # else: rt = bytes(rst) # tmp
    # print('main.rt',rt)

    #logger.debug(f'=>{rt}')
    await ctx.asend(rt)
    #return rt

async def main_async(address):
    print('listen',address)
    with pynng.Rep0(listen=address) as socket:
        while await asyncio.sleep(0, result=True):
            ctx = socket.new_context()
            data = await ctx.arecv()
            #logging.debug(f'<={data}')
            asyncio.create_task(handle_data(ctx, data))

def my_main_nng(address):
    asyncio_run(main_async(address))


if __name__ == "__main__":
    """ TODO
import warnings
os.environ['PYTHONASYNCIODEBUG'] = '1'
logging.basicConfig(level=logging.DEBUG)
warnings.resetwarnings()
"""
    #logging.basicConfig(level=logging.DEBUG)

    try_async(lambda:my_main_nng(argv[1]))

    # tmp browing, todo start_stdin move to myeval
    #from megadata.svr_ipc_bin import start_stdin
    start_stdin(get_builtins=lambda:o_globals)

