import os

# TO USE A DATABASE OTHER THAN SQLITE, USE THIS LINE
# Note that this is necessary for parallel execution amongst other things...
# os.environ['SNORKELDB'] = 'postgres:///snorkel-intro'
# os.environ['SNORKELDB'] = 'postgres:///snorkel-intro'
os.environ['SNORKELHOME']='/Users/yixinc-d/workspace/work2/snorkel'

from snorkel import SnorkelSession
session = SnorkelSession()

# Here, we just set how many documents we'll process for automatic testing- you can safely ignore this!
n_docs = 500 if 'CI' in os.environ else 2591

from snorkel.parser import TSVDocPreprocessor

doc_preprocessor = TSVDocPreprocessor('data/articles.tsv', max_docs=n_docs)

from snorkel.parser import CorpusParser

corpus_parser = CorpusParser()
corpus_parser.apply(doc_preprocessor, count=n_docs)


from snorkel.models import Document, Sentence

print("Documents:", session.query(Document).count())
print("Sentences:", session.query(Sentence).count())

from snorkel.models import candidate_subclass

Spouse = candidate_subclass('Spouse', ['person1', 'person2'])

from snorkel.candidates import Ngrams, CandidateExtractor
from snorkel.matchers import PersonMatcher

ngrams         = Ngrams(n_max=7)
person_matcher = PersonMatcher(longest_match_only=True)
cand_extractor = CandidateExtractor(Spouse, [ngrams, ngrams], [person_matcher, person_matcher])

from snorkel.models import Document
from util import number_of_people

docs = session.query(Document).order_by(Document.name).all()

train_sents = set()
dev_sents   = set()
test_sents  = set()

for i, doc in enumerate(docs):
    for s in doc.sentences:
        if number_of_people(s) <= 5:
            if i % 10 == 8:
                dev_sents.add(s)
            elif i % 10 == 9:
                test_sents.add(s)
            else:
                train_sents.add(s)

for i, sents in enumerate([train_sents, dev_sents, test_sents]):
    cand_extractor.apply(sents, split=i)
    print("Number of candidates:", session.query(Spouse).filter(Spouse.split == i).count())
from util import load_external_labels
missed = load_external_labels(session, Spouse, annotator_name='gold')

