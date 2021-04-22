import pandas as pd

import hunspell
import spacy
#from spacy_hunspell import spacy_hunspell # unable to install spacy_hunspell

# Load small trained pipeline that is used to predict POS tags and dependencies
# Can use en_core_web_lg for a larger trained pipeline
nlp = spacy.load('en_core_web_sm')

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

# 'en_core_web_sm' is a standardised pipeline.
# Pipelines are made of pipes.
# The pipeline is:
#   1. tokenizer
#   2. tagger
#   3. parser (add dependency labels)
#   4. ner (entity recogniser)
#   5. lemmatizer
#   6. textcat (text categoriser)
#   7. custom (custom components)
# We can modify existing pipelines by adding pipes!
# def function(doc):
#     ...
#     return doc

# custom_nlp = nlp.add_pipe(function, before='parser')