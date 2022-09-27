import sys,types,os
from mypy import dumps_func,_print,s2o,o2s
def sizeof(v):
    vv = v # todo fn/function
    size_code = None
    size_code_x = None
    getsizeof = sys.getsizeof
    # typeof = type(v)
    if isinstance(v,types.FunctionType): # user function
      size_code = getsizeof(v.__code__)
      size_code_x = getsizeof(dumps_func(v))
    elif callable(v):
      _print('non-user func')
    size_vv = sys.getsizeof(vv)
    size_v = sys.getsizeof(v)
    return size_v,size_vv,size_code,size_code_x

def sys_version_info(fix_py2_utf8=False):
    return {'version_info':s2o(o2s(sys.version_info))}

def mygc():
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
    import gc
    gc.collect()
    return len(gc.get_objects())

#file_exists = lambda f:os.path.exists(f)
file_exists = os.path.exists
touch_dir = lambda fn:os.makedirs(fn,exist_ok=True)
#def vers(): return dict([ (m,tryx(lambda:sys.modules[m].__version__,False)) for m in sys.modules])
#def vers():
#    import pip
#    #import pkg_resources
#    #return pkg_resources.get_distribution('construct').version
#    return [ pkg.key + ': ' + pkg.version for pkg in pip.get_installed_distributions()
#        if pkg.key in ['setuptools', 'statlib', 'construct'] ]

#if __name__!='__main__':
#    # make module callable as class
#    import sys
#    sys.modules[__name__] = __class__
#else:
#    print(__name__)

from time import time
from mypy import tryx
class freqq:
    def __init__(self, freq_count=500, freq_time=60, init_q=[]):
        self.freq_count = freq_count
        self.freq_time = freq_time
        self.q = []
        self.qd = [] 
        for v in init_q: self.do_enq(v)
    def do_deq(self):
        while tryx(lambda: self.qd.pop() if time()-self.qd[0]>=self.freq_time else None,False):
            pass
        #while len(self.qd)>0 and time()-self.qd[0]>=self.freq_time:
        #    print(time(),self.qd.pop())
        if len(self.qd)<self.freq_count:
            rt = tryx(lambda:self.q.pop(),False)
            if rt: self.qd.append(time())
            return rt
    def do_enq(self,param,deq=False):
        self.q.append(param)
        if deq: return self.do_deq()
    def process(self,thefunc):
        import threading
        from time import sleep
        while True:
            len_myq_q = len(self.q)
            len_myq_qd = len(self.qd)
            while True:
                data = self.do_deq()
                if data is None: break
                #print(len_myq_q,len_myq_qd,data)
                th = threading.Thread(target=lambda:thefunc(data))
                th.setDaemon(True)
                th.start()
            if len_myq_qd<=0 and len_myq_q<=0: break
            sleep(0.1)

import numpy as np

pctlog2=lambda df,e=0.0001:np.log2(df.where(df>e).pct_change().replace(np.nan,0)+1)
pctloge=lambda df,e=0.0001:np.log(df.where(df>e).pct_change().replace(np.nan,0)+1)

