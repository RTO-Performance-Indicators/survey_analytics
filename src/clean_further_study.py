# The purpose of this script is to extract the further study course responses  
# from the Student Satisfaction survey
# 
# Note 1: This script can be run at any point in time as improvements are
#         made to the functions below.
#
# Note 2: The script should be updated to reflect the Survey Years
#
# Note 3: Changes to this script should be managed using GIT and GitHub
#
# Last updated: 21/09/2020

import re                           # Regular Expressions
import pandas as pd                 # Python Data Analysis Library
import numpy as np                  # Numerical Python

# Load data
filePath = 'S:/RTOPI/Both Surveys/All Final Datasets/Datasets - 2020/Output/StudentSurveys.csv'
df = pd.read_csv(filePath, encoding = 'ISO-8859-1')
df = df[np.isin(df['SurveyYear'], ['S2019', 'S2020'])]

# Select relevant columns
df = df[['SurveyResponseID', 'SurveyYear', 'TOID', 'ClientIdentifier', 'CourseID', 'SupercededCourseID','CourseCommencementDate', 's_fs_lev', 's_fs_name_v']]

# Functions
def tokenize(data = df, id = 'SurveyResponseID', col = 's_fs_name_v'):
    
    data = data[~pd.isna(data[col])]

    # Note: code frame changed between 2019 and 2020,
    #       resulting in two levels translating to 'bachelor'
    # Note: 11 is 'degree or higher', but majority are bachelor degrees,
    #       so it is set to 'bachelor
    s_fs_lev_dict = {'s_fs_lev': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                     'level_description': ['certificate i', 'certificate ii',
                                           'certificate iii', 'certificate iv',
                                           'vce or vcal', 'diploma',
                                           'advanced diploma', 'bachelor',
                                           'masters', 'other', 
                                           'bachelor']}
    s_fs_lev_dict = pd.DataFrame(s_fs_lev_dict)

    # Add level description to data,
    # and fill missing with 'Not available'
    data = pd.merge(data, s_fs_lev_dict, how = 'left')
    data['level_description'] = data['level_description'].fillna('Not available')
    
    data[col] = data[col].apply(lambda x: x.lower())
    data[col] = data[col].apply(lambda x: re.sub(r'\.', '', x))

    # tokenize
    # data['tokens'] = data[col].apply(lambda x: nltk.word_tokenize(x))
    # data['tokens'] = data[col].apply(lambda x: re.split(' |/|/.', x))
    data['tokens'] = data[col].apply(lambda x: re.split('[ .-]', x))

    # convert to narrow data
    tokenized_df = data.explode('tokens')

    return(tokenized_df)

# This is the fix applied before tokens are pasted together again
def fix_bachelor_token(string):
    
    string = str(string)

    corrected = 'bachelor'

    string = re.sub(pattern = "^achelor$", repl = corrected, string = string)

    string = re.sub(pattern = "^bac[a-z]*", repl = corrected, string = string)
    string = re.sub(pattern = "^bahelor$", repl = corrected, string = string)

    string = re.sub(pattern = "^batch$", repl = corrected, string = string)
    string = re.sub(pattern = "^batchler$", repl = corrected, string = string)

    string = re.sub(pattern = "^bauchor$", repl = corrected, string = string)
    string = re.sub(pattern = "^bechalor$", repl = corrected, string = string)
    string = re.sub(pattern = "^bechlor$", repl = corrected, string = string)
    string = re.sub(pattern = "^becholar$", repl = corrected, string = string)

    string = re.sub(pattern = "^bchelor$", repl = corrected, string = string)

    string = re.sub(pattern = "^bachelors$", repl = corrected, string = string)
    string = re.sub(pattern = "^bachelor's$", repl = corrected, string = string)

    return(string)

