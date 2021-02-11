

def calc_prop(df, group_vars = [], vars = [], weighted = True):

    import pandas as pd
    import numpy as np

    id_vars = group_vars.copy()

    if weighted == True:
        id_vars.append('WEIGHT')

    # Survey data is tidy; convert to long format
    long = pd.melt(df, id_vars = id_vars, value_vars = vars)

    # Remove invalid values (i.e. -888/-999 for unanswered / unpresented questions)
    long = long[(long['value'] >= 0) & (long['value'] <= 5)]

    # Convert from 5-scale likert to binary
    # NOTE: Does not affect binary columns, because 0 -> 0 and 1 -> 1
    likert_to_binary = pd.DataFrame({'value' : [0, 1, 2, 3, 4, 5], 'binary': [0, 1, 1, 0, 0, 0]})
    long = pd.merge(long, likert_to_binary)

    # 'variable' column needs to be added as a grouping variable
    group_vars.append('variable')

    # Calculate N
    n = long.groupby(group_vars).apply(lambda x: len(x['value'])).reset_index().rename(columns = {0: 'N'})
    
    # Calculate proportion, depending if weighting is required
    if weighted == True:
        prop = long.groupby(group_vars).apply(lambda x: sum(x['binary'] * x['WEIGHT']) / sum(x['WEIGHT'])).reset_index().rename(columns = {0: 'proportion'})
    else:
        prop = long.groupby(group_vars).apply(lambda x: sum(x['binary']) / len(x['value'])).reset_index().rename(columns = {0: 'proportion'})

    result_long = pd.merge(prop, n)

    result_long['proportion'] = result_long.apply(lambda x: np.nan if x['N'] < 5 else x['proportion'], axis = 1)

    return(result_long)