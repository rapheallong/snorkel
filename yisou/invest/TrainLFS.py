import os

# TO USE A DATABASE OTHER THAN SQLITE, USE THIS LINE
# Note that this is necessary for parallel execution amongst other things...
# os.environ['SNORKELDB'] = 'postgres:///snorkel-intro'
import yisou.Env_variable
import re
import numpy as np
from yisou.invest.LFS import *
from yisou.invest.LFS import LFS
from snorkel import SnorkelSession
from snorkel.learning import GenerativeModel
from snorkel.annotations import LabelAnnotator
from snorkel.lf_helpers import (
    get_left_tokens, get_right_tokens, get_between_tokens,
    get_text_between, get_tagged_text,
)
from snorkel.lf_helpers import test_LF
import matplotlib.pyplot as plt
from snorkel.annotations import save_marginals
from snorkel.models import Document, Sentence, candidate_subclass
import sys
reload(sys)
sys.setdefaultencoding('utf8')

session = SnorkelSession()

invest = candidate_subclass('invest', ['company1', 'company2'])
train_cands = session.query(invest).filter(invest.split == 1).all()
cds = [(a,b) for a,b in train_cands]


labeler = LabelAnnotator(lfs=LFS)
L_train = labeler.apply(split=1)
L_train = labeler.load_matrix(session, split=1)

gen_model=GenerativeModel()
gen_model.train(L_train, epochs=100, decay=0.95, step_size=0.1 / L_train.shape[0], reg_param=1e-6)
gen_model.learned_lf_stats()
train_marginals = gen_model.marginals(L_train)

c= zip(train_marginals,cds)
for x in c:
    if(x[0]>0.35):
        print x[1][0].sentence.text
        print x[0],str(x[1][0].get_span()),str(x[1][1].get_span())



plt.hist(train_marginals, bins=20)
plt.show()

# tp, fp, tn, fn = gen_model.error_analysis(session, L_dev, L_gold_dev)
save_marginals(session, L_train, train_marginals)