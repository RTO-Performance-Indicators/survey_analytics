import pandas as pd
import numpy as np

# set this to get rid of warnings for setting on a slice of copy (which is the desired behaviour here)
pd.options.mode.chained_assignment = None

def calc_multi_measure(df,components,output_name,preserve_NA=True):
    ''' Calculates a survey measure based on multiple components

    Calculates performance measures based on having no negative outcomes in
    a list of components. NA if all components are null, otherwise nulls treated
    as non-negative outcome. All values <1 or >5 assumed to be NA.

    Returns a pandas series 

    Args:
        df (pandas dataframe): a dataframe with columns for each measure component
        components (list): a list with the column names from df for each component
        output_name (string): the desired name of the resulting series
        preserve_NA (boolean): specifies whether to keep numerical NA values or replace with NaN

    Returns:
        A pandas series named output_name, the same length as the input 
        dataframe with binary (or NaN) values. 

    '''
    # get neccesary columns
    data = df[components].copy()

    # replace NAs. 
    if preserve_NA == False:
        # replace NAs. 
        data.mask((data <0) | (data >5),np.nan,inplace=True)
    else:
        data.mask((data >5),-999,inplace=True)

    # make 5-point variables binary. 
    # Can't just use np.where because the NaNs would be evaluated and get changed to 1 or 0.
    data.replace(2,1,inplace=True)
    data.mask((data.isin([3,4,5])),0,inplace=True)

    # this logic is a bit backwards but very concise:
    # make measure equal to 1 by default
    data[output_name] = 1
    # change rows with ANY 0 to 0 (doesn't matter whether the rest are null or 1)
    # technically this is also 
    data.loc[(data[components] == 0).any(1),output_name] = 0
    # change rows will ALL null to NaN
    if preserve_NA == False:
        data.loc[data[components].isnull().all(1),output_name] = np.nan
    else:
        data.loc[(~data[components].isin([0,1])).all(1),output_name] = -999

    return(data[output_name])

def calc_one_question_measure(df,colname,output_name,preserve_NA=True):
    ''' Calculates a survey measure based on one question.

    Calculates performance measures based on a question with responses
    on a scale of 1-5, where 1 is high and 5 is low. 
    All values <1 or >5 assumed to be NA.

    Returns a pandas series.

    Args:
        df (pandas dataframe): a dataframe with columns for each measure component
        colname (string): the name of the column in df with the input data
        output_name (string): the desired name of the resulting series
        preserve_NA (boolean): specifies whether to keep numerical NA values or replace with NaN

    Returns:
        A pandas series named output_name, the same length as the input 
        dataframe with binary (or NaN) values. 

    '''

     # get data
    data = df[colname].copy()

    # replace NAs. 
    if preserve_NA == False:
        # replace NAs. 
        data.mask((data <0) | (data >5),np.nan,inplace=True)
    else:
        data.mask((data >5),-999,inplace=True)

    # make 5-point variables binary. 
    # Can't just use np.where because the NaNs would be evaluated and get changed to 1 or 0.
    data.replace(2,1,inplace=True)
    data.mask((data.isin([3,4,5])) ,0,inplace=True)
    # rename from input variable to output name
    data.rename(output_name,inplace=True)

    return(data)

''' usage example 
(obviously you don't have to put these straight into the existing dataframe, just makes it easy to do a crosstab with src versions)

# read in survey file
file_path = '' # put the filepath here before running, suppressed here so the code can go on github without displaying S: drive structure
df = pd.read_csv(file_path, encoding = 'ISO-8859-1')

# calculate student survey measures
df['Measure5_check'] = calc_multi_measure(df,['s_sat_prob','s_sat_team','s_sat_num','s_sat_engwrt','s_sat_sc','s_sat_co'],'Measure5_check')

df['Measure9_check'] = calc_one_question_measure(df,'s_achiev','Measure9_check')

df['Measure10_check'] = calc_multi_measure(df,['s_sat_clr','s_sat_lrn','s_sat_ind'],'Measure10_check')

df['Measure12_check'] = calc_one_question_measure(df,'s_rec_to','Measure12_check')

df['Measure13_check'] = calc_multi_measure(df,['s_sat_a_clr','s_sat_a_app','s_sat_a_cout'],'Measure13_check')

df['Measure16_check'] = calc_one_question_measure(df,'s_sat_tot','Measure16_check') '''