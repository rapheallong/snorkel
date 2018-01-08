import os

# TO USE A DATABASE OTHER THAN SQLITE, USE THIS LINE
# Note that this is necessary for parallel execution amongst other things...
# os.environ['SNORKELDB'] = 'postgres:///snorkel-intro'

import numpy as np
from .LFS import *
from .LFS import LFS
from snorkel import SnorkelSession
from snorkel.annotations import LabelAnnotator
session = SnorkelSession()

from snorkel.models import Document, Sentence, candidate_subclass

invest = candidate_subclass('invset', ['company1', 'company2'])
labeler = LabelAnnotator(lfs=LFS)
