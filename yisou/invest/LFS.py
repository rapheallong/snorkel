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

    bw=get_between_tokens(c)
    # print '\t'.join(bw)
    # if len(invest_verb1.intersection(get_between_tokens(c)))>0:
    #     print 'bw:---------------------->label true'
    #     return 1
    # elif len(invest_verb2.intersection(get_between_tokens(c)))>0:
    #     print 'bw:---------------------->label true'
    #     return 1
    #
    # else:
    #     print 'bw:lable false'
    #     return -1
    for w in bw:
        if('融资' in w or '投资' in w or '获得' in w):
            print 'bw:---------------------->label true'
            print a.sentence.text
            print a.get_span()
            print b.get_span()
            return 1
    # print 'bw:label false'
    return 0
def LF_right_words(c):
    rw = get_right_tokens(c)
    a=c[0]
    b=c[1]
    for w in rw:
        if('融资' in w):
            print 'rw:---------------------->label true'
            print a.sentence.text
            print a.get_span()
            print b.get_span()
            return 1
    # print 'rw:label false'
    return 0
# def LF_rgx(c):
#     a=c[0]
#     b=c[1]
#     str=a.sentence.text
#     if(re.search('.*投资.*',str) or ):
#         return 1
#     return -1
def LF_not(c):
    a=c[0]
    b=c[1]
    text=a.sentence.text
    if('投资' in text or '融资' in text):
        # print a.sentence.text
        # print a.get_span()
        # print b.get_span()
        return 0
    return -1
def LF_bw_2(c):
    a=c[0]
    b=c[1]
    bw=get_between_tokens(c)
    if(any('投资方为' in b for b in bw)):
        return 1
    return 0
def LF_not_company(c):
    a=c[0]
    b=c[1]
    if(len(a.get_span())<3 or len(b.get_span())<3 or '投资' in a.get_span() or '投资' in b.get_span() or a.get_span() in b.get_span() or b.get_span() in a.get_span()):
        return -1
    return 0
def LF_distant(c):
    '''
    远程监督方式
    :param c:
    :return:
    '''
    c1=c.company1.get_span()
    c2=c.company2.get_span()
    return cdb.exists(c1,c2)


LFS=[LF_between_words,LF_right_words,LF_bw_2,LF_not_company]