import sys,os
#print('sys.path',sys.path)

sys.path.insert(0, '..')

path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)

#print("__package__",__package__)
#print("__file__",__file__)

print('sys.path',sys.path)

import megadata
print('megadata.load_time=',megadata.load_time)
print('megadata.module_version=',megadata.module_version)

