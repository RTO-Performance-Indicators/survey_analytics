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
filepath <- paste0("\\\\education.vic.gov.au/SHARE/HESG/Projects/PEU/",
                   "RTOPI/Both Surveys/All Final Datasets/",
                   "Datasets - 2020/Output/StudentSurveys.csv")
StudentSurvey  <- read.csv(filepath, stringsAsFactors = FALSE)
df = pd.read_csv(filePath, encoding = 'ISO-8859-1')
df = df[np.isin(df['SurveyYear'], ['S2019', 'S2020'])]

# Select relevant columns
df = df[['SurveyResponseID', 'SurveyYear', 'TOID', 'ClientIdentifier', 'CourseID', 'SupercededCourseID', 'CourseLevelDesc', 'CourseCommencementDate', 's_fs_lev', 's_fs_name_v']]

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
    data[col] = data[col].apply(lambda x: re.sub(r'[.,:_?]+', '', x))

    # tokenize
    # data['tokens'] = data[col].apply(lambda x: nltk.word_tokenize(x))
    # data['tokens'] = data[col].apply(lambda x: re.split(' |/|/.', x))
    data['tokens'] = data[col].apply(lambda x: re.split('[ .-]+', x))

    # convert to narrow data
    tokenized_df = data.explode('tokens')

    return(tokenized_df)

def arabic_to_roman(token):
    token = re.sub(pattern = '^1v$', repl = 'iv', string = token)
    token = re.sub(pattern = '^1111$', repl = 'iv', string = token)
    token = re.sub(pattern = '^111$', repl = 'iii', string = token)
    token = re.sub(pattern = '^11$', repl = 'ii', string = token)
    token = re.sub(pattern = '^1$', repl = 'i', string = token)

    token = re.sub(pattern = '\|\|\|', repl = 'iii', string = token)
    token = re.sub(pattern = '\|\|', repl = 'ii', string = token)
    token = re.sub(pattern = '\|', repl = 'i', string = token)

    return(token)

# arabic_to_roman('|||')
# re.sub(pattern = '\|\|\|', repl = 'iii', string = '|||')

def fix_roman(token):
    token = re.sub(pattern = '^lv$', repl = 'iv', string = token)
    token = re.sub(pattern = '^lll$', repl = 'iii', string = token)
    token = re.sub(pattern = '^ll$', repl = 'ii', string = token)
    token = re.sub(pattern = '^l$', repl = 'i', string = token)

    return(token)

# fix_roman('ll')

# This is the fix applied before tokens are pasted together again
def fix_bachelor_token(string):
    
    string = str(string)

    corrected = 'bachelor'

    string = re.sub(pattern = "^achelor$", repl = corrected, string = string)

    string = re.sub(pattern = "^bac[a-z]*", repl = corrected, string = string)
    string = re.sub(pattern = "^bahelor$", repl = corrected, string = string)

    string = re.sub(pattern = "^batch$", repl = corrected, string = string)
    string = re.sub(pattern = "^batchelor$", repl = corrected, string = string)
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

def fix_certificate(string):
    string = str(string)
    if string != 'certified':
        string = re.sub(pattern = "^c1$", repl = "certificate i", string = string)
        string = re.sub(pattern = "^c2$", repl = "certificate ii", string = string)
        string = re.sub(pattern = "^c3$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^c4$", repl = "certificate iv", string = string)

        string = re.sub(pattern = "^centeficate$", repl = "certificate", string = string)
        string = re.sub(pattern = "^certi$", repl = "certificate i", string = string)
        string = re.sub(pattern = "^certii$", repl = "certificate ii", string = string)
        string = re.sub(pattern = "^certiii$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^certiv$", repl = "certificate iv", string = string)
        string = re.sub(pattern = "^cert1$", repl = "certificate i", string = string)
        string = re.sub(pattern = "^cert11$", repl = "certificate ii", string = string)
        string = re.sub(pattern = "^cert111$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^cert2$", repl = "certificate ii", string = string)
        string = re.sub(pattern = "^cert3$", repl = "certificate iii", string = string)
        string = re.sub(pattern = "^cert4$", repl = "certificate iv", string = string)
        string = re.sub(pattern = "^cetificate$", repl = "certificate", string = string)
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

        # lack of spaces
        string = re.sub(pattern = '4in', repl = 'iv in', string = string)
        string = re.sub(pattern = '3in', repl = 'iii in', string = string)
        string = re.sub(pattern = '2in', repl = 'ii in', string = string)
        string = re.sub(pattern = '1in', repl = 'i in', string = string)
        string = re.sub(pattern = '4of', repl = 'iv in', string = string)
        string = re.sub(pattern = '3of', repl = 'iii in', string = string)
        string = re.sub(pattern = '2of', repl = 'ii in', string = string)
        string = re.sub(pattern = '1of', repl = 'i in', string = string)

    return(string)

