#%%
import re
import nltk
import pandas as pd
import numpy as np

#%%
df = pd.read_csv("data/s_fs_name_v.csv")

#%%
# filePath = 'S:/RTOPI/Both Surveys/All Final Datasets/Datasets - 2019/StudentSurveys.csv'
# df = pd.read_csv(filePath, encoding = 'ISO-8859-1')
# df = df[df['SurveyYear'] == 'S2019']

# SELECT columns that relate to further study (fs)
# and filter to non-NA verbatim for the course name
# and save data to csv to use as test
#%%
# df = df.filter(regex = "^s_fs", axis = 1)[~pd.isna(df["s_fs_name_v"])]
# df = df[['s_fs_lev', 's_fs_name_v']]
# df['id'] = range(1, len(df) + 1)
# df = df[['id', 's_fs_lev', 's_fs_name_v']]
# df.to_csv("data/s_fs_name_v.csv")

# Function to get a data frame as an input,
# and convert into a one-token-per-row format
#%%
def split_explode(df, id = 'SurveyResponseID', colname = 's_fs_name_v'):
    # Get only required columns from Student Survey data,
    # even when a whole data frame is provided
    df = df[[id, colname]]
    df['tokens'] = df[colname].apply(lambda x: nltk.word_tokenize(x))
    df = df.explode('tokens')

    return(df)

# test split_explode function
#%%
# split_explode(df = fs_v, id = 'id')
# split_explode(df = df[['id', 's_fs_name_v']].dropna(), id = 'id')

# Function to take in a string variable, or pandas.Series
# to return a cleaned vector of text
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
    string = re.sub(pattern = "^cert1", repl = "cert i", string = string)
    string = re.sub(pattern = "^cert11", repl = "cert ii", string = string)
    string = re.sub(pattern = "^cert111", repl = "cert iii", string = string)

    # Convert Arabic to Roman numbers
    # (mainly for certificates)
    string = re.sub(pattern = "^1$", repl = "i", string = string)
    string = re.sub(pattern = "^2$", repl = "ii", string = string)
    string = re.sub(pattern = "^3$", repl = "iii", string = string)
    string = re.sub(pattern = "^4$", repl = "iv", string = string)

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
# NOTE: map is faster than list comprehension. See:
#       https://www.geeksforgeeks.org/python-map-vs-list-comprehension/


# Combined function
# Take in a data frame, and a column name
# %%
def fix_fs_name_v(df, id = 'SurveyResponseID', colname = 's_fs_name_v'):
    # Remove rows with s_fs_name_v == NaN
    df = df.dropna()

    # tokenize s_fs_name_v and convert to one-token-per-row data frame
    tokenized_df = split_explode(df = df, id = id, colname = colname)

    # Fix words
    tokenized_df['tokens2'] = tokenized_df['tokens'].apply(string_subs)
    
    # Join tokens together again
    df_fixed = tokenized_df.groupby([id, colname])['tokens2'].apply(' '.join).reset_index(name = 's_fs_name_v_fixed')

    return(df_fixed)

# test
temp = fix_fs_name_v(df = df, id = 'id')
temp

# fix real data
# %%
df_fixed_interim = fix_fs_name_v(df = df, id = 'id')
df_fixed_interim

# Check for biggest errors
# %%
errors = df_fixed_interim['s_fs_name_v_fixed'].value_counts()
errors

# %%
df_fixed_interim[df_fixed_interim['s_fs_name_v_fixed'] == 'vce year 11']

# %%
