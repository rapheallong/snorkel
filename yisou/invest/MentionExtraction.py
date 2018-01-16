# encoding=utf-8
import os
import numpy as np
from snorkel import SnorkelSession
from snorkel.parser import CorpusParser
from yisou.invest.nlp.YisouParser import JiebaParser
from snorkel.candidates import Ngrams, CandidateExtractor
from yisou.invest.nlp.YisouMatcher import ORGMatcher

os.environ['SNORKELHOME'] = '/home/lx/longxiao/workspace/work1/snorkel/snorkel'
from snorkel import SnorkelSession

session = SnorkelSession()
# load docs
from snorkel.parser import TextDocPreprocessor

# TODO 待处理的文本
docs = TextDocPreprocessor('/home/lx/longxiao/workspace/work1/snorkel/yisou/data/news')

# TODO needs specify the parser
corpusParser = CorpusParser(parser=JiebaParser())
# 文本已经作好解析
corpusParser.apply(docs)

from snorkel.models import Document, Sentence

print("Documents:", session.query(Document).count())
print("Sentences:", session.query(Sentence).count())

# 下面开始提取mention
from snorkel.models import Document, Sentence, candidate_subclass

invest = candidate_subclass('invset', ['company1', 'company2'])



ngrams = Ngrams(n_max=7)
# TODO  这个地方需要改
matcher = ORGMatcher(longest_match_only=True)
candExtrator = CandidateExtractor(invest, [ngrams, ngrams], [matcher, matcher])
candExtrator.apply()
