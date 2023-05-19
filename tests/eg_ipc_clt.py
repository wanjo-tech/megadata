print('python -m megadata ipc port host')

import sys

sys.path.insert(0,'..')
print('sys.path',sys.path)

from megadata.mypy import argv
from megadata.clt_ipc import clt_ipc

clt_ipc(argv)

