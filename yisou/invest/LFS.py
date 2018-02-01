#encoding=utf-8
import re
import pandas as pd
from snorkel.lf_helpers import (
    get_left_tokens, get_right_tokens, get_between_tokens,
    get_text_between, get_tagged_text,
)
from csvdb import csvdb
invest_verb1={'投资','斥资'}
invest_verb2={'融资','领投'}
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
    a=c[0]
    b=c[1]
    # print a.sentence
    print a.get_span()
    print '\t'.join(get_between_tokens(c))
    if len(invest_verb1.intersection(get_between_tokens(c)))>0:
        print 'bw:---------------------->label true'
        return 1
    elif len(invest_verb2.intersection(get_between_tokens(c)))>0:
        print 'bw:---------------------->label true'
        return 1
    else:
        print 'bw:lable false'
        return -1
def LF_right_words(c):
    if len(invest_verb1.intersection(get_between_tokens(c)))>0:
        print 'rw:---------------------->label true'
        return 1
    elif len(invest_verb2.intersection(get_between_tokens(c)))>0:
        print 'rw:---------------------->label true'
        return 1
    else:
        print 'rw:label false'
        return -1
def LF_distant(c):
    '''
    远程监督方式
    :param c:
    :return:
    '''
    c1=c.company1.get_span()
    c2=c.company2.get_span()
    print 'distant: label true'
    return cdb.exists(c1,c2)


LFS=[LF_between_words,LF_distant,LF_right_words]
