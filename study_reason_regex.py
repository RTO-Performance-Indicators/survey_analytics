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

# Function to take in a vector of text
# to return a cleaned vector of text
#%%
def process_further_study_verbatim(s_fs_v):

    # Remove punctuations

    # Remove white space at either end of string

    # Remove extra spaces between words

    # Different spelling for Bachelor

    return(s_fs_v)