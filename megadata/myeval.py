# eval tool by wanjo 20230527
# TODO is_awaitable need while-loop
# TODO merge codes to more elegant..

from .mypy import *
load_time = now()

import logging
logger = logging.getLogger(__name__)

# fwdapi = lambda c,m,*args,**kwargs:useapi(f'api{c}',m)(*args,**kwargs)
def fwdapi(c,m,*args,**kwargs):
  rt = useapi(f'api{c}',m)(*args,**kwargs)
  if is_awaitable(rt):
    rt = run_until_complete(try_await(rt))
  return rt

def myeval(s,g={},l={}):
    rt = None

    if type(s) is bytes: # try pickle/loads_func/...
        o = tryx(lambda:b2o(s),False)
        if o is None: # not pickle, try bytes-utf8-str
            o = tryx(lambda:s.decode(),False)
        if o is None: # try rpc function...
            oo = tryx(lambda:loads_func(s,g)) # load by ctx g
            if oo is not None:
              rt = tryx(oo,True)
              if is_awaitable(rt):
                rt = run_until_complete(try_await(rt))
              return rt
        s = o

    s = f'{s}'.strip()
    if len(s)<1: return None

    a = s2o(s)
    if logger.level>=logging.DEBUG:
        logger.debug(f'===In: {a or s}')

    call_id = None
    call_param = None
    call_style = None
    call_entry = None
    #if type(a) is list: # list-come-list-go

    if s[0]=='[': # list mode w+/- call_id
        # [ call_id:Optional, call_entry, [call_param...] ]
        # => [call_param, call_result]

        call_style = 1
        len_a = len(a)
        a0i = tryx(lambda:int(a[0]),False)
        if len_a>1 and type(a0i) is int:
            call_entry = a[1]
            call_param = tryx(lambda:a[2:],False)
            call_id = a[0]
        elif len_a>0:
            call_entry = a[0]
            call_param = tryx(lambda:a[1:],False)

    elif s[0]=='(' or s[0]=='/': # pyql ;)
        s=s.replace('__builtins__','') # safe-guard ;)
        if s[0]=='/': s = s[1:]
        rt = tryx(lambda:eval(s,g,l),True)

    elif s[0]=='{': # dict-come-dict-go, old and please try not to use...
        # deprecated ,dict mode is not good too
        call_style = 2
        call_entry = a.get('entry',None)
        call_param = a.get('param',[])
        call_id = a.get('id',None)

    elif a is None: # simple quick console mode sep by comma
        call_style = 3
        s=s.replace('\t','')
        a = s.split(',')
        len_a = len(a)
        a0i = tryx(lambda:int(a[0]),False)
        if len_a>1 and type(a0i) is int:
            call_style = 1 # rollback to list-mode
            call_entry = a[1]
            call_param = tryx(lambda:a[2:],False)
            call_id = a0i or a[0]
        elif len_a>0:
            call_entry = a[0]
            call_param = tryx(lambda:a[1:],False)

    if rt is None and call_style is not None:
        a = call_entry.split('.')
        if len(a)<2:
            rt = {'errmsg':'wrong entry {}'.format(call_entry)}
        else:
            rt = fwdapi(a[0],a[1],*call_param)

    # 2023-05-24 make the async-awaitable to sync
    if is_awaitable(rt):
      rt = run_until_complete(try_await(rt))

    if logger.level>=logging.DEBUG:
      #logger.debug(f'===Out <{type(rt).__name__}>',len(rt) if type(rt) in [bytes,str,dict,list,tuple] else rt)
      logger.debug(f"===Out <{type(rt).__name__}> {len(rt) if type(rt) in [bytes,str,dict,list,tuple] else rt}")

    if call_style==1: # list-in-list-out mode
        if call_id is None:
            return [rt] # 
        else:
            return [call_id,rt]
    else: return rt

# in some case, myeval() blocks, for example os.sleep(), try_asyncio_async can help
myevalasync = lambda *args,**kwargs:try_asyncio_async(lambda:myeval(*args,**kwargs))

# for server stdin quick-sheel mode ;)
def start_stdin(get_builtins):
  print('get_builtins()=',get_builtins())
  #for line in sys.stdin: print(myeval(line))
  loop = new_event_loop()
  for line in sys.stdin:
    if line.startswith(';'): # god mode (danger for no masking __builtins__)
      print(tryx(lambda:loop.run_until_complete(myevalasync(line[1:])) ))
    else: # craft mode
      try:
        r = loop.run_until_complete(myevalasync(line,{"__builtins__":get_builtins()},{}))
      except Exception as ex:
        r = ex
      print(type(r),r)

