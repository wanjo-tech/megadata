from .mypy import *

# like Application.diff_o2o upgrade version... TODO merge then future?
# NOTES: return True if Same else False; 'a' for quick debug stack

def is_same(o1,o2,a=None,p='',ignore_na=False):
  rt = True
  if type(o1)!=type(o2):
    if a is not None: a.append(f'{p}: {o1}=>{o2}')
    rt = False
    if ignore_na and o2 in [None,0,0.,'0','0.']: rt=True # TODO np.nan...
  elif type(o1) in [ list, tuple, set ]:
    list1 = list(o1)
    list2 = list(o2)
    len1 = len(list1)
    len2 = len(list2)
    if len1!=len2:
      if a is not None: a.append(f'{p}: {list1}=>{list2}')
      rt = False
    else:
      for i in range(len2):
        if not is_same(list1[i],list2[i],a,f'{p}/{i}',ignore_na=ignore_na):
          rt = False
          break
    #for k in o1:
    #  if k not in o2:
    #    if a is not None: a.append(f'{p}: {k}=>None')
    #    rt = False
    #    break
    #if rt is True:
    #  for k in o2:
    #    if k not in o1:
    #      if a is not None: a.append(f'{p}: None=>{k}')
    #      rt = False
    #      break
  elif type(o1) in [ dict ]:
    for k in o1:
      v1 = tryx(lambda:o1[k],False)
      v2 = tryx(lambda:o2[k],False)

      #if False == is_same(v1, v2, a, f'{p}/{k}',ignore_na=ignore_na):
      #    rt = False
      #    #break
      #    if a is not None: break

      dff = is_same(v1, v2, a, f'{p}/{k}', ignore_na=ignore_na)
      if dff==False: rt = False
    if rt or a is not None:
    #if True:
        for k in o2:
          if k in o1: continue
          v1 = tryx(lambda:o1[k],False)
          v2 = tryx(lambda:o2[k],False)
          if False == is_same(v1, v2, a, f'{p}/{k}',ignore_na=ignore_na):
              rt = False
              #break
              #if a is not None: break
              if a is None: break
  elif o1==o2: # not ===, so should already handled the epsilon...
    pass
  else:                       # TODO more type ...
    rt = False
    if a is not None:
      a.append(f'{p}: {o1}=>{o2}')
    if ignore_na and o2 in [None,0,0.,'0','0.']: rt=True # TODO np.nan...
  return rt

load_time = now()

from diskcache import Cache

# key list only...
def kv_list(pool,lmt=0,pagesize=99999,folder='../tmp'):
  lmt=int(lmt) # Last-Modified-Time
  pagesize=int(pagesize)
  if pagesize > 99999: pagesize = 99999
  def _with(cache):
    c=0
    if lmt>0: # TMP 
      #it = [cache._disk.get(k,r) for k,r in cache._sql("select key,raw from cache where key > ? ORDER BY key LIMIT ?",[lmt,pagesize]).fetchall()]
      it = [k[0] for k in cache._sql("select key from cache where key > ? ORDER BY key LIMIT ?",[lmt,pagesize]).fetchall()]
    else:
      #it = [cache._disk.get(k,r) for k,r in cache._sql("select key,raw from cache ORDER BY key LIMIT ?",[pagesize]).fetchall()]
      it = [k[0] for k in cache._sql("select key from cache ORDER BY key LIMIT ?",[pagesize]).fetchall()]
    rt = []
    if it is not None:
      for k in it:
        rt.append(k)
        c+=1
        if c>pagesize: break
    return rt
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:_with(cache))

def kv_last(pool,folder='../tmp'):
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:cache._sql("select key from cache ORDER BY key DESC LIMIT 1").fetchall()[0][0],False)

def kv_len(pool,folder='../tmp'):
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:cache._sql("select count() from cache").fetchall())

