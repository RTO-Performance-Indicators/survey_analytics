import pandas as pd
import numpy as np

def calc_student_weights(population_df,responses_df,inscope_df=None,merge_in=False):
    # this assumes the survey file is the version from src 
    # and hasn't already been merged with the admin file.
    
    if inscope_df is not None:
        # since the column name is formatted differently, set as index so it isn't duplicated in the merge
        #inscope_df.set_index('surveyresponseid',inplace=True)
        # merge and filter to those in scope
        merged = pd.merge(population_df,inscope_df,left_on='SurveyResponseID',right_index=True)
        population = merged[(merged['weighting_inscope'] ==1)].copy()
    else:
        population = population_df.copy()
    
    # make strata variables (where they're not already in the admin file)
   
    population['Weight_age'] = np.nan
    population.loc[population['Client Age'] <= 24,'Weight_age'] = '<=24'
    population.loc[(population['Client Age'] > 24) & (population['Client Age'] <= 34),'Weight_age'] = '25-34'
    population.loc[(population['Client Age'] > 34) & (population['Client Age'] <= 49),'Weight_age'] = '35-49'
    population.loc[(population['Client Age'] >= 50),'Weight_age'] = '50+'

    population['Weight_gender'] = population['Client Gender']
    population['Weight_gender'].replace('X','@',inplace=True)

    # merge strata onto responses
    wt_vars = ['CompletionStatus','Weight_age','Weight_gender','Program (Qualification/Course) Level of Education Description']
    cols = wt_vars.copy()
    cols.insert(0,'SurveyResponseID')

    responses = pd.merge(responses_df,population[cols],on='SurveyResponseID',how='left')

    # get counts of each weighting cell
    pop_strata = population.groupby(wt_vars)['SurveyResponseID'].count()
    res_strata = responses.groupby(wt_vars)['SurveyResponseID'].count()

    res_strata = res_strata.reset_index()
    weights = pd.merge(res_strata,pop_strata,left_on=wt_vars,right_index=True,how='left',suffixes=['_responses','_population'])

    weights['weight'] = weights['SurveyResponseID_population'] / weights['SurveyResponseID_responses']
    weights = weights.set_index(wt_vars)

    if merge_in == False:
        return(weights)
    
    else:
        merged_weights = pd.merge(responses, weights['weight'], left_on=wt_vars,right_index=True,how='left')
        return(merged_weights)


import string
import random

rows = 3000
responses = int(rows * 0.39)
regions = [
    'East Metro', 'North Metro', 'South Metro', 'West Metro',
    'Barwon South West', 'Gippsland', 'Grampians', 'Hume', 'Loddon Mallee'
]
industries = list(string.ascii_uppercase)[0:19]

pop_df = pd.DataFrame({
    'id': list(range(rows)),
    'region': random.choices(regions, k=rows),
    'ind': random.choices(industries, k=rows)
})

pop_df
resp_df = pd.DataFrame({
    'id': random.sample(range(rows), k=responses)
})

pop_adjustment = 1.0 # This will need to be calculated per region

pop_df
resp_df
pop_adjustment

pop_matrix = (
    pop_df
    .groupby(['region', 'ind'])
    .agg('count')
    .reset_index()
    .rename(columns={'id': 'pop'})
)

resp_matrix = (
    pop_df
    .merge(resp_df, how='inner')
    .groupby(['region', 'ind'])
    .agg('count')
    .reset_index()
    .rename(columns={'id': 'responses'})
)

pop_matrix['adj_pop'] = (pop_matrix['pop'] * pop_adjustment).astype(int)

ratios = (
    pop_matrix
    .merge(resp_matrix, how='left')
    .assign(ratio = lambda x: x['adj_pop'] / x['responses'])
)

ratios.sort_values('adj_pop')

