import sys
sys.path.append('..')

from mypy import build_address,try_asyncio as async_call
from svr_ipc_bin import my_main_ipc, start_stdin

address = build_address(('wtf'))
print('address',address)

#my_main_ipc(address)
async_call(lambda:my_main_ipc(address2))
start_stdin()


