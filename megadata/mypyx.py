# mypyx - more gist

from megadata.mypy import *

def sizeof(v):
    vv = v # todo fn/function
    size_code = None
    size_code_x = None
    getsizeof = sys.getsizeof
    # typeof = type(v)
    if isinstance(v,types.FunctionType): # user function
      size_code = getsizeof(v.__code__)
      size_code_x = getsizeof(dumps_func(v))
    elif callable(v): print('! non-user-func')
    size_vv = sys.getsizeof(vv)
    size_v = sys.getsizeof(v)
    return size_v,size_vv,size_code,size_code_x

sys_version_info = lambda fix_py2_utf8=False:{'version_info':s2o(o2s(sys.version_info))}

#if __name__!='__main__':
#    # make module callable as class
#    import sys
#    sys.modules[__name__] = __class__
#else:
#    print(__name__)

# control call frequency/rate less than freq_count/freq_time
class freqq:
    def __init__(self, init_q=[],freq_count=500, freq_time=60):
        self.freq_count = freq_count
        self.freq_time = freq_time
        self.q = []
        self.qd = [] 
        for v in init_q: self.do_enq(v)
    def do_deq(self):
        while tryx(lambda: self.qd.pop() if now()-self.qd[0]>=self.freq_time else None,False):
            #log1('.');flush1()
            pass
        if len(self.qd)<self.freq_count:
            #rt = tryx(lambda:self.q.pop(),False)
            rt = tryx(self.q.pop,False)
            if rt: self.qd.append(now())
            return rt
    def do_enq(self,param,deq=False):
        self.q.append(param)
        if deq: return self.do_deq()
    def process(self,thefunc):
        while True:
            len_myq_q = len(self.q)
            len_myq_qd = len(self.qd)
            while True:
                data = self.do_deq()
                if data is None: break
                #print(len_myq_q,len_myq_qd,data)

                try_async(lambda:thefunc(data))
            if len_myq_qd<=0 and len_myq_q<=0: break
            sleep(0.1)

class dict1(dict):# dict[]
    def __getitem__(self,k): return self.get(k)

class dict2(dict):# dict[][]
    def __getitem__(self,k):
        v = self.get(k)
        if v is None: self[k] = v = dict1()
        return v

import numpy as np

pctlog2=lambda df,e=0.0001:np.log2(df.where(df>e).pct_change().replace(np.nan,0)+1)
pctloge=lambda df,e=0.0001:np.log(df.where(df>e).pct_change().replace(np.nan,0)+1)

def tiny_email(user, mypass, sender, receiver, Subject, html, smtp_host='smtp.qq.com', smtp_port=465, Cc='', Bcc='',attachment_data=None,attachment_name=None):
    import smtplib
    from email.mime.text import MIMEText
    if attachment_name and attachment_data:
      from email.mime.multipart import MIMEMultipart
      msg=MIMEMultipart('mixed')
      att=MIMEText(attachment_data,'base64','utf-8')
      att['Content-Type']='application/octet-stream'
      att['Content-Disposition']='attachement; filename='+attachment_name
      msg.attach(att)
    else:
      msg=MIMEText(html,'html','utf-8')
    msg['From'] = sender
    if type(receiver) is str:
        receiver_a = [receiver,]
        receiver_s = receiver
    else:#iterable
        receiver_a = receiver
        receiver_s = ';'.join([str(v) for v in receiver])
    msg['To'] = receiver_s
    msg['Subject']= Subject
    msg['Cc'] = Cc
    msg['Bcc'] = Bcc
    receiver_a += [Cc,Bcc]

    server=smtplib.SMTP_SSL(smtp_host, smtp_port) 
    server.login(user, mypass)
    server.sendmail(sender, receiver_a, msg.as_string())
    server.quit()

###################################### dba wrapper (using sqlalchemy)
#'{scheme}://{user}:{password}@{host}:{port}/{db}?charset={charset}#{fragment}'
#'{scheme}://{netloc}@{host}:{port}/{path}?{query}#{fragment}'
#e.g.'mysql://root:123456@127.0.0.1:3306/?charset=utf8mb4'

class dba:
    _ = {'_':now()}
    def __init__(self,*args,**kwargs):
        self.hash = _hash = hash(self)
        dba._[_hash]={}
        try:
            from urllib.parse import quote_plus,urlparse

            password = kwargs.get('password')
            if password: kwargs['password'] = quote_plus(password)

            dbstr = kwargs.get('dbstr')

            dbstr_file = kwargs.get('dbstr_file')
            if dbstr_file: dbstr = read(dbstr_file).strip()

            if not dbstr:
                if len(args)>0:
                    args0 = args[0]
                    if '://' in args0: dbstr = args0
                    else:
                        dbstr_file = args0
                        dbstr = read(dbstr_file).strip()
            if dbstr:
                dbstr = dbstr.format(**kwargs)
                parsed = urlparse(dbstr)
                scheme = parsed.scheme
            else:
                scheme = kwargs.get('scheme')
            self.scheme = scheme
            debug = kwargs.get('debug')
            if debug:
                print('kwargs=',kwargs)
                print('dbstr=',dbstr)
                dba._[_hash]['dbstr']=dbstr
            from sqlalchemy import create_engine
            self.engine = create_engine(dbstr)
        except Exception as ex:
            print('ex=',ex)

    def __del__(self): dba._.pop(self.hash, None)

    def df(self,sql):
        from pandas import read_sql
        return read_sql(sql,self.engine)

    def yielder(self,sql):
        with self.engine.connect() as conn:
            conn = conn.execution_options(stream_results=True)
            for row in conn.execute(sql): yield row


def get_cmdline_args_kwargs():
  #import argparse
  #parser = argparse.ArgumentParser()
  from argparse import ArgumentParser
  parser = ArgumentParser()

  # first round (TODO, simplify logic later...)
  parsed, unknown = parser.parse_known_args() # this is an 'internal' method
  rt_args = []
  for arg in unknown:
      if arg.startswith(("-", "--")):
          parser.add_argument(arg.split('=')[0], type=str)
      else:
          rt_args.append(arg)
  # again to get the parsed
  parsed, unknown = parser.parse_known_args()
  rt_kwargs = parsed.__dict__
  return rt_args, rt_kwargs

