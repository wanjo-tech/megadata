import sys,os

#print("__package__",__package__)
#print("__file__",__file__)

sys.path.insert(0, '..')

#path = os.path.dirname(os.path.dirname(__file__))
#sys.path.insert(0, path)

print('sys.path',sys.path)

import megadata
print('megadata.load_time=',megadata.load_time)
print('megadata.module_version=',megadata.module_version)


from megadata.mypy import build_address,try_asyncio as async_call,hook_quit,on_quit_default,argv,argc
hook_quit(on_quit_default)

from megadata.svr_ipc_bin import my_main_ipc, start_stdin

address = build_address(('wtf' if argc<2 else argv[1]))
print('address',address)

#my_main_ipc(address,mode='asyncio')

async_call(lambda:my_main_ipc(address,mode='asyncio'))
start_stdin()


