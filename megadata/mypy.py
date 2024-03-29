#-*- coding: utf-8 -*-

# py-coding-simplifer by Wanjo

from time import time as now, mktime, sleep

load_time = now()

#exec('def tryx(l,e=print):\n try:return l()\n except Exception as ex:return ex if True==e else e(ex) if e else None')
def tryx(l,e=print):
    try: return l()
    except Exception as ex: return ex if True==e else e(ex) if e else None

import sys
argv = sys.argv
argc = len(argv)

if sys.stdout:
  log1 = sys.stdout.write
  flush1 = sys.stdout.flush
if sys.stderr:
  log2 = sys.stderr.write
  flush2 = sys.stderr.flush

def print1(*args):
  for v in args: log1(f'{v} ')
  log1('\n')
  flush1()

import os
touch_dir = lambda fn:os.makedirs(fn,exist_ok=True)
file_exists = os.path.exists
get_mtime = lambda f:os.path.getmtime(f)

# rename or delete
def file_rename(fnold,fnnew=None,try_delete_after=False):
    if try_delete_after:
        fnnew = f'{fnnew}.delete.{now()}'
    tryx(lambda:os.rename(fnold,fnnew))
    if try_delete_after:
        tryx(lambda:os.remove(fnnew))

evalx = lambda s,g=globals(),l=locals():eval(s,g,l)

flag_py2 = sys.version_info.major==2
import importlib
sys_import = importlib.import_module
sys_reload = importlib.reload
refresh = lambda n:sys_reload(sys_import(n))

class probe:
    def __init__(self,ev): self._ev=ev
    def __getattr__(self,k): return tryx(lambda:self._ev(k))

class probex:
    def __init__(self,ev,debug=False):
      self._ev=ev
      self.debug = debug
    def __getattr__(self,k):
      rt = tryx(lambda:self._ev(k),self.debug)
      if rt is None: rt = tryx(lambda:sys_import(k),self.debug)
      return rt

mypy = probex(evalx)

import marshal,types

def use(mdlname,clsname=None,reload=False):
  rt = None
  if type(mdlname) is str:
    if reload:
      rt = refresh(mdlname)
    else:
      rt = sys_import(mdlname)
  else:
    rt = mdlname
  if type(clsname) is str:
    #return tryx(lambda:getattr(rt,clsname))
    for v in clsname.split('.'):
      rt = tryx(lambda:getattr(rt,v))
      if rt is None: break # safety
  return rt

# useapi is not good for hardcoded 'api', use your own
# e.g. func = useapi(f'api{c}',m,request=request,post_s=post_s,post_o=post_o)
useapi = lambda c,m,*args,**kwargs: getattr(use(c,'api')(*args,**kwargs),m)

#if not flag_py2: # patch for some urlopen case
if True:
    # https://stackoverflow.com/questions/18466079/change-the-connection-pool-size-for-pythons-requests-module-when-in-threading/22253656#22253656
    def patch_connection_pool(**constructor_kwargs):
        from urllib3 import connectionpool, poolmanager
        class MyHTTPConnectionPool(connectionpool.HTTPConnectionPool):
            def __init__(self, *args,**kwargs):
                kwargs.update(constructor_kwargs)
                super(MyHTTPConnectionPool, self).__init__(*args,**kwargs)
        poolmanager.pool_classes_by_scheme['http'] = MyHTTPConnectionPool
        class MyHTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
            def __init__(self, *args,**kwargs):
                kwargs.update(constructor_kwargs)
                super(MyHTTPSConnectionPool, self).__init__(*args,**kwargs)
        poolmanager.pool_classes_by_scheme['https'] = MyHTTPSConnectionPool
    #tryx(lambda:patch_connection_pool(maxsize=16))

def delx(o,k):
    tryx(lambda:o.__delitem__(k),False)
    tryx(lambda:o.__delattr__(k),False)
    return o

