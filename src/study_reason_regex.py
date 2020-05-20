#%%
import re
import nltk
import pandas as pd
import numpy as np

#%%
df = pd.read_csv("../data/s_fs_name_v.csv")

#%%
# filePath = 'S:/RTOPI/Both Surveys/All Final Datasets/Datasets - 2019/StudentSurveys.csv'
# df = pd.read_csv(filePath, encoding = 'ISO-8859-1')
# df = df[df['SurveyYear'] == 'S2019']

#%%
# s_fs_lev_dict = {'s_fs_lev': [1, 2, 3, 4, 5, 6, 7, 8, 9],
#                  'level_description': ['certificate i', 'certificate ii',
#                                        'certificate iii', 'certificate iv',
#                                        'vce or vcal', 'diploma',
#                                        'advanced diploma', 'bachelor', 'higher than a degree']}
# s_fs_lev_dict = pd.DataFrame(s_fs_lev_dict)

# SELECT columns that relate to further study (fs)
# and filter to non-NA verbatim for the course name
# and save data to csv to use as test
#%%
# df = df.filter(regex = "^s_fs", axis = 1)[~pd.isna(df["s_fs_name_v"])]
# df = df[['s_fs_lev', 's_fs_name_v']]
# df['id'] = range(1, len(df) + 1)
# df = pd.merge(df, s_fs_lev_dict, how = 'left')
# df = df[['id', 's_fs_lev', 'level_description', 's_fs_name_v']]
# df.to_csv("../data/s_fs_name_v.csv", index = False)

# Function to get a data frame as an input,
# and convert into a one-token-per-row format
#%%
def split_explode(df, id = 'SurveyResponseID',  colname = 's_fs_name_v'):
    df = df[[id, colname]]
    df['tokens'] = df[colname].apply(lambda x: nltk.word_tokenize(x))
    tokenized_df = df.explode('tokens')

    return(tokenized_df)


# Function to take in a string variable, or pandas.Series
# to return a cleaned vector of text
#%%
def string_subs(string):
    string = string.lower()
    string = str.strip(string) # strip whitespace
    string = re.sub("\.+", "", string)
    string = re.sub(" +", " ", string) # Remove excess spaces

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
    string = re.sub(pattern = "^one$", repl = "i", string = string)
    string = re.sub(pattern = "^two$", repl = "ii", string = string)
    string = re.sub(pattern = "^three$", repl = "iii", string = string)
    string = re.sub(pattern = "^four$", repl = "iv", string = string)

    # Different ways of signalling IV
    string = re.sub(pattern = "^1v$", repl = "iv", string = string)
    string = re.sub(pattern = "^lv$", repl = "iv", string = string)
    string = re.sub(pattern = "^iiii$", repl = "iv", string = string)

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

#%%
def fix_parentheses(string):
    string = re.sub(pattern = "\( ", repl = "(", string = string)
    string = re.sub(pattern = " \)", repl = ")", string = string)
    
    return(string)

#%%
def fix_ecec(string):
    ecec_misspellings = ['early childhood', 'childcare', 'child care', 'early childhood education',
                         'early childhood and education', 'ecec', 'childcare course',
                         'early education']
    
    if string in ecec_misspellings:
        return('early childhood education and care')
    else:
        return(string)

def fix_aged_care(string):
    aged_care_misspellings = ['agecare', 'agedcare', 'age care', 'aged care course']

    if string in aged_care_misspellings:
        return('aged care')
    else:
        return(string)

def fix_health_services(string):
    health_services_misspellings = ['health service assistance', 
                                    'health service assistant', 
                                    'health services assistance']

    if string in health_services_misspellings:
        return('health services assistance')
    else:
        return(string)

def fix_light_vehicle_mech(string):
    health_services_misspellings = ['light vehicle mechanic', 
                                    'light vehicle mechanics']

    if string in health_services_misspellings:
        return('light vehicle mechanical technology')
    else:
        return(string)

def fix_it(string):
    it_misspellings = ['it']

    if string in it_misspellings:
        return('information technology')
    else:
        return(string)