# This is the fix for after tokens are pasted together again
def fix_bachelor_2(string):
    string = str(string)

    corrected = r'bachelor of \1'

    string = re.sub(r'bachelor degree of ([ az19]*)', corrected, string = string)
    string = re.sub(r'bachelor degree in ([ az19]*)', corrected, string = string)

    string = re.sub(r'^degree in([ az19]*)', repl = corrected, string = string)
    string = re.sub(r'^degree of([ az19]*)', repl = corrected, string = string)

    string = re.sub(r'([a-z ]*) degree$', repl = corrected, string = string)

    return(string)

# fix_bachelor_2('associate degree in graphic design')

def fix_certificate(string):
    string = str(string)
    if string != 'certified':
        string = re.sub(pattern = "^certi$", repl = "certificate i", string = string)
        string = re.sub(pattern = "^certii$", repl = "certificate ii", string = string)
        string = re.sub(pattern = "^certiii$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^certiv$", repl = "certificate iv", string = string)
        string = re.sub(pattern = "^cert1$", repl = "certificate i", string = string)
        string = re.sub(pattern = "^cert11$", repl = "certificate ii", string = string)
        string = re.sub(pattern = "^cert111$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^cert3$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^cert4$", repl = "certificate iv", string = string)
        string = re.sub(pattern = "^cirt$", repl = "certificate iv", string = string)

        # Convert Arabic to Roman numbers
        # (mainly for certificates)
        string = re.sub(pattern = "^1$", repl = "i", string = string)
        string = re.sub(pattern = "^2$", repl = "ii", string = string)
        string = re.sub(pattern = "^3$", repl = "iii", string = string)
        string = re.sub(pattern = "^4$", repl = "iv", string = string)
        string = re.sub(pattern = "^11$", repl = "ii", string = string)
        string = re.sub(pattern = "^111$", repl = "iii", string = string)
        string = re.sub(pattern = "^1111$", repl = "iv", string = string)

        # Convert English to Roman numbers
        # (mainly for certificates)
        string = re.sub(pattern = "^one$", repl = "i", string = string)
        string = re.sub(pattern = "^two$", repl = "ii", string = string)
        string = re.sub(pattern = "^three$", repl = "iii", string = string)
        string = re.sub(pattern = "^four$", repl = "iv", string = string)

        string = re.sub(pattern = "1v", repl = "iv", string = string)
        string = re.sub(pattern = "^iiii$", repl = "iv", string = string)

        # Remaining ways of spelling 'certificate'
        string = re.sub(pattern = "^cert[a-z]*", repl = "certificate", string = string)
        string = re.sub(pattern = "^cer$", repl = "certificate", string = string)

    return(string)

def fix_diploma(string):
    string = str(string)
    string = re.sub(pattern = "dip[a-z]*", repl = "diploma", string = string)
    string = re.sub(pattern = "diaploma*", repl = "diploma", string = string)
    
    return(string)

def fix_advanced(string):
    string = str(string)
    if string in ['advance', 'adv', 'advances', 'advanved', 'advans', 'advan']:
        return('advanced')
    else:
        return(string)

def fix_associate_token(string):
    string = str(string)
    string = re.sub(pattern = '^associates$', repl = 'associate', string = string)
    string = re.sub(pattern = '^associated$', repl = 'associate', string = string)

    return(string)

def fix_associate_degree(string):
    string = str(string)

    # Change associate degree IN to associate degree OF
    string = re.sub(r'(associate degree) in ([a-z]*)' , r'\1 of \2', string)

    # Add OF after diploma if missing
    # if re.match('diploma', string):
        # if re.match('diploma of', string = string):
            # string = string
        # else:
            # string = re.sub('diploma', repl = 'diploma of', string = string)

    return(string)

# fix_associate_degree('associate degree in graphic design')


def fix_ampersand(string):
    string = str(string)
    string = re.sub(pattern = "&", repl = "and", string = string)
    
    return(string)

