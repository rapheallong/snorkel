# encoding=utf-8
import os
import numpy as np
from snorkel import SnorkelSession
from snorkel.parser import CorpusParser
from yisou.invest.nlp.YisouParser import JiebaParser
from snorkel.candidates import Ngrams, CandidateExtractor
from yisou.invest.nlp.YisouMatcher import ORGMatcher
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  yisou.Env_variable
from snorkel import SnorkelSession

session = SnorkelSession()


# 下面开始提取mention
from snorkel.models import Document, Sentence, candidate_subclass
docs = session.query(Sentence).all()
invest = candidate_subclass('invest', ['company1', 'company2'])
trainset=set()
devset=set()
testset=set()
for i, s in enumerate(docs):
            if i % 10 == 8:
                devset.add(s)
            elif i % 10 == 9:
                testset.add(s)
            else:
                trainset.add(s)

ngrams = Ngrams(n_max=7)
# TODO  这个地方需要改
matcher = ORGMatcher(longest_match_only=True)
candExtrator = CandidateExtractor(invest, [ngrams, ngrams], [matcher, matcher])

for i, sents in enumerate([trainset,devset, testset]):
    candExtrator.apply(sents,split=i)
    print("Number of candidates:", session.query(invest).filter(invest.split == i).count())
