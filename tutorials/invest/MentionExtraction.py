# encoding=utf-8
import os
import numpy as np
from snorkel import SnorkelSession
from snorkel.parser import CorpusParser
from .nlp.YisouParser import LTPParser
from snorkel.candidates import Ngrams, CandidateExtractor
from .nlp.YisouMatcher import ORGMatcher

os.environ['SNORKELHOME'] = '/home/lx/longxiao/workspace/knowledgegraph/snorkel/snorkel'
from snorkel import SnorkelSession

session = SnorkelSession()
# load docs
from .parser.Preprocessors import CSVDocPreprocessor

# TODO 待处理的文本
docs = CSVDocPreprocessor('/home/lx/longxiao/workspace/knowledgegraph/CNdeepdive/transaction/input/articles.csv')

# TODO needs specify the parser
corpusParser = CorpusParser(parser=LTPParser())
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
