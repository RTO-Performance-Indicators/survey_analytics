# Text cleaning/preparation designed for student sat survey verbatims 
# prior to LDA modeling

# Generally each function does one thing.

# Most functions are run within "prepare_text" prior to making an LDA corpus using gensim.
# I have tried to define the functions in an order that they are defined 
# before other functions which call them.

# After defining all the functions there is an example of how they are 
# used to create an LDA model.

#import required modules
import pandas as pd
import numpy as np
import collections
from itertools import chain
import re
import nltk

def split_words(text):
# This function splits common words that are erroneously joined together 
# in the survey verbatims. 
# This is run within the prepare_df function as that's where the tokenistation occurs. 
# Prepare_df is itself called within prepare_text.
    text = text.replace("alot","a lot")
    text = text.replace('atleast','at least')
    text = text.replace('iam','i am')
    text = text.replace('aswell','as well')
    text = text.replace('abit','a bit')
    text = text.replace('wanna','want to')
    return text

def prepare_df(df, colname):
# Filter so verbatim column is not null and turn strings into lists of individual words
# For multiple columns I would be turning them into a single column first, 
# but this could be edited to take a list of columns if needed.
# Some basic text correction included as it is easiest before tokenising

    # remove null rows so string functions don't get type errors when they crop up 
    # (and it's a smaller dataset too)
    data = df[df[colname].notnull()]
    
    # lowercase
    data[colname]= [x.lower() for x in data[colname]]
   
    # I then delete the apostrophes because there's high instances where people 
    # omit them e.g. didnt, im etc. this is easier than replacing each one of these words...
    data[colname]= [x.replace(r"'","") for x in data[colname]]
    
    # also need to split words people erroneously join together before tokenising
    data[colname]= [split_words(x) for x in data[colname]]
    
    # tokenise data by returning list of all chunks of alphanumeric characters 
    # with no puncutation or whitespace. This works well enough for me compared 
    # to other options. Chose not the include hypens as in many cases the same 
    # words as used both with and without so treating them all as two words and 
    # putting them back together as bigrams standardises them.
    data[colname]= [re.findall(r"[\w]+", x) for x in data[colname]]    
    
    return data

def basic_bow(df,colname):
# This function isn't part of the data cleaning and isn't required prior to LDA. 
# It makes a nice human readable table of words and frequencies for getting a feel of the data.
# the input must be a nested list of lists of words - like the output of prepare_df.
# I used this to get the common spelling errors by exporting this to excel and 
# running spellchecker through the data.
# Also used to look at the word frequencies where I filtered the data based on 
# the responses to other questions as a proxy for sentiment.
    
    # make flat list of all tokens
    aslist = list(chain.from_iterable(df[colname].tolist()))
    # alphabetise
    aslist.sort()
    # count occurences of each word in list. Returns a dictionary.
    counted = collections.Counter(aslist)
    # make df from dictionary and give nice column names.
    counts_df = pd.DataFrame.from_dict(counted, orient='index').reset_index()
    counts_df.columns = ['word','count']
    # sort by counts from highest to lowest
    counts_df.sort_values(by=['count'], ascending=False,inplace=True)
    return counts_df

# There are two versions of this so I can use it in different contexts. 
# Generally I would use the nested list one as that's what prepare_df creates.
# at some point I'll make them one function with a parameter to specify the input format.
def remove_names(textlist,namelist):
# replaces names from a specified list with [NAME]
    textlist = [x.replace(x,'[NAME]') if x in namelist else x for x in textlist]
    return textlist

def remove_names_nested_list(nested_list,namelist):
# replaces names from a specified list with [NAME]
    textlist = [[x.replace(x,'[NAME]') if x in namelist else x for x in textlist]for textlist in nested_list]
    return textlist
    
