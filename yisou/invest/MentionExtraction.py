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
docs = session.query(Sentence).limit(200)
invest = candidate_subclass('invest', ['company1', 'company2'])



ngrams = Ngrams(n_max=7)
# TODO  这个地方需要改
matcher = ORGMatcher(longest_match_only=True)
candExtrator = CandidateExtractor(invest, [ngrams, ngrams], [matcher, matcher])
candExtrator.apply(docs,split=0)