#def kv_data_lmt_old(pool,lmt=0,pagesize=99999,folder='../tmp',cache=None):
#  pagesize=int(pagesize)
#  if pagesize > 99999: pagesize = 99999
#  def _with(cache):
#    c=0
#    rt = []
#    # TODO fix better codes here later
#    if lmt: # TMP 
#      it = [(cache._disk.get(k,r),l) for k,r,l in cache._sql("select key,raw,store_time from cache where store_time > ? ORDER BY key LIMIT ?",[lmt,pagesize]).fetchall()]
#    else:
#      it = [(cache._disk.get(k,r),l) for k,r,l in cache._sql("select key,raw,store_time from cache ORDER BY key LIMIT ?",[pagesize]).fetchall()]
#    if it is not None:
#      for k,l in it:
#        v = cache.get(k)
#        rt.append((k,v,l))
#        c+=1
#        if c>pagesize: break
#    return rt
#
#  if cache:
#    return tryx(lambda:_with(cache))
#  with Cache(f'{folder}/{pool}') as cache:
#    return tryx(lambda:_with(cache))

# filter key only
def kv_key_lmt(pool,lmt=0,pagesize=99999,folder='../tmp',cache=None):
  lmt=float(lmt)
  pagesize=int(pagesize)
  if pagesize > 99999: pagesize = 99999
  def _with(cache):
    return [(k,l) for k,l in cache._sql("select key,store_time from cache where store_time > ? ORDER BY store_time LIMIT ?",[lmt,pagesize]).fetchall()]
  if cache:
    return tryx(lambda:_with(cache))
  cache = Cache(f'{folder}/{pool}')
  return tryx(lambda:_with(cache))

# using 'store_time' as filter... returns [(k,v,l),]
def kv_data_lmt(pool,lmt=0,pagesize=99999,folder='../tmp',cache=None):
  lmt=float(lmt)
  pagesize=int(pagesize)
  if pagesize > 99999: pagesize = 99999
  def _with(cache):
    loads = cache.get
    return [(k,loads(k,r),l) for k,l,r in cache._sql("select key,store_time,raw from cache where store_time > ? ORDER BY store_time LIMIT ?",[lmt,pagesize]).fetchall()]

  if cache:
    return tryx(lambda:_with(cache))
  cache = Cache(f'{folder}/{pool}')
  return tryx(lambda:_with(cache))

# see also kv_data_lmt()
def kv_data(pool,lmt=0,pagesize=99999,folder='../tmp'):
  pagesize=int(pagesize)
  if pagesize > 99999: pagesize = 99999
  def _with(cache):
    c=0
    rt = []
    it = [cache._disk.get(k,r) for k,r in cache._sql("select key,raw from cache ORDER BY key LIMIT ?",[pagesize]).fetchall()]
    if it is not None:
      for k in it:
        v = cache.get(k)
        rt.append((k,v))
        c+=1
        if c>pagesize: break
    return rt
  cache = Cache(f'{folder}/{pool}')
  return tryx(lambda:_with(cache))

def kv_set(pool,k,v,expire=None,folder='../tmp',diff=False,debug=False):
  def _with(cache):
    a = [] if debug else None
    if diff and is_same(cache.get(k),v,a): return 0
    if debug: print('kv_set',a)
    cache.set(str(k),v,expire=expire)
    return 1
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:_with(cache))

def kv_set_batch(pool,batch_o,expire=None,folder='../tmp',diff=False,debug=False,ignore_na=False):

  def _with(cache):
    a = [] if debug else None
    c = 0
    items = list(batch_o.items())
    for k,v in items:
      if diff and is_same(cache.get(k),v,a,ignore_na=ignore_na): continue
      if debug: print('kv_set_batch',a)
      c += 1
      cache.set(str(k),v,expire=expire)
    return c
    
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:_with(cache))

def kv_get(pool,k,folder='../tmp'):
  #with Cache(f'{folder}/{pool}') as cache:
  cache = Cache(f'{folder}/{pool}')
  if True:
    return tryx(lambda:cache.get(str(k)),False)