def fix_accounting_bookkeeping(string):
    acc_bookkeeping_misspellings = ['accountant and bookkeeping', 'accounting + bookkeeping',
                                    'accounting and booking', 'accounting and bookkeeper'
                                    'accounting and bookmaker']

    if string in acc_bookkeeping_misspellings:
        return('accounting and bookkeeping')
    else:
        return(string)

def fix_electrotech(string):
    electrotech_misspellings = ['electro technology', 'electro tech', 'electrotech']

    if string in electrotech_misspellings:
        return('electrotechnology')
    else:
        return(string)

def fix_vet_nursing(string):
    vet_nursing_misspellings = ['vet nursing']

    if string in vet_nursing_misspellings:
        return('veterinary nursing')
    else:
        return(string)

#%%
def add_cert_details(row):
    if (row['s_fs_lev'] in [1, 2, 3, 4]) & (row['level_desc_in_fixed'] == False):
        return(row['level_description'] + " in " + row['s_fs_name_v_fixed'])
    else:
        return(row['s_fs_name_v_fixed'])

def add_dip_details(row):
    if (row['s_fs_lev'] in [6, 7]) & (row['level_desc_in_fixed'] == False):
        return(row['level_description'] + " of " + row['s_fs_name_v_fixed'])
    else:
        return(row['s_fs_name_v_fixed'])


# Combined function
# Take in a data frame, and a column name
# %%
def fix_fs_name_v(df, id = 'SurveyResponseID', colname = 's_fs_name_v'):
    
    df = df.dropna()
    # df = ~pd.isna(df[col])

    # tokenize s_fs_name_v and convert to one-token-per-row data frame
    tokenized_df = split_explode(df = df, id = id, colname = colname)

    # Fix words
    tokenized_df['tokens2'] = tokenized_df['tokens'].apply(string_subs)
    
    # Join tokens together again
    df_fixed = tokenized_df.groupby([id, colname])['tokens2'].apply(' '.join).reset_index(name = 's_fs_name_v_fixed')

    # Fix spaces before and after parentheses
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_parentheses)

    # Join df_fixed and original df
    df_fixed = pd.merge(df, df_fixed)

    # Fix common misspellings
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_ecec)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_aged_care)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_health_services)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_light_vehicle_mech)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_it)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_accounting_bookkeeping)

    # Flag whether qualification information is already in the fixed string
    df_fixed['level_description'] = df_fixed['level_description'].astype('string')
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].astype('string')
    df_fixed['level_desc_in_fixed'] = df_fixed.apply(lambda x: x.level_description in x.s_fs_name_v_fixed, axis = 1)

    # Add certificate and diploma info
    df_fixed['s_fs_name_v_fixed'] = df_fixed.apply(lambda x: add_cert_details(x), axis = 1)
    df_fixed['s_fs_name_v_fixed'] = df_fixed.apply(lambda x: add_dip_details(x), axis = 1)

    return(df_fixed)

# test
# %%
df_fixed_interim = fix_fs_name_v(df = df, id = 'id')
df_fixed_interim

# Check for common errors by looking at value_counts
# %%
counts = df_fixed_interim['s_fs_name_v_fixed'].value_counts()
counts


# %%
df_fixed_interim[df_fixed_interim['s_fs_name_v_fixed'] == 'vce year 12']

# Check if the level_description is in the fixed verbatim
# %%
# df_fixed_interim['level_description'] = df_fixed_interim['level_description'].astype('string')
# df_fixed_interim['s_fs_name_v_fixed'] = df_fixed_interim['s_fs_name_v_fixed'].astype('string')
df_fixed_interim['level_desc_in_fixed'] = df_fixed_interim.apply(lambda x: x.level_description in x.s_fs_name_v_fixed, axis = 1)
temp = df_fixed_interim[df_fixed_interim['level_desc_in_fixed'] == False]['s_fs_name_v_fixed'].value_counts()

# Harder to fix s_fs_lev 5, 8 and 9
# Can fix 1, 2, 3, 4, 6, 7
# %%
df_fixed_interim[(df_fixed_interim['level_desc_in_fixed'] == False) & (df_fixed_interim['s_fs_lev'] == 3) & (df_fixed_interim['s_fs_name_v_fixed'] == 'age care')]

# %%
