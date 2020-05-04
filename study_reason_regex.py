#%%
import re
import pandas as pd
import numpy as np

#%%
filePath = 'S:/RTOPI/Both Surveys/All Final Datasets/Datasets - 2019/StudentSurveys.csv'
df = pd.read_csv(filePath, encoding = 'ISO-8859-1')
df = df[df['SurveyYear'] == 'S2019']

#%%
df.columns.to_list()

# SELECT columns that relate to further study (fs)
# and filter to non-NA verbatim for the course name
#%%
df.filter(regex = "^s_fs", axis = 1)[~pd.isna(df["s_fs_name_v"])]

# Unique s_fs_name_v
#%%
s_fs_name_v = df[~pd.isna(df["s_fs_name_v"])]["s_fs_name_v"]
s_fs_name_v = [x.lower() for x in s_fs_name_v]
pd.Series(s_fs_name_v).value_counts()

# Dummy data for testing
#%%
string = [" Bach  of Engineering ", "Bachellors ", "bach of comm", "bachelo"]

# Function to take in a vector of text
# to return a cleaned vector of text
# NOTE: map is faster than list comprehension. See:
#       https://www.geeksforgeeks.org/python-map-vs-list-comprehension/
#%%
def process_further_study_verbatim(string):

    # To lowercase
    string = map(str.lower, string)

    # Remove white space at either end of string
    string = map(str.strip, string)

    # Remove extra spaces between words
    string = map(lambda x: re.sub(" +", " ", x), string)

    # Different spelling for Bachelor
    string = map(lambda x: re.sub("b of ", "bachelor  of ", x), string)

    string = map(lambda x: re.sub("bacgelor ", "bachelor ", x), string)

    string = map(lambda x: re.sub("bach ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachalor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachel ", "bachelor ",x), string)
    string = map(lambda x: re.sub("bachelo ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachelour ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bacherlor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachlelor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachleor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachloer ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bachlor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bacholar ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bacholer ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bacholor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bacholors ", "bachelor ", x), string)
    
    string = map(lambda x: re.sub("bahelor ", "bachelor ", x), string)

    string = map(lambda x: re.sub("batch of ", "bachelor of ", x), string)    
    string = map(lambda x: re.sub("batchelor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("batchler ", "bachelor ", x), string)
    
    string = map(lambda x: re.sub("bauchor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bechalor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("bechlor ", "bachelor ", x), string)
    string = map(lambda x: re.sub("becholar ", "bachelor ", x), string)
    
    string = map(lambda x: re.sub("bchelor ", "bachelor ", x), string)
    
    # diplomas and advanced diplomas
    string = map(lambda x: re.sub("adv ", "advanced ", x), string)
    string = map(lambda x: re.sub("advance ", "advanced ", x), string)
    string = map(lambda x: re.sub("dip ", "diploma ", x), string)
    string = map(lambda x: re.sub("diplom ", "diploma ", x), string)
    string = map(lambda x: re.sub("diploma in ", "diploma of ", x), string)
    string = map(lambda x: re.sub("advanced deploma ", "advanced diploma ", x), string)
    string = map(lambda x: re.sub("advanced dioloma ", "advanced diploma ", x), string)
    string = map(lambda x: re.sub("advanced deplima ", "advanced diploma ", x), string)
    string = map(lambda x: re.sub("advanced dipolma ", "advanced diploma ", x), string)
    
    # Certificates
    string = map(lambda x: re.sub("cert ", "certificate ", x), string)
    string = map(lambda x: re.sub("cart ii ", "certificate ii ", x), string)
    string = map(lambda x: re.sub("cartificate ", "certificate ", x), string)
    string = map(lambda x: re.sub("cerficate ", "certificate ", x), string)
    string = map(lambda x: re.sub("ceritificate ", "certificate ", x), string)
    string = map(lambda x: re.sub("cerificate ", "certificate ", x), string)
    string = map(lambda x: re.sub("certicate ", "certificate ", x), string)
    string = map(lambda x: re.sub("certifacate ", "certificate ", x), string)
    string = map(lambda x: re.sub("certifcate ", "certificate ", x), string)
    string = map(lambda x: re.sub("certificat ", "certificate ", x), string)
    string = map(lambda x: re.sub("certifucate ", "certificate ", x), string)
    string = map(lambda x: re.sub("certigicate ", "certificate ", x), string)
    string = map(lambda x: re.sub("cert1 ", "certificate i ", x), string)
    string = map(lambda x: re.sub("cert111 ", "certificate iii ", x), string)
    string = map(lambda x: re.sub("cert1v ", "certificate iv ", x), string)
    string = map(lambda x: re.sub("cer ii ", "certificate  ii ", x), string)
    string = map(lambda x: re.sub("cer iii ", "certificate  iii ", x), string)
    string = map(lambda x: re.sub("cer iv ", "certificate  iv ", x), string)
    string = map(lambda x: re.sub("certii ", "certificate  ii ", x), string)
    string = map(lambda x: re.sub("certiii ", "certificate  iii ", x), string)
    string = map(lambda x: re.sub("certiv ", "certificate  iv ", x), string)
    string = map(lambda x: re.sub("certificate l ", "certificate i ", x), string)
    string = map(lambda x: re.sub("certificate1 ", "certificate i ", x), string)
    string = map(lambda x: re.sub("certificate1in ", "certificate i in ", x), string)
    string = map(lambda x: re.sub("certificate ll ", "certificate ii ", x), string)
    string = map(lambda x: re.sub("certificateii ", "certificate ii ", x), string)
    string = map(lambda x: re.sub("certificateiii ", "certificate iii ", x), string)
    string = map(lambda x: re.sub("certificate four ", "certificate iv ", x), string)
    string = map(lambda x: re.sub("certificate three ", "certificate iii ", x), string)
    string = map(lambda x: re.sub("certificate two ", "certificate ii ", x), string)
    string = map(lambda x: re.sub("certificates iii ", "certificate iii ", x), string)
    string = map(lambda x: re.sub("certificates three ", "certificate iii ", x), string)
    string = map(lambda x: re.sub("certificates iv ", "certificate iv ", x), string)
    string = map(lambda x: re.sub("certification iii ", "certificate iii ", x), string)
    string = map(lambda x: re.sub("certification iv ", "certificate iv ", x), string)
    string = map(lambda x: re.sub("certificate 1 ", "certificate i ", x), string)
    string = map(lambda x: re.sub("certificate 11 ", "certificate ii ", x), string)
    string = map(lambda x: re.sub("certificate 1v ", "certificate iv ", x), string)
    string = map(lambda x: re.sub("certificate 1in ", "certificate i in ", x), string)
    string = map(lambda x: re.sub("certificate vi ", "certificate iv ", x), string) # there are no cert 6
    string = map(lambda x: re.sub("certificate 1 ", "certificate i ", x), string)
    string = map(lambda x: re.sub("very iv ", "certificate iv ", x), string)        # mobile word prediction cert > very
    string = map(lambda x: re.sub("\\<111\\>", "iii", x), string)
    string = map(lambda x: re.sub("4", "iv", x), string)
    string = map(lambda x: re.sub("3", "iii", x), string)
    string = map(lambda x: re.sub("2", "ii", x), string)
    string = map(lambda x: re.sub("lll", "iii", x), string)
    string = map(lambda x: re.sub("lv", "iv", x), string)

    # s_fs_name_v = gsub("certification ||| ", "certificate iii ", s_fs_name_v),
    
    # Masters degres
    string = map(lambda x: re.sub("masters of", "master of", x), string)
    string = map(lambda x: re.sub("masters in", "master of", x), string)
    
    # Associate degrees
    string = map(lambda x: re.sub("associate degree of ", "associate degree in ", x), string)
    string = map(lambda x: re.sub("associates degree in ", "associate degree in ", x), string)
    string = map(lambda x: re.sub("associated degree ", "associate degree ", x), string)
    string = map(lambda x: re.sub("associates degree ", "associate degree ", x), string)


    string = list(string)

    return(string)

# Test function
process_further_study_verbatim(string)


# Create a function that can be used on a single string,
# or a pandas.Series
#%%
def fix_fs_v(string):
    string = string.lower()
    string = str.strip(string)
    string = re.sub(" +", " ", string)

    # Fix different ways to spell bachelor
    string = re.sub(pattern = "^bac[a-z]+", repl = "bachelor", string = string)

    # Fix different ways to spell certificate
    string = re.sub(pattern = "^cert[a-z]+", repl = "certificate", string = string)    
    
    return(string)
# test
fix_fs_v("Bachelor of Nursing ")
list(map(fix_fs_v, ["Bachellors of nursing ", "Cert  IV in business"]))