def kv_get_kvl(pool,k,folder='../tmp'):
  #with Cache(f'{folder}/{pool}') as cache:
  cache = Cache(f'{folder}/{pool}')
  if True:
    for kk,l,r in cache._sql("select key,store_time,raw from cache where key = ?",[k]):
      return k,cache.get(kk,r),l

def kv_del(pool,k,folder='../tmp'):
  with Cache(f'{folder}/{pool}') as cache:
    delx(cache,k)

def kv_move(pool, to_pool, k, folder='../tmp'):
  def _with(cache):
    v = tryx(lambda:cache[k],False)
    print('kv_move.v',v)
    if v is not None:
      kv_set(to_pool,k,v)
    delx(cache,k)
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:_with(cache))

# upsert single item only. for update multiple items, see kv_set_batch()
def kv_upsert(pool,kv_k,kv_o,folder='../tmp',debug=False):
  def _with(cache):
    v_o = tryx(lambda:cache.get(kv_k)) or {}
    c = 0
    for key,val in kv_o.items():
      old_v = v_o.get(key)
      if val is None:
        if old_v is not None:
          c+=1
          #del v_o[key]
          tryx(lambda:delx(v_o,key),False)
          if debug: print(kv_k,key,old_v,'deleted')
      else:
        if not is_same(old_v,val):
          c+=1
          v_o[key] = val
          if debug: print(kv_k,key,old_v,'=>',val)
    if c>0: cache.set(str(kv_k),v_o)
    return c
  with Cache(f'{folder}/{pool}') as cache:
    return tryx(lambda:_with(cache))

# del all under lmt; for quicker cleanup speed, useful in memfs
def kv_del_lmt(pool,lmt,pagesize=99999,folder='../tmp',cache=None):
  lmt=float(lmt)
  pagesize=int(pagesize)
  if pagesize > 99999: pagesize = 99999
  def _with(cache):
    c = 0
    for k,l in cache._sql("select key,store_time from cache where store_time < ? LIMIT ?",[lmt,pagesize]).fetchall():
      delx(cache,k)
      c+=1
    return c
  if cache:
    return tryx(lambda:_with(cache))
  cache = Cache(f'{folder}/{pool}')
  return tryx(lambda:_with(cache))

#class kvstore(objx):# TODO
class kvstore():
  # the address for remote store is TODO again
  def __init__(self,pool,folder='../tmp',address=None):
    self.pool = pool
    self.folder = folder

  def __setitem__(self,k,v):
    return kv_set(self.pool,k,v,folder=self.folder)

  def __getitem__(self,k):
    return tryx(lambda:kv_get(self.pool,k,folder=self.folder))

  def __delitem__(self,k):
    return tryx(lambda:kv_del(self.pool,k,folder=self.folder))

  def kv_list(self,lmt=0):# keys()
    return kv_list(self.pool,folder=self.folder)

  def kv_data(self,lmt=0):# items()
    return kv_data(self.pool,lmt,folder=self.folder)

  def kv_key_lmt(self,lmt=0):
    return kv_key_lmt(self.pool,lmt,folder=self.folder)

  def kv_data_lmt(self,lmt=0):
    return kv_data_lmt(self.pool,lmt,folder=self.folder)

  def kv_del_lmt(self,lmt):
    return kv_del_lmt(self.pool,lmt,folder=self.folder)

  def kv_get_kvl(self,k):
    return kv_get_kvl(self.pool,k,folder=self.folder)

  def kv_move(self,to_pool,k):
    return kv_move(self.pool,to_pool,k,folder=self.folder)

  def kv_upsert(self,k,v):
    return kv_upsert(self.pool,k,v,folder=self.folder)

  def kv_set_batch(self,o,diff=False):
    return kv_set_batch(self.pool,o,diff=diff,folder=self.folder)

  def __repr__(self):
    return str(self.kv_list())

  # for len()
  def __len__(self):
    return len(self.kv_list())


