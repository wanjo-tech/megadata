from megadata.mypy import tryx,objx,now
load_time = now()

class api(objx):

  def ping(self, ping=None):
      dff_time = None
      now_time = int(now())
      if ping:
        dff_time = now_time - int(float(ping))
      return now_time,round(load_time),dff_time

  def reload(self, mdl=__name__):

    if type(self.param) is dict:
      mdl_param = self.param.get('mdl')
      if mdl_param is not None:
        print('mdl_param=',mdl_param)
        mdl = mdl_param

    return refresh(mdl).load_time


