#%%
import re
import nltk
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

#%%
nltk.word_tokenize("Bachellor of business")

# Tokenize strings
#%%
course_v = ["Bachellors of nursing ",
            "Cert  IV in business",
            "cer i in a",
            "certi b",
            "certII of c",
            "CertIV in d",
            "cert1 in e",
            "cert11 in f",
            "Cert111 in g",
            "cert 1 in h",
            "Cert one in i",
            "certif three in j",
            "Adv Dip in Nursing",
            "dip in Early childhood education and care",
            "associates degree in ",
            "Bachelor of Business",
            "Advanced diploma of cyber security"]
fs_v = {'id': list(range(1, len(course_v) + 1)),
        's_fs_name_v':course_v
        }
fs_v = pd.DataFrame(fs_v)
# fs_v['tokens'] = fs_v['s_fs_name_v'].str.split()
# fs_v.explode('tokens')
# fs_v['tokens'] = fs_v['s_fs_name_v'].apply(lambda x: nltk.word_tokenize(x))
# fs_v


#%%
def split_explode(df, id, colname = 's_fs_name_v'):
    # Get only required columns from Student Survey data
    df = df[[id, colname]]
    # df['tokens'] = df[colname].str.split()
    df['tokens'] = df[colname].apply(lambda x: nltk.word_tokenize(x))
    df = df.explode('tokens')

    return(df)

# test
split_explode(df = fs_v, id = 'id')

# Create a function that can be used on a single string,
# or a pandas.Series
#%%
def string_subs(string):
    string = string.lower()
    string = str.strip(string)
    string = re.sub(" +", " ", string)

    # Fix different ways to spell bachelor
    string = re.sub(pattern = "^bac[a-z]*", repl = "bachelor", string = string)
    string = re.sub(pattern = "^bahelor", repl = "bachelor", string = string)

    string = re.sub(pattern = "^batch", repl = "bachelor", string = string)
    string = re.sub(pattern = "^batchler", repl = "bachelor", string = string)

    string = re.sub(pattern = "^bauchor", repl = "bachelor", string = string)
    string = re.sub(pattern = "^bechalor", repl = "bachelor", string = string)
    string = re.sub(pattern = "^bechlor", repl = "bachelor", string = string)
    string = re.sub(pattern = "^becholar", repl = "bachelor", string = string)

    string = re.sub(pattern = "^bchelor", repl = "bachelor", string = string)


    # Add spaces between "cert" and numbers
    # (Must occur before fixing cert -> certificate)
    string = re.sub(pattern = "^certi$", repl = "cert i", string = string)
    string = re.sub(pattern = "^certii$", repl = "cert ii", string = string)
    string = re.sub(pattern = "^certiii$", repl = "cert iii", string = string)
    string = re.sub(pattern = "^certiv$", repl = "cert iv", string = string)
    string = re.sub(pattern = "^cert1$", repl = "cert i", string = string)
    string = re.sub(pattern = "^cert11$", repl = "cert ii", string = string)
    string = re.sub(pattern = "^cert111$", repl = "cert iii", string = string)

    # Convert Arabic to Roman numbers
    # (mainly for certificates)
    string = re.sub(pattern = "1", repl = "i", string = string)
    string = re.sub(pattern = "2", repl = "ii", string = string)
    string = re.sub(pattern = "3", repl = "iii", string = string)
    string = re.sub(pattern = "4", repl = "iv", string = string)

    # Convert English to Roman numbers
    # (mainly for certificates)
    string = re.sub(pattern = "one", repl = "i", string = string)
    string = re.sub(pattern = "two", repl = "ii", string = string)
    string = re.sub(pattern = "three", repl = "iii", string = string)
    string = re.sub(pattern = "four", repl = "iv", string = string)

    string = re.sub(pattern = "1v", repl = "iv", string = string)

    # Fix different ways to spell certificate
    string = re.sub(pattern = "^cert[a-z]*", repl = "certificate", string = string)
    string = re.sub(pattern = "^cer$", repl = "certificate", string = string)

    # Fix different ways to spell avanced
    string = re.sub(pattern = "^adv[a-z]*", repl = "advanced", string = string)

    # Fix different ways to spell diploma
    string = re.sub(pattern = "dip[a-z]*", repl = "diploma", string = string)

    # Fix different ways to spell associate
    string = re.sub(pattern = "^associa[a-z]*", repl = "associate", string = string)

    return(string)

# test
#%%
list(map(string_subs, course_v))

# %%
temp = split_explode(df = fs_v, colname = 's_fs_name_v')
temp['tokens2'] = temp['tokens'].apply(string_subs)

# Combined function
# Take in a data frame, and a column name
# %%
def fix_fs_name_v(df, colname = 's_fs_name_v'):
    # tokenize and convert to narrow data frame
    tokenized_df = split_explode(df = df, colname = colname)

    fixed_df
