import os
path= __file__
subpath='yisou/Env_variable.py'
idx = path.find(subpath)
os.environ['SNORKELHOME'] = path[:idx]
