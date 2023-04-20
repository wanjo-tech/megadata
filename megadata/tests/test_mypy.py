import sys
sys.path.append('..')

from mypy import try_asyncio

import asyncio
from asyncio import get_event_loop, run as asyncio_run,new_event_loop

# debug get_event_loop
#try_asyncio = lambda func:get_event_loop().run_in_executor(None,func)
# debug new_event_loop
#try_asyncio_new = lambda func:new_event_loop().run_in_executor(None,func)

async def async_print(*args,**kwargs):
    return await try_asyncio(lambda:print(*args,**kwargs))

async def async_print_new(*args,**kwargs):
    return await try_asyncio(lambda:print(*args,**kwargs),new=True)

def test_print():
    rt = asyncio_run(async_print('hello world'))
    assert rt is None, 'async_print should return None'

# TODO: sth wrong with future
#def test_print_new():
#    rt = asyncio_run(async_print_new('hello world2'))
#    assert rt is None, 'async_print should return None'
