import pandas as pd
import numpy as np
import re

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
import contextualSpellCheck

# Load data
data = pd.read_csv('S:\\RTOPI\\Both Surveys\\All Final Datasets\\Datasets - 2020\\Output\\StudentSurveys.csv', encoding='ISO-8859-1')

# Get verbatims from survey data
verbatims = data[['s_rsn_dc_v', 's_rsn_rc_v', 's_imp_v']]
verbatims = verbatims.replace(np.NaN, '')

verbatims['verbatims_combined'] = verbatims['s_rsn_dc_v'] + verbatims['s_rsn_rc_v'] + verbatims['s_imp_v']
verbatims

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