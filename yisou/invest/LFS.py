#encoding=utf-8
import re
import pandas as pd
from snorkel.lf_helpers import (
    get_left_tokens, get_right_tokens, get_between_tokens,
    get_text_between, get_tagged_text,
)
import csvdb
LFS=[]
invest_verb1={'投资','斥资'}
invest_verb2={'融资'}
rgx1={r'.*投资.*'}
rgx2={r'.*获.*融资'}
relate_word=['美元']
cdb = csvdb()
def LF_between_words(c):
    '''
    1 a投资b
    2 a获得b的投资
    0 未识别
    :param c:
    :return:
    '''
    if len(invest_verb1.intersection(get_between_tokens(c)))>0:
        return 1
    elif len(invest_verb1.intersection(get_between_tokens(c)))>0:
        return 2
    else:
        return 0
def LF_left_words(c):
    return
def LF_regx(c):
    '''
    通过正则表达式
    :param c:
    :return:
    '''
    return
def LF_distant(c):
    '''
    远程监督方式
    :param c:
    :return:
    '''
    c1=c.company1.get_span()
    c2=c.company2.get_span()
    return cdb.exists(c1,c2)
