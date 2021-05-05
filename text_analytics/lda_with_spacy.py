import pandas as pd
import re

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
import contextualSpellCheck

# nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg') # English, web-based library, large

# Add contextualSpellCheck to end of pipeline
contextualSpellCheck.add_to_pipe(nlp)

nlp.pipe_names

# Disable unnecesary pipes

# Load data
data = pd.read_csv('S:\\RTOPI\\Both Surveys\\All Final Datasets\\Datasets - 2020\\Output\\StudentSurveys.csv', encoding='ISO-8859-1')

# Get verbatims from survey data
verbatims = data[['s_rsn_dc_v', 's_rsn_rc_v', 's_imp_v']]
verbatims = verbatims.replace(np.NaN, '')

verbatims['verbatims_combined'] = verbatims['s_rsn_dc_v'] + verbatims['s_rsn_rc_v'] + verbatims['s_imp_v']
verbatims

test = verbatims[verbatims['verbatims_combined'] != '']
test

# Run pipeline
docs = list(nlp.pipe(test['verbatims_combined'])) # This automatically batches the texts
