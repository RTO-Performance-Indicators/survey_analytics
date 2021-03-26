import pandas as pd
import numpy as np

def calc_prop(df, groups=[], vars=[], min_n=5, weighted=True):

    # Take copies of lists to avoid modifying global/environment variables
    group_vars = groups.copy()
    calc_vars = vars.copy()

    if weighted == True:
        weights = df['WEIGHT']
    else:
        weights = [1] * len(df) # unweighted = all weights are 1
    
    df['weight'] = weights
    group_vars.append('weight') # keeps weights as separate column

    # Survey data is wide; convert to long
    long = pd.melt(df, id_vars=group_vars, value_vars=calc_vars)

    # Remove invalid values (i.e. -888/-999 for unanswered/unpresented)
    long = long[(long['value'] >= 0) & (long['value'] <= 5)]

    # Convert from 5-scale likert to binary via merge
    # NOTE: Has not effect binary columns, because 0 -> 0 and 1 -> 1
    likert_to_binary = pd.DataFrame({
        'value' : [0, 1, 2, 3, 4, 5], 
        'binary': [0, 1, 1, 0, 0, 0]
    })
    long = pd.merge(long, likert_to_binary, how='left')

    # Conversion to long format gathers measures into one column, 'variable'
    # 'variable' column needs to be added as a grouping variable
    group_vars.append('variable')
    
    # Calculate proportions and N
    result_long = long.groupby(group_vars).apply(prop_n)

    # Convert proportion to NA if N < min_n
    result_long.loc[result_long['N'] < min_n, 'proportion'] = np.nan

    return(result_long)

# calculates proportion and N
def prop_n(x):
    d = {}
    d['proportion'] = sum(x['binary'] * x['weight']) / sum(x['weight'])
    d['N'] = len(x['binary'])
    return pd.Series(d, index=['proportion', 'N'])

# Test
# data = pd.read_csv('../data/test.csv')

# groups = ['TOID']
# measures = ['Measure']
# calc_prop(df=data, groups=groups, vars=measures, weighted=False)