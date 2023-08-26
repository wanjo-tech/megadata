# example api

from megadata.mypy import tryx,objx,now,sleep
load_time = now()

class api(objx):

  def ping(self, ping=None):
      dff_time = None
      now_time = int(now())
      if ping:
        dff_time = now_time - int(float(ping))
      return now_time,round(load_time),dff_time

  async def pingx(self, ping=None):
      dff_time = None
      now_time = int(now())
      if ping:
        dff_time = now_time - int(float(ping))
      print('pingx')
      return now_time,round(load_time),dff_time

  def sleep(self,t=None):
      tt = min(int(t or 1),60)
      sleep(tt)
      return tt

  async def sleepx(self,t=None):
      tt = min(int(t or 1),60)
      sleep(tt)
      return tt

  async def errx1(self, ping=None):
      print('before assert')
      assert False, 'error test errx1'
      print('after assert')
      return 1

  def reload(self, mdl=__name__):

    if type(self.param) is dict:
      mdl_param = self.param.get('mdl')
      if mdl_param is not None:
        print('mdl_param=',mdl_param)
        mdl = mdl_param

    return refresh(mdl).load_time


