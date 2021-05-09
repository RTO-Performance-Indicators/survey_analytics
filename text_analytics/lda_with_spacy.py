import pandas as pd
import numpy as np
import re

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
import contextualSpellCheck

from joblib import Parallel, delayed

# https://prrao87.github.io/blog/spacy/nlp/performance/2020/05/02/spacy-multiprocess.html#Option-3:-Parallelize-the-work-using-joblib
def chunker(iterable, total_length, chunksize):
    return (iterable[pos: pos + chunksize] for pos in range(0, total_length, chunksize))

def flatten(list_of_lists):
    # Flatten a list of lists to a combined list
    return [item for sublist in list_of_lists for item in sublist]

def process_chunk(texts):
    preproc_pipe = []
    # for doc in nlp.pipe(texts, batch_size=20):
    #     preproc_pipe.append(lemmatize_pipe(doc))
    for text in texts:
        preproc_pipe.append(nlp.pipe(texts, batch_size=20))
    return preproc_pipe

def preprocess_parallel(texts, chunksize=100):
    executor = Parallel(n_jobs=7, backend='multiprocessing', prefer="processes")
    do = delayed(process_chunk)
    tasks = (do(chunk) for chunk in chunker(texts, len(texts), chunksize=chunksize))
    result = executor(tasks)
    return flatten(result)

# Load data
data = pd.read_csv('S:\\RTOPI\\Both Surveys\\All Final Datasets\\Datasets - 2020\\Output\\StudentSurveys.csv', encoding='ISO-8859-1')

# Get verbatims from survey data
verbatims = data[['s_rsn_dc_v', 's_rsn_rc_v', 's_imp_v']]
verbatims = verbatims.replace(np.NaN, '')

verbatims['verbatims_combined'] = verbatims['s_rsn_dc_v'] + verbatims['s_rsn_rc_v'] + verbatims['s_imp_v']
verbatims

test = verbatims[0:100]

# Run pipeline
# nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg') # English, web-based library, large

# Add contextualSpellCheck to end of pipeline
contextualSpellCheck.add_to_pipe(nlp)
nlp.pipe_names

def pos(df, required_tags):
    pos_list = []
    for i in range(df.shape[0]):
        doc = nlp(df['verbatims_combined'][i])
        pos_dict = {}
        for token in doc:
            pos = token.pos_
            if pos in required_tags:
                pos_dict.setdefault(pos, 0)
                pos_dict[pos] = pos_dict[pos] + 1
        pos_list.append(pos_dict)
    return pd.DataFrame(pos_list)

required_tags = ['NOUN', 'ADJ', 'VERB']
test = pos(verbatims, required_tags=required_tags)

%%time
test['preproc_parallel'] = preprocess_parallel(test['verbatims_combined'], chunksize=10)