def fix_parentheses(string):
    string = str(string)

    string = re.sub(pattern = r'([a-z]*)\(', repl = r'\1 (', string = string)
    string = re.sub(pattern = r'\)([a-z]*)', repl = r') \1', string = string)

    return(string)

def fix_accounting_bookkeeping(string):
    string = str(string)

    corrected = r'\1accounting and bookkeeping'
    
    string = re.sub(r'(diploma of |certificate [iv]* in )accountant and bookkeeping$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )accounting + bookkeeping$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )accounting and booking ([ a-z]*)', repl = r'\1accounting and bookkeeping \2', string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )accounting and bookkeeper$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )accounting and bookmaker$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )bookkeeping and accounting$', corrected, string = string)

    string = re.sub(r'^accounting and booking ([ az]*)', repl = r'accounting and bookkeeping \1', string = string)

    return(string)

# fix_accounting_bookkeeping('accounting and booking certificate iv')

def fix_aged_care(string):
    string = str(string)

    corrected =  r'\1aged care'

    string = re.sub(r'(diploma of |certificate [iv]* in )agecare$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )agedcare$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )age care$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )aged care course$', corrected, string = string)
    
    return(string)

def fix_build_const(string):
    string = str(string)

    corrected = r'\1building and construction'

    string = re.sub(r'(diploma of |certificate [iv]* in )building construction', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )construction and building', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )building construction', corrected, string = string)

    # Specific case
    string = re.sub(r'(diploma of |certificate [iv]* in )building and construction building', r'\1building and construction (building)', string = string)

    return(string)

def fix_business(string):
    string = str(string)
    
    replace = 'business'
    
    string = re.sub(pattern = 'businedd$', repl = replace, string = string)
    string = re.sub(pattern = 'busineess$', repl = replace, string = string)
    string = re.sub(pattern = 'businiss$', repl = replace, string = string)
    string = re.sub(pattern = 'busines$', repl = replace, string = string)
    string = re.sub(pattern = 'businesa$', repl = replace, string = string)
    string = re.sub(pattern = 'businese$', repl = replace, string = string)
    string = re.sub(pattern = 'businees$', repl = replace, string = string)

    return(string)

def fix_ecec(string):
    string = str(string)
    
    corrected = r'\1early childhood education and care'

    string = re.sub(r'(diploma of |certificate [iv]* in )childcare$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )child care$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early childhood$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early childhood education$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early childhood and care$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early childhood and education$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early childhood care and education$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early education$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early education and care$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )ecec$', corrected, string = string)
    
    return(string)

def fix_electrotech(string):
    string = str(string)
    
    corrected = r'\1electrotechnology'

    string = re.sub(r'(diploma of |certificate [iv]* in )electro technology$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electro tech$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electrotech$', corrected, string = string)

    return(string)

def fix_engineering(string):
    string = str(string)

    replace = 'engineering'

    string = re.sub(pattern = 'engineeing', repl = replace, string = string)
    string = re.sub(pattern = 'engineeing,', repl = replace, string = string)
    string = re.sub(pattern = 'engineeering', repl = replace, string = string)

    return(string)

def fix_health_services(string):
    string = str(string)

    corrected = r'\1health services assistance'
    
    string = re.sub(r'(diploma of |certificate [iv]* in )health service assistance$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )health service assistant$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )health services assistance$', corrected, string = string)

    return(string)

def fix_hospitality(string):
    string = str(string)

    replace = 'hospitality'
    
    string = re.sub(pattern = 'hospiatily$', repl = replace, string = string)
    string = re.sub(pattern = 'ospotality$', repl = replace, string = string)
    string = re.sub(pattern = 'hosp$', repl = replace, string = string)
    string = re.sub(pattern = 'hospotality$', repl = replace, string = string)
    string = re.sub(pattern = 'hospitallity$', repl = replace, string = string)

    return(string)

def fix_it(string):
    string = str(string)
    
    string = re.sub(r'(diploma of |certificate [iv]* in )it$', r'\1information technology', string = string)

    return(string)

