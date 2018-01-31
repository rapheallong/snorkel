import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
path= __file__
subpath='yisou/Env_variable.py'
idx = path.find(subpath)
os.environ['SNORKELHOME'] = path[:idx]
