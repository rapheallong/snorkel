#encoding=utf-8
import os

# TO USE A DATABASE OTHER THAN SQLITE, USE THIS LINE
# Note that this is necessary for parallel execution amongst other things...
# os.environ['SNORKELDB'] = 'postgres:///snorkel-intro'
from snorkel.models import Document, Sentence, candidate_subclass
from snorkel import SnorkelSession
from snorkel.annotations import load_marginals
from snorkel.learning.disc_models.rnn import reRNN


session = SnorkelSession()
train_marginals = load_marginals(session, split=0)

invest = candidate_subclass('invset', ['company1', 'company2'])
train_cands = session.query(invest).filter(invest.split == 0).order_by(invest.id).all()
dev_cands   = session.query(invest).filter(invest.split == 1).order_by(invest.id).all()
test_cands  = session.query(invest).filter(invest.split == 2).order_by(invest.id).all()
from snorkel.annotations import load_gold_labels
# TODO 这些我还没标记用来作evaluation
L_gold_dev  = load_gold_labels(session, annotator_name='gold', split=1)
L_gold_test = load_gold_labels(session, annotator_name='gold', split=2)
train_kwargs = {
    'lr':         0.01,
    'dim':        50,
    'n_epochs':   10,
    'dropout':    0.25,
    'print_freq': 1,
    'max_sentence_length': 100
}

lstm = reRNN(seed=1701, n_threads=None)
lstm.train(train_cands, train_marginals, X_dev=dev_cands, Y_dev=L_gold_dev, **train_kwargs)
p, r, f1 = lstm.score(test_cands, L_gold_test)
print("Prec: {0:.3f}, Recall: {1:.3f}, F1 Score: {2:.3f}".format(p, r, f1))

tp, fp, tn, fn = lstm.error_analysis(session, test_cands, L_gold_test)

lstm.save_marginals(session, test_cands)