def fix_law(string):
    string = str(string)

    string = re.sub(pattern = '^laws$', repl = 'law', string = string)
    string = re.sub(pattern = '^lawz$', repl = 'law', string = string)

    return(string)

def fix_light_vehicle_mech(string):
    string = str(string)

    corrected = r'\1light vehicle mechanical technology'

    string = re.sub(r'(diploma of |certificate [iv]* in )light vehicle mechanic$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )light vehicle mechanics$', corrected, string = string)

    return(string)

def fix_nursing(string):
    string = str(string)

    corrected =  r'\1nursing'

    string = re.sub(r'(diploma of | certificate [iv]* i)nursng$', corrected, string = string)
    string = re.sub(r'nursing diploma$', 'diploma of nursing', string = string)

    return(string)

def fix_science(string):
    string = str(string)

    replace = 'science'
    
    string = re.sub(pattern = '^sciense$', repl = replace, string = string)
    string = re.sub(pattern = '^scienec$', repl = replace, string = string)
    string = re.sub(pattern = '^ofscience$', repl = replace, string = string)
    string = re.sub(pattern = '^science$,', repl = replace, string = string)
    string = re.sub(pattern = '^sciense$', repl = replace, string = string)

    return(string)

def fix_training(string):
    string = str(string)

    replace = 'training'

    string = re.sub(pattern = 'trainning', repl = replace, string = string)
    string = re.sub(pattern = 'trainng', repl = replace, string = string)

    return(string)
    
def fix_training_assessment(string):
    string = str(string)
    
    corrected = r'\1training and assessment'

    string = re.sub(r'(diploma of |certificate [iv]* in )tae$', corrected, string = string)

    return(string)

def fix_tv(string):
    string = str(string)
    
    corrected = 'television'

    string = re.sub(r'^tv$', corrected, string = string)

    return(string)

def fix_university(string):
    string = str(string)
    replace = 'university'

    string = re.sub(pattern = '^univesity$', repl = replace, string = string)
    string = re.sub(pattern = '^univeraity$', repl = replace, string = string)
    string = re.sub(pattern = '^univesities$', repl = replace, string = string)
    string = re.sub(pattern = '^university:$', repl = replace, string = string)
    string = re.sub(pattern = '^universityp$', repl = replace, string = string)
    string = re.sub(pattern = '^university,$', repl = replace, string = string)

    return(string)

def fix_vet_nursing(string):
    string = str(string)
    
    string = re.sub(r'(diploma of |certificate [iv]* in )vet nursing$', r'\1veterinary nursing', string = string)
    
    return(string)

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

def bachelor_of(x):
    string = re.sub(r'(bachelor) in ([a-z]*)' , r'\1 of \2', str(x))
    return(string)

def diploma_of(x):
    # Change diploma IN to diploma OF
    string = re.sub(r'(diploma) in ([a-z]*)' , r'\1 of \2', str(x))
    string = re.sub(r'(diploma) - ([a-z]*)' , r'\1 of \2', str(x))
    string = re.sub(r'(diploma of [a-z ]*) degree', r'\1', str(x))

    # Add OF after diploma if missing
    if re.match('diploma', string):
        if re.match('diploma of', string = string):
            string = string
        else:
            string = re.sub('diploma', repl = 'diploma of', string = string)

    return(string) 

def certificate_in(x):
    # Change cert OF to cert IN
    string = re.sub(r'(certificate [a-z]*) of ([a-z]*)' , r'\1 in \2', str(x))

    # Add IN after cert if missing
    if re.match('certificate', string):
        if re.match(r'certificate ([iv]*) in', string):
            string = string
        else:
            string = re.sub(r'certificate ([iv]*)', repl = r'certificate \1 in', string = string)

    return(string)