# fix_certificate('C4349 Certificate IV in Education Support')

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

def fix_ampersand(string):
    string = str(string)
    
    string = re.sub(pattern = "&", repl = "and", string = string)
    string = re.sub(pattern = "\+", repl = "and", string = string)
    
    return(string)

# fix_ampersand('certificate iv in accounting + bookkeeping')

def fix_accounting_bookkeeping(string):
    string = str(string)

    corrected = r'\1 accounting and bookkeeping'
    
    string = re.sub(r'(in|of) account and[a-z ]*', repl = corrected, string = string)
    string = re.sub(r'(in|of) accountant and[a-z ]*', repl = corrected, string = string)
    string = re.sub(r'(in|of) accounting + book[a-z ]*', repl = corrected, string = string)
    string = re.sub(r'(in|of) accounting and book[ a-z]*', repl = corrected, string = string)
    string = re.sub(r'(in|of) book[ a-z]*', repl = corrected, string = string)

    return(string)

# fix_accounting_bookkeeping('certificate iv in account and bookkeeping')
# fix_accounting_bookkeeping('advanced diploma of accountant and bookkeeping')

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

    corrected = r'\1 building and construction'

    string = re.sub(r'(of|in) building and con[a-z]* ', corrected, string = string)
    string = re.sub(r'(of|in) building con[a-z]*', corrected, string = string)
    string = re.sub(r'(of|in) construction and building', corrected, string = string)
    string = re.sub(r'(of|in) building construction', corrected, string = string)

    # Specific case
    string = re.sub(r'(diploma of |certificate [iv]* in )building and construction building', r'\1building and construction (building)', string = string)

    return(string)

# fix_build_const('certificate iv in building construcrion')
# fix_build_const('certificate iv in building construction (building)')

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

def fix_child_intervention(string):
    string = str(string)

    replace = r'\1 child, youth and family intervention'

    string = re.sub(pattern = '(in|of) child and y[ a-z]*', repl = replace, string = string)
    string = re.sub(pattern = '(in|of) child family[ a-z]*', repl = replace, string = string)
    string = re.sub(pattern = '(in|of) child health[ a-z]*', repl = replace, string = string)
    string = re.sub(pattern = '(in|of) child youth[ a-z]*', repl = replace, string = string)
    string = re.sub(pattern = '(in|of) childyou[ a-z]*', repl = replace, string = string)

    return(string)

# fix_child_intervention('certificate iv in child youth and family intervention')

def fix_community(string):
    string = str(string)

    replace = 'community'

    string = re.sub(pattern = '^communityservices*', repl = 'community services', string = string)
    string = re.sub(pattern = '^communiy', repl = 'community', string = string)
    string = re.sub(pattern = '^communut[a-z1-9]*', repl = 'community', string = string)
    string = re.sub(pattern = '^communit[a-z1-9]*', repl = 'community', string = string)
    string = re.sub(pattern = '^communt[a-z1-9]*', repl = 'community', string = string)


    return(string)

def fix_cybersecurity(string):
    string = str(string)

    string = re.sub(pattern = '^cybersecurity*', repl = 'cyber security', string = string)

    return(string)

def fix_ecec(string):
    string = str(string)
    
    corrected = r'\1early childhood education and care'

    string = re.sub(r'(diploma of |certificate [iv]* in )child care[a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )chile care$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )childcare[a-z ]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )childhood[a-z ]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )earlt[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early chi[ a-z]*', corrected, string = string)
    # string = re.sub(r'(diploma of |certificate [iv]* in )early childhood[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early education[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early learning[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early vhildhood[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )early year[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )earlych[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )earlyhood[ a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )eary child[ a-z]*', corrected, string = string)
    
    string = re.sub(r'(diploma of |certificate [iv]* in )cc$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )ecc[a-z ]*$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )ece[a-z ]*', corrected, string = string)
    
    return(string)