def spelling_is_fun(text):
# fix common spelling errors  
    # str.replace is reportedly faster than re.sub
    text = text.replace('accessable','accessible')
    text = text.replace('accomod','accommod')
    text = text.replace('allways','always')
    text = text.replace('ather','other')

    text = text.replace("bcoz'","because")
    text = text.replace('becuse','because')
    text = text.replace('beacuse','because')
    text = text.replace('beacause','because')
    text = text.replace('benifit','benefit')
    
    text = text.replace('chisolm','chisholm')
    text = text.replace('comunity','community')
    text = text.replace('convinient','convenient')
    text = text.replace('convienient','convenient')
    text = text.replace('convient','convenient')
    text = text.replace('convience','convenience')
    text = text.replace('conveniant','convenient')
    text = text.replace('coarse','course')
    text = text.replace('corse','course')
    text = text.replace('coure','course')
    
    text = text.replace('definately','definitely')
    
    text = text.replace("educaters'","teachers")
    text = text.replace("enroll","enrol")
    text = text.replace('enviornment','environment')
    text = text.replace('excelent','excellent')
    text = text.replace('exsperience','experience')
    text = text.replace('expierence','experience')
    text = text.replace('experiance','experience')
    
    
    text = text.replace('facilty','facility')
    text = text.replace('feild','field')
    text = text.replace('flexability','flexibility')
    text = text.replace('foresite','foresight')
    text = text.replace('freindly','friendly')
    text = text.replace('freidly','friendly')
    
    text = text.replace('greatful','grateful')
    text = text.replace('goverment','government')

    text = text.replace('helful','helpful')
    text = text.replace('helpfull','helpful')
    text = text.replace('homesglen','holmesglen')

    text = text.replace("instructers'","teachers")
    text = text.replace('inviroment','environment')
    
    text = text.replace("knowledgable","knowledgeable")
    
    text = text.replace('leant','learnt')
    text = text.replace("likely'","likely")
    
    text = text.replace('managment','management')
    text = text.replace('mth','month')
    
    text = text.replace('organize','organise')
    text = text.replace('persue','pursue')
    text = text.replace('organization','organisation')
    text = text.replace('orginisation','organisation')
    text = text.replace('organistion','organisation')
    text = text.replace('oranganisation','organisation')
    
    text = text.replace('plagerised','plagiarised')
    text = text.replace('plesent','pleasant')
        
    text = text.replace('rother','rather')
    text = text.replace('recomment','recommend')
    text = text.replace('recomend','recommend')
    text = text.replace('recommed','recommend')
    text = text.replace('reccomend','recommend')
    text = text.replace("recieve","receive")
    text = text.replace('relivent','relevant')
    text = text.replace('relevent','relevant')
    text = text.replace('realy','really')
    
    text = text.replace('srudent','student') 
    text = text.replace('studing','studying')
    
    text = text.replace('terriffic','teriffic')
    text = text.replace('terrific','teriffic')
    text = text.replace('terific','teriffic')
    text = text.replace('thier','their')
    text = text.replace('throughly','thoroughly')
    text = text.replace('traing','training')
    text = text.replace('traineer','teacher')
    text = text.replace('tranier','teacher')
    text = text.replace('tremendouss','tremendous')
    text = text.replace('tremendou','tremendous')
    text = text.replace('trainn','train')
    text = text.replace('traner','trainer')
    text = text.replace('traning','training')
    text = text.replace('trainor','trainer')
    
    text = text.replace('untill','until')

    text = text.replace('waisted','wasted')
    text = text.replace('workal','work')
    
    text = text.replace('yr','year')
    
    
    
    # use regex library for recognising patterns
    # these crop up presumably where people use something other than '
    
    re.sub("couldn$","couldnt",text)

    re.sub("didn$","didnt",text)
    re.sub("^dis[a-z]+point", "disappoint", "disapppoint")
    re.sub("doesn$","doesnt",text)  
    
    re.sub("hadn$","hadn't",text)
    
    re.sub("isn$","isnt",text)
    
    re.sub("shouldn$","shouldnt",text)
    
    re.sub("wasn$","wasnt",text)
    re.sub("weren$","werent",text)
    re.sub("wouldn$","wouldnt",text)
    
    # This one also appears as "couselling" so need to use regex
    re.sub('^couse$','course',text)
    
    # Additional ones the need to be exact matches as they occur validly within other words
    re.sub('^tho$','though',text)
    re.sub('^cours$','course',text)
    re.sub('^grate$','great',text)
    re.sub('^ect$','etc',text)
    re.sub("asses[^s]*",'assess',text)
    re.sub('^cert$','certificate',text)
    re.sub("^uni$",'university',text)

    return(text)

def synonyms_are_noise(text):
# Standardize similar words
    text = text.replace('trainer','teacher')
    text = text.replace('occupation','work')
    text = text.replace('job','work')
    text = text.replace('employment','work')
    text = text.replace('unorganised','disorganised')
    
    return(text)