import json
#class MyJsonEncoder(json.JSONEncoder): default = lambda self,obj:tryx(lambda:json.JSONEncoder.default(self,obj),lambda ex:str(obj))
#o2s = lambda o,indent=None,separators=(',',':'):json.dumps(o, indent=indent, ensure_ascii=False, separators=separators, cls=MyJsonEncoder)
s2o = lambda s,eh=False:tryx(lambda:json.loads(s),eh)
o2s = lambda o,indent=None,separators=(',',':'):json.dumps(o, indent=indent, ensure_ascii=False, separators=separators, cls=type("MyJsonEncoder", (json.JSONEncoder,), { "default": lambda self, obj: tryx(lambda: json.JSONEncoder.default(self, obj), lambda ex: str(obj)) }))

from pickle import dumps as o2b, loads as b2o
o2b_None = o2b(None)

from urllib.request import urlopen
def get_urlopen():
  #if flag_py2: from urllib2 import urlopen
  #else: from urllib.request import urlopen
  return urlopen

# NOTES: one-off simple web call, not for heavy usage!! using aiohttp instead!

wc=lambda u=None, data=None, m='POST', timeout=10:get_urlopen()(url=u,data=data.encode('utf-8') if isinstance(data,str) else o2s(data).encode('utf-8') if data else None,timeout=timeout).read().decode()

# NOTES: one-off ws call, not for heavy usage!!! has problem of IO-blocking
def wsc(u,data,lines=1):
  s=data.encode('utf-8') if isinstance(data,str) else o2s(data).encode('utf-8') if data else None

  import websocket
  conn = websocket.create_connection(u)

  conn.send(s)
  if lines==1:
    rt = tryx(conn.recv,False)
  else:
    rta = []
    while True:
      rt = tryx(conn.recv,False)
      if rt is None: break
      rta.append(rt)
    rt = '\n'.join(rta)
  tryx(conn.close,False)
  return rt

# NOTES:
## UP {bytes: ..., None: None, str: encode('utf-8'), else:o2s(...).encode('utf-8')}
## DN {bytes: b2o, else:...} 
def ipc(u,data,authkey=None,out=None,timeout=7):
  s=data.encode('utf-8') if isinstance(data,str) else data if isinstance(data,bytes) else o2s(data).encode('utf-8') if data is not None else None
  #print('dbg.ipc=>',type(data),type(s))
  from multiprocessing.connection import Client,wait
  close = False
  if out is None:
    conn = Client(u)
    close = True
  elif 'conn' in out.keys():
    #print('reuse')
    conn = out['conn'] # try reuse
    if conn is None:
      conn = Client(u)
      out['conn'] = conn
  else: # cache into out
    conn = Client(u)
    out['conn'] = conn
  try:
    conn.send(s)
    if timeout: wait([conn],timeout)
    rt = conn.recv()
  except Exception as ex:
    if out is not None:
      if 'conn' in out.keys():
        del out['conn']
    rt = None
    tryx(conn.close)
    raise ex
  if close: tryx(conn.close)
  #print('dbg.ipc<=',type(rt))

  if isinstance(rt, bytes):
    try:
      rt = b2o(rt)
    except Exception as ex:
      pass
  return rt

build_api_closure=lambda *args,**kwargs:eval(f'lambda:api(*{args},**{kwargs})')

## TODO timeout and out not yet
def nng(address,data,authkey=None,out=None,timeout=7):
  import pynng
  if type(address) in [tuple,list]: # assume from build_address()
    #print(type(address),address)
    len_address = len(address)
    host = address[0]
    port = address[1]
    protocol = address[2] if len_address>2 else 'tcp'
    address = f'{protocol}://{host}:{port}'
  with pynng.Req0(dial=address) as sock:
    if type(data) is str: data = data.encode()
    sock.send(data)
    b = sock.recv()
    if b == o2b_None: return None
    s = tryx(lambda:b.decode(),False) # check if b-str
    if s is not None: return s
    o = tryx(lambda:b2o(b),False) # or check from o2b()
    if o is not None: return o
    return b # raw anyway