def fix_electrotech(string):
    string = str(string)
    
    corrected = r'\1electrotechnology'

    string = re.sub(r'(diploma of |certificate [iv]* in )electro technology$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electro tech$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electrote[a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electrt[a-z]*', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electrology$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electricte[a-z]*$', corrected, string = string)
    string = re.sub(r'(diploma of |certificate [iv]* in )electritech[a-z]*$', corrected, string = string)

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

def fix_ind_supp(string):
    string = str(string)

    replace = 'individual support'

    string = re.sub(pattern = 'ind su[a-z ]*', repl = replace, string = string)
    string = re.sub(pattern = 'individual[a-z ]*', repl = replace, string = string)
    string = re.sub(pattern = 'indiv[a-z ]*', repl = replace, string = string)
    string = re.sub(pattern = 'indov[a-z ]*', repl = replace, string = string)

    return(string)

# fix_ind_supp('certificate iii in ind support')
# fix_ind_supp('certificate iii in indovidual support')
# fix_ind_supp('certificate iii in indivual support')

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

def fix_parentheses(string):
    string = str(string)

    string = re.sub(pattern = '\( ', repl = '(', string = string)
    string = re.sub(pattern = ' \)', repl = ')', string = string)

    return(string)

# fix_parentheses('( access )')

def fix_science(string):
    string = str(string)

    replace = 'science'
    
    string = re.sub(pattern = '^sccienc[a-z]*', repl = replace, string = string)
    string = re.sub(pattern = '^sciences$', repl = replace, string = string)
    string = re.sub(pattern = '^sciense$', repl = replace, string = string)
    string = re.sub(pattern = '^scienec$', repl = replace, string = string)
    string = re.sub(pattern = '^ofscience$', repl = 'of science', string = string)
    string = re.sub(pattern = '^science$,', repl = replace, string = string)
    string = re.sub(pattern = '^sciense$', repl = replace, string = string)

    return(string)

# Miscellaneous spelling errors
# Can be applied at tokenized stage AND joined stage
def fix_spelling(string):
    string = str(string)

    string = re.sub(pattern = 'accountting', repl = 'accounting', string = string)
    string = re.sub(pattern = 'accountimg', repl = 'accounting', string = string)
    string = re.sub(pattern = 'adaults', repl = 'adults', string = string)
    string = re.sub(pattern = 'aging', repl = 'ageing', string = string)
    string = re.sub(pattern = 'aldults', repl = 'adults', string = string)
    string = re.sub(pattern = 'asults', repl = 'adults', string = string)
    string = re.sub(pattern = 'asvanced', repl = 'advanced', string = string)
    string = re.sub(pattern = 'brick lay[a-z]*', repl = 'bricklaying', string = string)
    string = re.sub(pattern = 'brick ly[a-z]*', repl = 'bricklaying', string = string)
    string = re.sub(pattern = 'cetificate', repl = 'certificate', string = string)
    string = re.sub(pattern = 'constructionmanagement', repl = 'construction management', string = string)
    string = re.sub(pattern = 'constru[a-z]*', repl = 'construction', string = string) # Must be done after 'constructionmanagement'
    string = re.sub(pattern = 'deploma', repl = 'diploma', string = string)
    string = re.sub(pattern = 'deploys', repl = 'diploma', string = string)
    string = re.sub(pattern = 'dimploma', repl = 'diploma', string = string)
    string = re.sub(pattern = 'dioloma', repl = 'diploma', string = string)
    string = re.sub(pattern = 'electrotech[a-z]*', repl = 'electrotechnology', string = string)
    string = re.sub(pattern = 'genural', repl = 'general', string = string)
    string = re.sub(pattern = 'gereral', repl = 'general', string = string)
    string = re.sub(pattern = '^inf[a-z]+tion$', repl = 'information', string = string)
    string = re.sub(pattern = 'infrastucture', repl = 'infrastructure', string = string)
    string = re.sub(pattern = 'litracy', repl = 'literacy', string = string)
    string = re.sub(pattern = 'machanic', repl = 'mechanic', string = string)
    string = re.sub(pattern = 'menchindiching', repl = 'merchandising', string = string)
    string = re.sub(pattern = 'merchendising', repl = 'merchandising', string = string)
    string = re.sub(pattern = 'nmueracy', repl = 'numeracy', string = string)
    string = re.sub(pattern = 'pre app[a-z]*', repl = 'pre-apprenticeship', string = string)
    string = re.sub(pattern = 'preapp[a-z]*', repl = 'pre-apprenticeship', string = string)

    string = re.sub(pattern = 'supoport', repl = 'support', string = string)
    string = re.sub(pattern = '^tech[a-z]+gy$', repl = 'technology', string = string)
    string = re.sub(pattern = 'work ed[a-z]*', repl = 'work education', string = string)
    string = re.sub(pattern = 'writen', repl = 'written', string = string)
    

    return(string)

# fix_spelling('certificate ii in electrotechnology')
# fix_spelling('certificate ii in electrotechnolo (career start)')

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

def fix_very(token):
    return(re.sub('^very$', repl = 'certificate', string = token))

# fix_very('very')

def fix_vet_nursing(string):
    string = str(string)
    
    string = re.sub(r'(diploma of |certificate [iv]* in )vet nursing$', r'\1veterinary nursing', string = string)
    
    return(string)

def add_cert_details(row):
    import re

    if(row['s_fs_lev'] in [1, 2, 3, 4]) & (row['level_desc_in_fixed'] == False):
        if re.search('^certificate in', row['s_fs_name_v_fixed']):
            fs = re.sub('^certificate in', '', row['s_fs_name_v_fixed'])
            fs = row['level_description'] + ' in' + fs
        elif re.search('[a-z ]* certificate$', row['s_fs_name_v_fixed']):
            fs = re.sub(' certificate', '', row['s_fs_name_v_fixed'])
            fs = row['level_description'] + ' in ' + fs
        elif re.search('^[iv]+', row['s_fs_name_v_fixed']):
            fs = re.sub(r'^([iv]+)', r'certificate \1', row['s_fs_name_v_fixed'])
        
        # Sometimes the level_description doesn't match the verbatim
        # in these cases, stick with verbatim 
        # as in these situations s_fs_lev is more often incorrect
        elif re.search('^certificate [iv]+', row['s_fs_name_v_fixed']):
            fs = row['s_fs_name_v_fixed']
        elif re.search('diploma', row['s_fs_name_v_fixed']):
            fs = row['s_fs_name_v_fixed']
        else:
            fs = row['level_description'] + ' in ' + row['s_fs_name_v_fixed']
    else:
        fs = row['s_fs_name_v_fixed']

    return(fs)

# test = {'s_fs_lev': [1, 2, 2, 3, 4],
#         's_fs_name_v_fixed': ['certificate i in x',
#                               'certificate in x',
#                               'x certificate',
#                               'diploma of x',
#                               'iv in disability'],
#         'level_description': ['certificate i', 'certificate ii', 'certificate ii', 'certificate iii', 'certificate iv'],
#         'level_desc_in_fixed': [True, False, False, False, False]
#         }
# test_df = pd.DataFrame(test)
# test_df['fixed'] = test_df.apply(lambda x: add_cert_details(x), axis = 1)
# test_df

def add_dip_details(row):
    if row['s_fs_lev'] in [6, 7]:
        if row['level_desc_in_fixed'] == True:
            if re.search(r'advanced diploma([a-z ]*)', string = row['s_fs_name_v_fixed']):
                fs = row['s_fs_name_v_fixed']
            elif re.search('([a-z ]*) advanced diploma', string = row['s_fs_name_v_fixed']):
                fs = re.sub(r'([a-z ]*) advanced diploma', repl = r'advanced diploma of \1', string = row['s_fs_name_v_fixed'])
            elif re.search('([a-z ]*) diploma', string = row['s_fs_name_v_fixed']):
                fs = re.sub(r'([a-z ]*) diploma', repl = r'diploma of \1', string = row['s_fs_name_v_fixed'])
            else:
                fs = row['s_fs_name_v_fixed']
        else:
            if re.search('diploma', string = row['s_fs_name_v_fixed']):
                if re.search('diploma of', string = row['s_fs_name_v_fixed']):
                    fs = row['s_fs_name_v_fixed']
                else:
                    fs = re.sub('diploma', repl = 'diploma of', string = row['s_fs_name_v_fixed'])
            elif re.search('certificate', string = row['s_fs_name_v_fixed']):
                fs = row['s_fs_name_v_fixed']
            else:
                fs = row['level_description'] + ' of ' + row['s_fs_name_v_fixed']
    else:
        fs = row['s_fs_name_v_fixed']
    return(fs)

# test = {'s_fs_lev': [6, 7, 6, 7, 7],
#         's_fs_name_v_fixed': ['diploma of x',
#                               'advanced diploma',
#                               'advanced diploma x',
#                               'advanced diploma of x',
#                               'x'],
#         'level_description': ['diploma', 'advanced diploma', 'advanced diploma', 'diploma', 'advanced diploma'],
#         'level_desc_in_fixed': [True, True, False, True, False],
#         'expected': ['diploma of x', 'certificate in x', 'advanced diploma of x', 'advanced diploma of x', 'advanced diploma of x']
#         }
# test_df = pd.DataFrame(test)
# test_df['fixed'] = test_df.apply(lambda x: add_dip_details(x), axis = 1)
# test_df

# Intended to...?
def add_spaces(string):
    string = str(string)

    string = re.sub(r'([1-4])([a-z]*)', repl = r'\1 \2', string = string)
    string = re.sub(r'([a-z])([1-4])', repl = r'\1 \2', string = string)

    # Deprecated (moved to arabic_to_roman function)
    # string = re.sub(pattern = "^4$", repl = "iv", string = string)
    # string = re.sub(pattern = "^3$", repl = "iii", string = string)
    # string = re.sub(pattern = "^2$", repl = "ii", string = string)
    # string = re.sub(pattern = "^1$", repl = "i", string = string)

    return(string)

add_spaces('22251certificate')

def bachelor_of(x):
    string = re.sub(r'(bachelor) in ([a-z]*)' , r'\1 of \2', str(x))
    return(string)

# Deprecated
def diploma_of(x):
    # Change diploma IN to diploma OF
    string = re.sub(r'(diploma) in ([a-z ]*)' , r'\1 of \2', str(x))
    string = re.sub(r'(diploma) - ([a-z ]*)' , r'\1 of \2', string)
    string = re.sub(r'(diploma of [a-z ]*) degree', r'\1', string)

    # Add OF after diploma if missing
    if re.search('^advanced diploma$', string):
        string = string
    elif re.search('^diploma$', string):
        string = string
    elif re.search('diploma', string = string):
        if re.search('diploma of', string = string):
            string = string
        else:
            string = re.sub('diploma', repl = 'diploma of', string = string)
    else:
        string = string

    return(string) 

# diploma_of('advanced diploma accounting')

# deprecated
def certificate_in(x):
    # Change cert OF to cert IN
    string = re.sub(r'(certificate [iv]+) of ([a-z]*)' , r'\1 in \2', str(x))

    # Add IN after cert if missing
    if re.match('certificate', string):
        if re.search(r'certificate ([iv]+) in ', string):
            string = string
        else:
            string = re.sub(r'certificate ([iv]+) ([a-z]*)', repl = r'certificate \1 in \2', string = string)

    return(string)

# certificate_in('certificate iii individual support')
# certificate_in('certificate iv in individual support')

# TODO
def masters_of(x):

    string = str(x)

    return(string)

# deprecated
# def reposition_qual_level(x):

#     string = re.sub(r'([ a-z]*) (diploma)', r'\2 of \1', str(x))
#     string = re.sub(r'([ a-z]*) (certificate [iv]*)', r'\2 in \1', string)

#     return(string)

# reposition_qual_level('advanced diploma')

def remove_meaningless_names(x):
    meaningless_name = bool(re.search("^(certificate|diploma) [ iv]*(in|of)$", x))

    if meaningless_name == True:
        return('')
    else:
        return(x)

def fix_fs_name_v(dataframe, id = 'SurveyResponseID', col = 's_fs_name_v'):
    # Tokenize s_fs_name_v column
    tokenized_df = tokenize(dataframe, id = id, col = col)

    # Fix tokens
    tokenized_df['tokens2'] = tokenized_df['tokens'].apply(fix_ampersand)
    tokenized_df['tokens2'] = tokenized_df['tokens'].apply(arabic_to_roman)
    tokenized_df['tokens2'] = tokenized_df['tokens'].apply(fix_roman)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_bachelor_token)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_certificate)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_diploma)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_advanced)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_associate_token)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_very)

    # Is this doing more harm than good?
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(add_spaces)

    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_business)
    tokenized_df['tokens2'] = tokenized_df['tokens2'].apply(fix_community)
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
    
    # Remove words/ngrams
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].str.replace('part time', repl = '')

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
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_ampersand)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_ecec)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_aged_care)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_child_intervention)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_cybersecurity)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_health_services)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_nursing)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_light_vehicle_mech)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_it)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_ind_supp)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_accounting_bookkeeping)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_electrotech)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_training_assessment)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_build_const)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_bachelor_2)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_associate_degree)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_spelling)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_ampersand)
    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(fix_parentheses)

    df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(remove_meaningless_names)
    # df_fixed['s_fs_name_v_fixed'] = df_fixed['s_fs_name_v_fixed'].apply(reposition_qual_level) # DEPRECATED

    return(df_fixed)

