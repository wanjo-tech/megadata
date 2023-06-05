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

from megadata.myeval import *
load_time = now()
hook_quit()

from megadata.svr_ipc_bin import my_main_ipc, start_stdin

address = build_address(('wtf' if argc<2 else argv[1]))
print('address',address)


async_call(lambda:my_main_ipc(address,mode='asyncio'))
start_stdin()


