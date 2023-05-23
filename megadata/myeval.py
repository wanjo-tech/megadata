# eval tool by wanjo 20230511
from .mypy import *
load_time = now()

# TODO:
# loadapi(c,m,request=request)(*args,**kwargs)
# fix lambda:__builtins__ bug??

# old way, deprecated, will remove soon
def fwd(c,m,param_a): return tryx(lambda:getattr(sys_import(c).api(param_a),m)(*param_a),lambda ex:{'errmsg':str(ex)})

# working version but not yet support server objects
def fwdapi(c,m,*args,**kwargs):
  rt = tryx(lambda:getattr(sys_import(f'api{c}').api(),m)(*args,**kwargs),lambda ex:{'errmsg':str(ex)})
  #print('DEBUG fwdapi',[c,m,args],'=>',rt)
  return rt

def myeval(s,g={},l={},debug=False):
    rt = None

    if type(s) is bytes: # try pickle/loads_func/...
        import pickle
        # try pickle...
        o = tryx(lambda:pickle.loads(s),False)
        if o is None: # not pickle, try bytes str
            o = tryx(lambda:s.decode(),False)
        if o is None: # try rpc function...
            o = tryx(lambda:loads_func(s,g)) # load by ctx g
            if o is not None:
              return tryx(o,True)
        s = o

    s = f'{s}'.strip()
    if len(s)<1: return None
    a = s2o(s)
    if debug: print(f'===In: {a or s}')
    #flg_right = False
    call_id = None
    call_param = None
    call_style = None
    #if type(a) is list: # list-come-list-go

    if s[0]=='[':
        # list mode w+/- call_id
        # [ call_id:Optional, call_entry, [call_param...] ]
        # => [call_param, call_result]

        call_style = 1
        len_a = len(a)
        a0i = tryx(lambda:int(a[0]),False)
        if len_a>1 and type(a0i) is int:
            call_entry = a[1]
            call_param = tryx(lambda:a[2:],False)
            call_id = a[0]
            #flg_right = True
        elif len_a>0:
            call_entry = a[0]
            call_param = tryx(lambda:a[1:],False)
            #flg_right = True

    elif s[0]=='(' or s[0]=='/': # pyql ;)
        s=s.replace('__builtins__','') # safe-guard ;)
        if s[0]=='/': s = s[1:]
        #return str(tryx(lambda:eval(s,g,l),True)) # DEBUG: testing no str...
        #return tryx(lambda:eval(s,g,l),True)
        rt = tryx(lambda:eval(s,g,l),True)
        #return rt

    # dict-come-dict-go, old and please try not to use...
    elif s[0]=='{':
        # deprecated ,dict mode is not good too
        call_style = 2
        call_entry = a.get('entry',None)
        call_param = a.get('param',[])
        call_id = a.get('id',None)
        #flg_right = True

    elif a is None: # assume: quick console mode sep by comma (not good for special case...)
        # deprecated, quick-console-mode is not good ;)
        call_style = 3
        #a = s.split('\t')
        s=s.replace('\t','')
        a = s.split(',') # not good for some quote case! for that should /api(...)
        len_a = len(a)
        a0i = tryx(lambda:int(a[0]),False)
        if len_a>1 and type(a0i) is int:
            call_style = 1 # rollback to list-mode
            call_entry = a[1]
            call_param = tryx(lambda:a[2:],False)
            call_id = a0i or a[0]
            #flg_right = True
        elif len_a>0:
            call_entry = a[0]
            call_param = tryx(lambda:a[1:],False)
            #flg_right = True

    #if flg_right:
    if rt is None:
        a = call_entry.split('.')
        if len(a)<2:
            rt = {'errmsg':'wrong entry {}'.format(call_entry)}
        else:
            # TODO remove fwd() and using fwdapi instead...
            # TMP fwd to api{c}.m(call_param)
            # TODO should using *args,**kwargs
            rt = fwd(f'api{a[0]}',a[1],call_param)
    else:
        rt = {'errmsg':'TODO'}

    if is_awaitable(rt): return rt

    if debug:print(f'===Out <{type(rt).__name__}>',len(rt) if type(rt) in [bytes,str,dict,list,tuple] else rt)

    if call_style==1: # list mode
        if call_id is None:
            return [rt] # 
        else:
            return [call_id,rt]
    else: return rt
    #elif call_style in [2,3]: # dict mode or quick console mode
    #    return rt
    #else:
    #    return None

#async def myevalasync(*args,**kwargs):
#  # return await try_await( await try_asyncio_async(lambda:myeval(*args,**kwargs)) )
#  rt = await try_asyncio_async(lambda:myeval(*args,**kwargs))
#  if is_awaitable(rt): rt = await rt
#  return rt
myevalasync = lambda *args,**kwargs:try_asyncio_async(lambda:myeval(*args,**kwargs))
