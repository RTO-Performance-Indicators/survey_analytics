import pandas as pd
import re

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
import contextualSpellCheck

from spellchecker import SpellChecker

# Load small trained pipeline that is used to predict POS tags and dependencies
# Can use en_core_web_lg for a larger trained pipeline
# nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_lg') # English, web-based library, large

# Add contextualSpellCheck to end of pipeline
contextualSpellCheck.add_to_pipe(nlp)

nlp.pipe_names

# Test data
data = pd.DataFrame({
    's_rsn_dc_v': [
        'Testing the spacy package', 
        'I was really unsatisfied with the poor quality of teachers', 
        'The teachers and trainors at Chisholm Institute were bulying the students',
        'This course was a waste of time! Teachers do not turn up on time, and students get bullied all the time',
        'Teachers are not professional.',
        'Admin did not help me re-enrol into the course',
        'Teachers were fantastic! The course helped me overcome my anxiety',
        'qualiry of teachhers is very poor',
        'THe assessments were inconsistent'
    ]
})

# Run pipeline:
# Create document object for each verbatim
data['doc'] = [nlp(text) for text in data['s_rsn_dc_v']]

# Number of tokens in each doc
data['n_tokens'] = [len(tokens) for tokens in data['doc']]

# Sentences per doc
data['n_sentences'] = [len(list(doc.sents)) for doc in data['doc']]

data

# Part of Speech (POS) tags (already identified in nlp function above)
for token in data['doc'][1]:
    print(token.text, token.pos_)

# Lemma
for token in data['doc'][1]:
    print(token.text, token.lemma_)

# Is stop word
for token in data['doc'][1]:
    print(token.text, token.is_stop)

# Named entities
for ent in data['doc'][2].ents:
    print(ent.text, ent.label_)


# Fixing Spelling errors
nlp = spacy.load('en_core_web_lg')
contextualSpellCheck.add_to_pipe(nlp)
text = 'The qualiry of teachhers and trainors at Chisholm Institute were bulying the students'
doc = nlp(text)

print(doc._.performed_spellCheck)
print(doc._.outcome_spellCheck)
print(doc._.suggestions_spellCheck) # 'bulying' suggested 'among'
print(doc._.score_spellCheck) # Suggestion for 'bulying' doesn't even include bullying!

# get spelling-corrected tokens
def corrected_token(token):
    if token._.get_require_spellCheck:
        return(token._.get_suggestion_spellCheck)
    else:
        return(token.lemma_)

[corrected_token(token) for token in doc if token.pos_ == 'NOUN']

desired_pos = ['NOUN']
noun_list = []
for doc in data['doc']:
    nouns = [corrected_token(token) for token in doc if token.pos_ in desired_pos]
    noun_list.append(nouns)

data['nouns'] = noun_list
data

# Topic Modelling with gensim
# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

# For Gensim, spacy docs need to be converted into a list of lists
# doc_list = []
# for doc in data['s_rsn_dc_v']:
#     doc_strings = nlp(doc)
#     doc_list.append(doc_strings)

# doc_list

# Create dictionary and corpus
dictionary = corpora.Dictionary(data['nouns'])
corpus = [dictionary.doc2bow(noun) for noun in data['nouns']]
corpus

# Run LDA model
lda_model = gensim.models.ldamodel.LdaModel(
    corpus=corpus, 
    id2word=dictionary, 
    num_topics=3,
)

lda_model.print_topics()


# Topic Evaluation
# 1 - Observer Coherence measure
# 2 - Word Intrusion  detection

# Topic reliability/consistency