#nngx = lambda *args,**kwargs:try_asyncio_async(lambda:nng(*args,**kwargs))
async def nngx(address,data,authkey=None,out=None,timeout=7):
  import pynng
  if type(address) in [tuple,list]: # assume from build_address()
    #print(type(address),address)
    len_address = len(address)
    host = address[0]
    port = address[1]
    protocol = address[2] if len_address>2 else 'tcp'
    address = f'{protocol}://{host}:{port}'
  with pynng.Req0(dial=address) as sock:
    if type(data) is str: data = data.encode()
    await sock.asend(data)
    b = await sock.arecv()
    if b == o2b_None: return None
    s = tryx(lambda:b.decode(),False) # check if b-str
    if s is not None: return s
    o = tryx(lambda:b2o(b),False) # or check from o2b()
    if o is not None: return o
    return b # raw anyway

# NOETS need to wrap own rpc/rpcx
# e.g. rpc(build_address(3388))('Adm','ping')
rpc = lambda u,authkey=None,out=None,timeout=7:(lambda *rpc_args,**rpc_kwargs:ipc(u,dumps_func(build_api_closure(*rpc_args,**rpc_kwargs)),authkey=authkey,out=out,timeout=timeout))

read = lambda f,m='r',encoding='utf-8':open(f,m,encoding=encoding).read()
# for binary: write(f,s,'wb',None)
write = lambda f,s,m='w',encoding='utf-8':open(f,m,encoding=encoding).write(s)
load = lambda f:s2o(read(f))
save = lambda f,o:write(f,o2s(o))

log = lambda fn,o,ln='\n':write(fn, f'{o if type(o) is str else o2s(o)}{ln}', 'a')

dumps_func = lambda func:marshal.dumps(func.__code__)
loads_func = lambda codes,ctx,name=None:types.FunctionType(marshal.loads(codes),ctx,name=name)
func2file = lambda fc,fn:write(fn,dumps_func(fc),'wb',None)
file2func = lambda fn,ctx=globals(),name=None:types.FunctionType(marshal.loads(read(fn,'rb',None)),ctx,name=name)

class obj(dict):# dictx
    def __init__(self,pa=None):
        for k in pa or {}:self[k]=pa[k]
    def __getitem__(self,key): return self.get(key)
    def __getattr__(self,key): return self[key]
    def __setattr__(self,k,v): self[k]=v

class objx(dict):#dictxx
    def __init__(self,*args,**kwargs):# TODO for v in args.values(): if type(v) is dict, merge k=>v
        for k,v in kwargs.items():self[k]=v
    def __getitem__(self,key): return self.get(key)
    def __getattr__(self,key): return self[key]
    def __setattr__(self,k,v): self[k]=v

def on_quit_default(*a):
  print('on_quit_default',*a)
  os._exit(0)

def hook_quit(on_quit=on_quit_default):
    import signal
    signal.signal(signal.SIGINT, on_quit)
    if sys.platform != 'win32': signal.signal(signal.SIGHUP, on_quit)
    signal.signal(signal.SIGTERM, on_quit)

sgn = lambda v:1 if v>0 else -1 if v<0 else 0
lvl = lambda v,d=0.05:round(v/d-sgn(v)*0.5) #level to zero by d
almost = lambda v1,v2,epsilon=0.0001:abs(v1-v2)<epsilon

# tips: for HH:MM:SS, days should be 1970 ;)
def time_maker(days=0,date=None,outfmt=None,infmt='%Y-%m-%d',
        months=0):
    from datetime import datetime,timedelta
    if date is None: _dt = datetime.now()
    else: _dt = datetime.fromtimestamp(int(date))\
        if infmt=='0' or not infmt\
        else datetime.strptime(str(date),infmt)
    if months>0 or months<0:
        from dateutil.relativedelta import relativedelta
        _dt += relativedelta(months=months)
    _dt += timedelta(days=days)
    if outfmt is None: outfmt = infmt
    if outfmt=='0' or not outfmt:
        return int(mktime(_dt.timetuple()))
    return _dt.strftime(outfmt)

