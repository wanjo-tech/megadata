# NOTES:
# 2023-05-26 企图测试pynng，发现在concurrent下有问题，用来做服务器可能出问题。至于zeromq还没空试...
### pynng.exceptions.BadState: Incorrect state

#from megadata.mypy import *
from megadata.myeval import *

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

# address = "ipc:///tmp/wtf.ipc"
#'tcp://127.0.0.1:5555'

o_globals = {"__builtins__":{
    'api':fwdapi,
    'useapi':useapi,
    'now':now(),'help':'nothing to help u unless u read the source codes'
    }}

# TODO KeyboardInterrupt => quit

async def handle_data(ctx,data):
    log1('#');flush1()

    try:
      rt = await myevalasync(data,o_globals)
      #rt = now()
    except Exception as ex:
      rt = {'errmsg':str(ex)}

    rt = rt.encode() if type(rt) in [str] else o2s(rt).encode() if type(rt) not in [bytes] else rt

    # type_rst = type(rst)
    # if type_rst is str: rt = rst.encode()
    # elif type_rst in [dict,list,tuple]: rt = o2s(rst).encode()
    # else: rt = bytes(rst) # tmp
    # print('main.rt',rt)

    logging.debug(f'=>{rt}')
    await ctx.asend(rt)
    #return rt

async def main_async(address):
    print('listen',address)
    with pynng.Rep0(listen=address) as socket:
        while await asyncio.sleep(0, result=True):
            ctx = socket.new_context()
            data = await ctx.arecv()
            logging.debug(f'<={data}')
            asyncio.create_task(handle_data(ctx, data))


if __name__ == "__main__":
    """ TODO
import warnings
os.environ['PYTHONASYNCIODEBUG'] = '1'
logging.basicConfig(level=logging.DEBUG)
warnings.resetwarnings()
"""
    #logging.basicConfig(level=logging.DEBUG)

    address = argv[1]
    print('address=',address)
    asyncio_run(main_async(address))