# SECTION 1 - CLEAN S_FS_NAME_V
fs = fix_fs_name_v(dataframe = df, id = 'SurveyResponseID', col = 's_fs_name_v')
fs = fs.drop(['s_fs_lev', 's_fs_name_v'], axis = 1)
join_cols = list(fs.columns.difference(['level_description', 's_fs_lev', 's_fs_name_v', 's_fs_name_v_fixed', 'level_description', 'verbatim_course_code']))
fs = pd.merge(df, fs, how = 'left', left_on = join_cols, right_on = join_cols)

# SECTION 2 - REPLACE COURSE NAME USING COURSE CODES SUPPLIED IN VERBATIM

# Load and superseded course concordances
superseded = pd.read_excel('S:/TMIPU/Info Library/ISA Data & Information/Superseded Mappings/TGA Superseded Mappings - December 2020 - All courses.xlsx',
                            sheet_name = 'Only 1 allocation')
superseded['LatestCourseTitle'] = superseded['LatestCourseTitle'].str.lower()

# Not all extracted verbatim course codes are valid course codes, such as 2019 and 2020
# Remove years as valid superseded course codes
superseded = superseded[~np.isin(superseded['Course'], ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])]

# Merge superseded course title to fs data frame
fs_merged = pd.merge(fs, superseded[['Course', 'LatestCourseTitle']], left_on = ['verbatim_course_code'], right_on = ['Course'], how = 'left')