#e.g. acct_num = re_match(r'\D*(\d*)',str(acct))
import re
re_match=lambda p,s,a=re.M|re.I:(re.search(p, s, a) or [None,None])[1]
#e.g. re_replace(r'\D+','?',r'test 1234 ok')
re_replace=lambda p,needle,hay,a=re.M|re.I:re.sub(p, needle, hay, a)

# e.g. attachment_data = read('QR.png','rb',None)
# TODO support list of attachment_data/attachment_name later

import multiprocessing
def parallel(func, a, pool_size=None,chunksize=None,mode='default',map_async=False):
  proc_name = multiprocessing.current_process().name
  if mode in ['loky','multiprocessing'] and proc_name!='MainProcess':
    print(f'WARNING: mode-{mode} on {proc_name}, should kick in __main__')
    return []
  #print(f'proc_name={proc_name}')

  if pool_size is None:
    from os import cpu_count
    pool_size =  cpu_count()

  if mode == 'loky': 
    from joblib import Parallel,delayed
    rt = Parallel(n_jobs=pool_size,backend=mode)(delayed(func)(v) for v in a)
    if not map_async: return rt
  if mode == 'multiprocessing':
    Pool = multiprocessing.Pool
  else: # default is thread mode
    from multiprocessing.dummy import Pool
  if map_async:
    return Pool(pool_size).map_async(func, a, chunksize=chunksize)
  else:
    return Pool(pool_size).map(func, a, chunksize=chunksize)

def mygc():
    import gc
    import sys
    # gc-patch for win32
    if sys.platform=='win32':
        # https://stackoverflow.com/questions/31851848/python-program-memory-in-windows
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        def errcheck_bool(result, func, args):
            if not result: raise ctypes.WinError(ctypes.get_last_error())
            return args

        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        kernel32.SetProcessWorkingSetSize.errcheck = errcheck_bool
        kernel32.SetProcessWorkingSetSize.argtypes = (wintypes.HANDLE,
                                                      ctypes.c_size_t,
                                                      ctypes.c_size_t)
        hProcess = kernel32.GetCurrentProcess()
        kernel32.SetProcessWorkingSetSize(hProcess, -1, -1)
    elif sys.platform=='linux':
        from ctypes import cdll, CDLL
        try:
            cdll.LoadLibrary("libc.so.6")
            libc = CDLL("libc.so.6")
            libc.malloc_trim(0)
        except (OSError, AttributeError):
            libc = None
    gc.collect()
    return len(gc.get_objects())

#def md5(s):return mypy.hashlib.md5(bytes(s,encoding='utf8')).hexdigest()
md5=lambda s:mypy.hashlib.md5(bytes(s,encoding='utf8')).hexdigest()

def yielder(func,wrap=tryx,do_yield=True): yield (wrap(func) if wrap else func())
def yielder_loop(func,wrap=tryx,do_yield=True):
  while True:
    rt = yield from yielder(func, wrap, do_yield)
    if do_yield and rt is not None: yield rt

Thread = mypy.threading.Thread
def try_async(func): Thread(target=func).start()

# for ipc()
def build_address(arg1,arg2=None,folder='../tmp/'):
  port = tryx(lambda:int(arg1),False)
  if port is None:
    if sys.platform=='win32':
      host = '.' if arg2 is None else arg2
      address = rf'\\{host}\pipe\{arg1}'
    else:
      address = f'{folder}{arg1}.sck'
  else:
    host = '127.0.0.1' if arg2 is None else arg2
    address = (host,port)
  return address

import subprocess
def passthrough(cmd,shell=True,stdout=sys.stdout,stderr=sys.stderr,wait=True):
  rt = subprocess.Popen(cmd,shell=shell,stdout=stdout,stderr=stderr)
  if wait: return rt.wait()
  return rt

passthru = passthrough