# These are the custom lists of stopwords I've been using. 
# The functions are written so any list can be used though.
# lists of stopwords
duds = ['and','the','am','to','i','did','has','a','me','was','of','course','in','it','for','course','my','with','is','they','that','this','are','have','you','as','because','had',"ive",'on','at','be','all','would','there','from','very','were','get','so','we','do','or','if','an','about','or','when','which','also','t','really','very','s','he','she','his','her','our','them','we','their','u','l',"im",'by','box_hill','kangan','holmesglen','melbourne_polytechnic','mcie','swtafe','aie','rmit','chisholm','wyndham','mwt','ctm','mfi','coonara','seda','seymour','moe','southwest','knight','swinburn','tbm','bawm','objective','primary','who','will','more','less','can','how','make','should','these','just','it','is','it_is','need',"dont",'into','may','some','what','then','than','etc','could','nothing']
#this one includes additional list of sentiment words
duds_plus_sent = duds + ['no','not','but','good','great','excellent','teacher','happy','love','fantastic','thanks','like','best','bad','poor','great','excellent','love','good','disappoint','disappointed','terrible','wonderful','brilliant','unhappy','enjoy','amazing','terrific']
#convert lists to dictionaries because they're way more efficient for membership testing
duds_plus_sent = dict.fromkeys(duds_plus_sent, True)
duds= dict.fromkeys(duds, True)

def penn2morphy(penntag):
# this was taken from the web to match up ntlk's built in POS tagger results 
# with those required by the lemmatizer function.
# I modified it to take in a broader list of tags.
    """ Converts Penn Treebank tags to WordNet. """
    morphy_tag = {'NN':'n','NNS':'n','NNP':'n','NNPS':'n', 'JJ':'a',
                  'JJR':'a','JJS':'a','VB':'v','VBD':'v','VBG':'v','VBN':'v','VBP':'v','VBZ':'v', 'RB':'r', 'RBR':'r', 'RBS':'r'}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return 'n' # if mapping isn't found, fall back to Noun.


def get_lemmatized_text(text):
# lemmatizer for pos tagged text
    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    
    return [[lemmatizer.lemmatize(word, pos=penn2morphy(tag)) 
            for word, tag in sentence] for sentence in text]


def lemmatize_list(text_list):
# lemmatize lists of untagged word tokens.
# I made this for when I'm doing this on its own, 
# not in the prepare_text function e.g. when making wordclouds.
    # add POS tags
    from nltk import pos_tag
    tagged = pos_tag(text_list) 

    #then lemmatize
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos=penn2morphy(tag)) for word, tag in tagged]

def make_bigrams_sentences(text) :
# this code copied from interwebz
    bigram = gs.models.Phrases(text, min_count=5, threshold=20) # higher threshold fewer phrases.
    bigram_mod = gs.models.phrases.Phraser(bigram)
    text = [bigram_mod[sentence] for sentence in text]
    return text

# Prepare text for topic modelling. 
# This replaces synonyms and mispelled words, lemmatizes text and removes stopwords and numerals. Specifiy text as a list of sentences which are themselves lists of words, and a list of stopwords.
def prepare_text(df, colname, stops, min_length=1):
    #remove NAs and split into tokens
    data = prepare_df(df, colname)
    #select just tokens column
    text = data[colname]
    #remove proper names
    text= remove_names_nested_list(text,names)
    #fix known typos
    text = [[spelling_is_fun(word) for word in sentence]for sentence in text]
    #change trainer to teacher
    text = [[synonyms_are_noise(word) for word in sentence]for sentence in text]
    #remove numerals
    text = [[re.sub('[0-9]','',word)for word in sentence]for sentence in text]
    #join bigrams
    text = make_bigrams_sentences(text)
    #add POS tags for lemmatizer
    tagged = [nltk.pos_tag(x) for x in text]
    #lemmatize
    lemmatized = get_lemmatized_text(tagged)
    #remove stopwords
    no_stops = [[word for word in sentence if word not in stops]for sentence in lemmatized]
    #filter out short verbatims
    no_stops = [x for x in no_stops if len(x) > (min_length-1)]
    return no_stops


# the functions below take the output from prepare_text and create 
# a gensim dictionary and corpus which are the inputs for gensim's LDA model.

def prep_for_LDA(textlist):
    #create dictionary and corpus from initial data (tokens as nested lists- i.e. output from prepare_text ).
    dictionary = gs.corpora.Dictionary(textlist)
    #filter out the most and least frequent words
    dictionary.filter_extremes(no_below=10, no_above=0.35)
    corpus = [dictionary.doc2bow(text) for text in textlist]
    #save in the working file so I can get it in another session without running this function again. Should make this optional and make the filename a parameter.
    dictionary.save('dictionary.gensim')
    return dictionary, corpus

