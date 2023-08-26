import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)

import testmodule

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建控制台处理程序
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

#formatter = logging.Formatter(log_format)
#console_handler.setFormatter(formatter)
#logger.addHandler(console_handler)

#file_handler = logging.FileHandler('app.log')
#file_handler.setLevel(logging.ERROR)
#file_handler.setFormatter(formatter)
#logger.addHandler(file_handler)

logger.info('程序开始执行')
from megadata.myeval import myeval,logger as sublogger
sublogger.setLevel(logging.DEBUG)
rst = myeval('(2**3)')
print('rst',rst)

#from testmodule import do_something
#do_something()
#testmodule.do_something()
logger.info('程序执行完毕')