def fix_fs_name_v(dataframe, id = 'SurveyResponseID', col = 's_fs_name_v'):
    # Tokenize s_fs_name_v column
    tokenized_df = tokenize(dataframe, id = id, col = col)

    tokenized_df['tokens2'] = tokenized_df['tokens'].apply(fix_ampersand)

    # Fix tokens
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_bachelor_token)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_certificate)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_diploma)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_advanced)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_associate_token)

    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_business)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_engineering)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_hospitality)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_law)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_parentheses)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_science)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_training)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_tv)

    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_university)

    # Remove words
    tokenized_df = tokenized_df[~np.isin(tokenized_df['tokens2'], ['online', '\\(online\\)'])]
    tokenized_df = tokenized_df[~tokenized_df['tokens2'].str.contains('online')]


    # Join tokens together again
    group_cols = list(tokenized_df.columns.difference(['tokens', 'tokens2']))
    df_fixed = tokenized_df.groupby(group_cols)['tokens2'].apply(' '.join).reset_index(name = 's_fs_name_v_fixed')
    
    # Extract course code sequence, which may have a space before the 'vic', i.e.: 22483 vic
    df_fixed['verbatim_course_code'] = df_fixed['s_fs_name_v_fixed'].str.extract(r'([a-z]*[0-9]{4,6}[a-z]*[ ]*(?:(vic))*)')[0]
    df_fixed['verbatim_course_code'] = df_fixed['verbatim_course_code'].str.replace(' ', '')
    df_fixed['verbatim_course_code'] = df_fixed['verbatim_course_code'].str.upper()
    
    # Replace 40116 with TAE40116 (a common occurence)
    df_fixed['verbatim_course_code'] = df_fixed.apply(lambda x: 'TAE40116' if x['verbatim_course_code'] == '40116' else x['verbatim_course_code'], axis = 1)

    # Remove course code from verbatim, AFTER extraction
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].str.replace(r'([a-z]*[0-9]{4,6}[a-z]*[ ]*(?:(vic))*)', repl = "")

    # Remove white space
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].str.strip()

    # Flag whether qualification information is already in the fixed string
    df_fixed['level_desc_in_fixed'] = df_fixed.apply(lambda x: x.level_description in x.s_fs_name_v_fixed, axis = 1)

    # Add certificate and diploma info
    df_fixed['s_fs_name_v_fixed'] = df_fixed.apply(lambda x: add_cert_details(x), axis = 1)
    df_fixed['s_fs_name_v_fixed'] = df_fixed.apply(lambda x: add_dip_details(x), axis = 1)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(diploma_of)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(bachelor_of)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(certificate_in)

    # Remove level_desc_in_fixed column
    df_fixed = df_fixed.drop(['level_desc_in_fixed'], axis = 1)

    # Fix remaining errors after tokens are joined together
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_ecec)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_aged_care)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_health_services)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_nursing)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_light_vehicle_mech)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_it)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_accounting_bookkeeping)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_electrotech)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_training_assessment)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_build_const)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_bachelor_2)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_associate_degree)


    return(df_fixed)

# Fun the function above, 'fix_fs_name_v' on the data frame
temp = fix_fs_name_v(dataframe = df, id = 'SurveyResponseID', col = 's_fs_name_v')
temp = temp.drop(['level_description', 's_fs_lev', 's_fs_name_v'], axis = 1)
join_cols = list(temp.columns.difference(['s_fs_lev', 's_fs_name_v', 's_fs_name_v_fixed', 'level_description', 'verbatim_course_code']))
temp2 = pd.merge(df, temp, how = 'left',
                 left_on = join_cols, right_on = join_cols)

# Write to csv
temp2.to_csv("S:/RTOPI/Research projects/Further study/data/further_study.csv", index = False)

# Exploring the data for more improvement opportunities and bugs
temp2[~pd.isna(temp2['verbatim_course_code'])]['verbatim_course_code'].unique()

temp = tokenize(df)
temp[temp['tokens'].str.contains("assoc")]['tokens'].unique()