def prep_for_LDA_tfidf(textlist):
    #create dictionary and corpus from initial data (tokens as nested lists)
    dictionary = gs.corpora.Dictionary(textlist)
    #filter out the most and least frequent words
    dictionary.filter_extremes(no_below=10, no_above=0.35)

    corpus = [dictionary.doc2bow(text) for text in textlist]
    #change corpus from bow vectors to normalized tfidf
    tfidf = gs.models.TfidfModel(corpus,normalize=True)
    corpus = tfidf[corpus]
    dictionary.save('dictionary.gensim')
    return dictionary, corpus

#example of using these in an LDA model
#I made this function to call gensim's LDA and then save the model. The default values for alpha, eta and random_state are the gensim defaults.
def LDA(corpus, dictionary, topics, savename='model',alpha='symmetric',eta=None,random_state=None):
    #machine learning magic happens
    ldamodel = gs.models.LdaModel(corpus, num_topics = topics, id2word=dictionary, passes=300, alpha=alpha,eta=eta,random_state=random_state)
    ldamodel.save(savename + '.gensim')
    return ldamodel

#how I call the functions. Column name has been redacted but it's a column of verbatims.
tokens = prepare_text(df=df,colname='redacted',stops=duds_plus_sent,min_length=2)
dictionary_tfidf, corpus_tfidf = prep_for_LDA_tfidf(tokens)
dictionary, corpus = prep_for_LDA(tokens)
lda_auto_beta_new =LDA(corpus,dictionary,20,'testmodel_sc_ab_new',alpha=0.1,eta='auto',random_state=27)
lda_p_test_tfidf =LDA(corpus_tfidf,dictionary_tfidf,20,'testmodel_sc_tfidf',random_state=27)

#%%
#functions for exploring LDA results

def LDA_visualise(model,corpus, dictionary, output_filename=None):
#shows interactive visualisation for the specified gensim LDA model and optionally exports it for viewing in browser. 
#Corpus and dictionary must be the same ones used to create the model.
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(model, corpus, dictionary)
    if output_filename is not None:
        pyLDAvis.save_html(vis, output_filename + '.html')
    return vis


def topic_columns(doc_topics,tokens='tokens'):
#returns a dataframe with probabilities for each LDA topic for each processed verbatim.
#doc_topics is the object returned from calling the .get_document_topics() method on a gensim lda model. This is a nested list of (topic, probability) for each topic for each document.
#make a dataframe with columns of LDA topics and probabilities for each row of input
    topics =[]
    columns=['tokens']
    for i in range(0,len(doc_topics)):
        output = [" ".join(tokens[i])]
        for j in range(0,len(doc_topics[i])):
            output.append(doc_topics[i][j][1])
        topics.append(output)
    for j in range(0,len(doc_topics[0])):
        columns.append(j)
    topicsdf = pd.DataFrame(topics,columns=columns)
    return topicsdf

def merge_LDA_with_df(df,verb_col,model,corpus,LDA_tokens,stopwords,IDcolumn):
#function to add columns of the LDA topics and their probabilities to the original source data
#adds tokens column to input df and then merges the output of topic_columns on this.
    #do text preprocessing inplace so it's matchable to the other variables
    #use the same parameters as those used to create LDA_tokens.
    tokensdf = text_to_tokens_inplace(df,verb_col,stops=stopwords,IDcol=IDcolumn)
    #merge preprocessed tokens back into original dataframe
    merged= pd.merge(df,tokensdf,left_index=True,right_index=True,how='left')
    #replace empty tokens with empty string so they're all the correct data type
    merged['tokens'].fillna("", inplace=True)
    #get topics using an existing model and the convert to df. 
    #note: Model corpus must be made from same tokens as those in tokensdf. This requires the same parameters to be used.
    doc_topics= [model.get_document_topics(x, minimum_probability=0) for x in corpus]
    topics_all = topic_columns(doc_topics,tokens=LDA_tokens)
    #drop identical tokens (there's quite a few if you allow short minimum length e.g. ones that just say thank you)
    topics_all.drop_duplicates(subset=['tokens'],inplace=True)
    #merge LDA results back into full dataframe
    merged_topics = pd.merge(merged,topics_all,on=['tokens'],how='left')
    return merged_topics