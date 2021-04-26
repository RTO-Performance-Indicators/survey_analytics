import pandas as pd
import numpy as np

import hunspell

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
from spacy.language import Language
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

# Load small trained pipeline that is used to predict POS tags and dependencies
# Can use en_core_web_lg for a larger trained pipeline
# nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_lg')

# Test data
data = pd.DataFrame({
    'SurveyResponseID': [1, 2, 3, 4],
    's_rsn_dc_v': [
        'Testing the spacy package', 
        'I was really unsatisfied with the poor quality of teachers', 
        'The teachers and trainors at Chisholm Institute were bulying the students',
        'This course was a waste of time! Teachers do not turn up on time, and students get bullied all the time']
})

# Run pipeline:
# Create document object for each verbatim
data['doc'] = [nlp(text) for text in data['s_rsn_dc_v']]

# Number of tokens in each doc
data['n_tokens'] = [len(tokens) for tokens in data['doc']]
data


# Sentences per doc
list(data['doc'][3].sents)
for doc in data['doc']:
    print(len(list(doc.sents)))
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


# https://towardsdatascience.com/building-a-topic-modeling-pipeline-with-spacy-and-gensim-c5dc03ffc619

# Add a pipe to the pipeline to remove stop words
@Language.component('stopwords')
def component_func(doc):
    doc = [token.text for token in doc if token.is_stop != True]
    return(doc)

nlp.add_pipe('stopwords')

# For Gensim, spacy docs need to be converted into a list of lists
doc_list = []
for doc in data['s_rsn_dc_v']:
    doc_strings = nlp(doc)
    doc_list.append(doc_strings)

doc_list

words = corpora.Dictionary(doc_list)

# Turn each document into bag of words
corpus = [words.doc2bow(doc) for doc in doc_list]
corpus

# Run LDA model
lda_model = gensim.models.ldamodel.LdaModel(
    corpus=corpus, 
    id2word=words, 
    num_topics=2,
    random_state=2,
    update_every=1,
    passes=2,
    alpha='auto',
    per_word_topics=True
)

lda_model