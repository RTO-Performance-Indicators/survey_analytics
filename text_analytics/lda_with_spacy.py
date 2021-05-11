import pandas as pd
import numpy as np
import re

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
from spacy.matcher import Matcher, PhraseMatcher

# Load data
data = pd.read_csv('S:\\RTOPI\\Both Surveys\\All Final Datasets\\Datasets - 2020\\Output\\StudentSurveys.csv', encoding='ISO-8859-1')

# Get verbatims from survey data
verbatims = data[['s_rsn_dc_v', 's_rsn_rc_v', 's_imp_v']]
verbatims = verbatims.replace(np.NaN, '')

verbatims['verbatims_combined'] = verbatims['s_rsn_dc_v'] + verbatims['s_rsn_rc_v'] + verbatims['s_imp_v']
verbatims

len(verbatims)

test = verbatims[0:500]

nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_lg')

nlp.pipe_names

# Standard spacy method
# %%time
# docs = [nlp(text) for text in test['verbatims_combined']]

# nlp.pipe method (a bit faster)
# n_threads argument is deprecated in spacy v3, 
# but is kept for backwards compatibility.
# DO NOT USE n_threads AND batch_size ARGUMENTS
%%time
docs = list(nlp.pipe(test['verbatims_combined']))

for token in docs[1]:
    print(token.text, token.pos_)

for ent in docs[1]:
    print(ent.text)

# Initialise matcher
matcher = Matcher(nlp.vocab)

# Create pattern to match two tokens:
pattern = [
    {'TEXT': 'Victoria'},
    {'TEXT': 'University'}
]

# Add pattern to the matcher
matcher.add('RTO_PATTERN', [pattern])

matches = matcher(docs[1])
print("Matches:", [docs[1][start:end].text for match_id, start, end in matches])

# Alternatively, with phrase matcher
rtos = ['Victoria University', 'Swinburne University', 'Chisholm']
rto_patterns = list(nlp.pipe(rtos))

matcher = PhraseMatcher(nlp.vocab) # Initialise phrase matcher
matcher.add("RTO", rto_patterns, on_match=matcher) # add to phrase matcher

# Define custom component to add to pipeline
def rto_component(doc):
    # Apply matcher to doc
    matches = matcher(doc)
    # Create span for each match and assign label
    spans = [Span(doc, start, end, label='RTO') for match_id, start, end in matches]
    # Overwrite doc.ents with the matched spans
    doc.ents = spans
    return doc

# Add component to the pipeline after the NER component
# @Language.component('rto_component')
    nlp.add_pipe(rto_component, after='ner')

