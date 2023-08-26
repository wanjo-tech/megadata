import sys

sys.path.append('..')

from mypy import parallelx,try_await

from asyncio import sleep as async_sleep

async def print_async(*args, **kwargs):
    await async_sleep(1)
    return await try_await(print(*args, **kwargs))

async def main():
    rst = await parallelx(print_async, range(10), pool_size=3)
    print('rst=',rst)

import asyncio
#asyncio.run(main())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