# Now replace s_fs_name_v_fixed if LatestCourseTitle is not na
fs_merged['s_fs_name_v_fixed'] = fs_merged.apply(lambda x: x['LatestCourseTitle'] if pd.isna(x['LatestCourseTitle']) == False else x['s_fs_name_v_fixed'], axis = 1)
fs_merged = fs_merged.drop(['verbatim_course_code', 'Course', 'LatestCourseTitle'], axis = 1)


# FINAL SECTION - Write to csv
fs_merged.to_csv("S:/RTOPI/Research projects/Further study/data/further_study.csv", index = False)

# Exploring the data for more improvement opportunities and bugs
fs_merged['s_fs_name_v_fixed'] = fs_merged.apply(lambda x: '' if pd.isna(x['s_fs_name_v_fixed']) == True else x['s_fs_name_v_fixed'], axis = 1)
fs_merged['s_fs_name_v'] = fs_merged.apply(lambda x: '' if pd.isna(x['s_fs_name_v']) == True else x['s_fs_name_v'], axis = 1)

fs_merged[fs_merged['s_fs_name_v_fixed'].str.contains('edu')]
fs_merged[fs_merged['s_fs_name_v_fixed'].str.contains('diploma of advanced diploma')]

fs_merged[(fs_merged['SupercededCourseID'] == '22334VIC') & (fs_merged['s_fs_lev'] > 0)]
    
# At [an RTO]
fs[fs['s_fs_name_v_fixed'].str.match('[a-z ]+ at [a-z]+')]

fs_merged[fs_merged['s_fs_name_v_fixed'] == 'diploma of advanced']
fs_merged[fs_merged['s_fs_name_v_fixed'].str.contains('certificate i in in')][['s_fs_name_v', 'level_description', 's_fs_name_v_fixed']]

fs_merged[fs_merged['s_fs_name_v_fixed'].str.contains('i am')][['s_fs_name_v', 'level_description', 's_fs_name_v_fixed']]
fs_merged[fs_merged['s_fs_name_v_fixed'].str.contains('i have')][['s_fs_name_v', 'level_description', 's_fs_name_v_fixed']]

# > 200 students are studying the same course.
# Should these actually be 'further study'?
fs_merged[fs_merged['s_fs_name_v_fixed'].str.contains('same')][['s_fs_name_v', 'level_description', 's_fs_name_v_fixed']]

fs_merged[fs_merged['SurveyResponseID'] == 'S031033']

tokenized_df[tokenized_df['SurveyResponseID'] == 'S126502']
df_fixed[df_fixed['SurveyResponseID'] == 'S126502']