#def systemx(cmd,w=None,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=0x08000000):
#  _stdout = sys.stdout if stdout is None else stdout
#  with subprocess.Popen(cmd, stdout=_stdout, stdin=subprocess.PIPE,creationflags=creationflags) as p:
#      return p.communicate(input=w.encode() if type(w) is str else w)[0] if w else p.stdout.read() if p.stdout is not None and stdout is not None else None
CREATE_NO_WINDOW = 0x08000000
def systemx(cmd,w=None,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=0):
  _stdout = sys.stdout if stdout is None else stdout
  #if stdout is None: creationflags = 0
  with subprocess.Popen(cmd, stdout=_stdout, stdin=subprocess.PIPE,creationflags=creationflags) as p:
      return p.communicate(input=w.encode() if type(w) is str else w)[0] if w else p.stdout.read() if p.stdout is not None and stdout is not None else None

# audit = print
# .stdout, .stderr, .returncode
def system(cmd_or_a,stdout_only=True,audit=None):
  result = subprocess.run(cmd_or_a, shell=True, capture_output=True, text=True)
  rt = result.stdout if stdout_only else result
  if audit: audit(rt)
  return rt

system_call = lambda cmd: subprocess.call(cmd,shell=True)

#################### async tools


import asyncio
from asyncio import iscoroutinefunction,iscoroutine,run as asyncio_run,get_event_loop,new_event_loop,set_event_loop,sleep as sleep_async

from asyncio import Semaphore,gather,wait_for

# asyncio version of parallel()
async def parallelx(async_func, a, pool_size=None, timeout=30):
    async def limited_concurrent_tasks(semaphore, async_func, arg):
        async with semaphore:
            #return await async_func(arg)
            return await wait_for(async_func(arg),timeout=timeout)
    if pool_size is None:
      from os import cpu_count
      pool_size =  cpu_count()
    semaphore = Semaphore(pool_size)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as pool:
        loop = get_event_loop()
        #tasks = [loop.create_task(async_func(arg)) for arg in a]
        tasks = [loop.create_task(limited_concurrent_tasks(semaphore,async_func,arg)) for arg in a]
        return await gather(*tasks)

from inspect import isawaitable as is_awaitable

async def try_await(o):
  rt = o
  while is_awaitable(rt):
    rt = await rt
  return rt

async def tryxp(l,e=print):
    try: return await try_await(l)
    except Exception as ex: return ex if True==e else e(ex) if e else None

try_asyncio = lambda sync_func,new=False,executor=None:(new_event_loop if new else get_event_loop)().run_in_executor(executor,sync_func)

async def try_asyncio_async(sync_func,new=False): return await try_await(try_asyncio(sync_func,new))

# somehow like asyncio_run
def run_until_complete(fn,new=True,timeout=0):
  if callable(fn): new=False
  loop = (new_event_loop if new else get_event_loop)()
  async_o = try_asyncio_async(fn) if callable(fn) else try_await(fn) if timeout==0 else wait_for(try_await(fn),timeout=timeout)
  return loop.run_until_complete(async_o)

# some block-sync to non-block-async: 
ipcx = lambda *args,**kwargs:try_asyncio_async(lambda:ipc(*args,**kwargs))
wcx = lambda *args,**kwargs:try_asyncio_async(lambda:wc(*args,**kwargs))
sleepx = lambda *args:try_asyncio_async(lambda:sleep(*args))

def rpcx(u,authkey=None,out=None,timeout=7):
  async def rpc_func(*rpc_args,**rpc_kwargs):
    c = build_api_closure(*rpc_args,**rpc_kwargs)
    b = dumps_func(c)
    s=await ipcx(u,b,authkey=authkey,out=out,timeout=timeout)
    return s2o(s)
  return rpc_func

destruct = lambda d,k:[d.get(k.strip()) for k in k.split(',')]

#################### DELETED
#sys_reload = __builtins__.reload if flag_py2 else sys_import('importlib').reload
#sys_import = __import__
#flag_py2 = sys.version_info.major==2
