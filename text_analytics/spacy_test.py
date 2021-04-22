import pandas as pd

import hunspell
import spacy
#from spacy_hunspell import spacy_hunspell # unable to install spacy_hunspell

data = pd.DataFrame({
    'SurveyResponseID': [1, 2, 3],
    's_rsn_dc_v': [
        'Testing the spacy package', 
        'I was really unsatisfied with the training', 
        'The teachers and trainors at Chisholm were bulying the students']
})

# Load small trained pipeline that is used to predict POS tags and dependencies
# Can use en_core_web_lg for a larger trained pipeline
nlp = spacy.load('en_core_web_sm')

# Create document object for each verbatim
data['doc'] = [nlp(text) for text in data['s_rsn_dc_v']]

# Number of tokens in each doc
data['n_tokens'] = [len(tokens) for tokens in data['doc']]

data

# Part of Speech (POS) tagging
for token in data['doc'][1]:
    print(token.text, token.pos_)

# Lemmatization
for token in data['doc'][1]:
    print(token.text, token.lemma_)

# Is stop word
for token in data['doc'][1]:
    print(token.text, token.is_stop)

# Named entities
for ent in data['doc'][2].ents:
    print(ent.text, ent.label_)