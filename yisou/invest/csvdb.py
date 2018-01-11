#encoding=utf-8
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class csvdb():
    def __init__(self):
        self.data=df=pd.read_csv('/Users/yixinc-d/workspace/work2/snorkel/yisou/data/invest.csv')
    def exists(self,f,o):
        for i in self.data.index:
            dt=self.data.loc[i]
            fname = dt['fc_name']
            oname = dt['object_name']
            if((o in oname or oname in o) and (f in fname or fname in f)):
                return 1
            elif((f in oname or oname in f) and (o in fname or fname in o )):
                return 2
        return 0