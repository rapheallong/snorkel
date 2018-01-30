# encoding=utf-8
import os
import numpy as np
from snorkel import SnorkelSession
from snorkel.parser import CorpusParser
from yisou.invest.nlp.YisouParser import JiebaParser
from snorkel.candidates import Ngrams, CandidateExtractor
from yisou.invest.nlp.YisouMatcher import ORGMatcher
from snorkel import SnorkelSession
import yisou.Env_variable
session = SnorkelSession()
# load docs
from snorkel.parser import TextDocPreprocessor

# TODO 待处理的文本
docs = TextDocPreprocessor('../data/news')

# TODO needs specify the parser
corpusParser = CorpusParser(parser=JiebaParser())
# 文本已经作好解析
corpusParser.apply(docs)

from snorkel.models import Document, Sentence

print("Documents:", session.query(Document).count())
print("Sentences:", session.query(Sentence).count())