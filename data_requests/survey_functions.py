import pandas as pd
import numpy as np
import dask
import dask.dataframe as dd

def calc_prop(df, groups=[], vars=[], min_n=5, weighted=True):

    # Take copies of lists to avoid modifying global/environment variables
    group_vars1 = groups.copy()
    group_vars2 = groups.copy()
    calc_vars = vars.copy()

    if weighted == True:
        weights = df['WEIGHT']
    else:
        weights = [1] * len(df) # unweighted: all weights are equal to 1
    
    df['weight'] = weights
    group_vars1.append('weight') # keeps weights as separate column

    # Survey data is wide; convert to long format
    long = pd.melt(df, id_vars=group_vars1, value_vars=calc_vars)

    # Remove invalid values (i.e. -888/-999 for unanswered/unpresented)
    long = long[(long['value'] >= 0) & (long['value'] <= 5)]

    # Convert from 5-scale likert to binary via merge
    # NOTE: Does not affect binary variables, because 0 -> 0 and 1 -> 1
    likert_to_binary = pd.DataFrame({
        'value' : [0, 1, 2, 3, 4, 5], 
        'binary': [0, 1, 1, 0, 0, 0]
    })
    long = pd.merge(long, likert_to_binary, how='left')

    # Conversion to long format gathers measures into one column, 'variable'
    # 'variable' column needs to be added as a grouping variable
    group_vars2.append('variable')
    
    # Calculate proportions and N
    result_long = long.groupby(group_vars2).apply(prop_n)

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
# calc_prop(df=data, groups=[], vars=measures, weighted=True)


# Create a larger test dataset
# import random
# size = 1000000
# data = pd.DataFrame({
#     'TOID': [random.randint(1, 3) for i in range(size)],
#     'Measure': [random.randint(0, 1) for i in range(size)],
#     'WEIGHT': [random.random() for i in range(size)]
# })

# import time
# groups = ['TOID']
# measures = ['Measure']
# calc_prop(df=data, groups=groups, vars=measures, weighted=False)
# %timeit calc_prop(df=data, groups=groups, vars=measures, weighted=False)

# DASK version
def calc_prop_dask(df, groups=[], vars=[], min_n=5, weighted=True):
    
    # Take copies of lists to avoid modifying global/environment variables
    group_vars = groups.copy()
    calc_vars = vars.copy()

    if weighted == True:
        weights = df['WEIGHT']
    else:
        weights = [1] * len(df) # unweighted: all weights are equal to 1
    
    df['weight'] = weights
    group_vars.append('weight') # keeps weights as separate column

    # Convert to dask dataframe
    df = dd.from_pandas(df, npartitions=4)

    # Survey data is wide; convert to long format
    # long = pd.melt(df, id_vars=group_vars, value_vars=calc_vars)
    long = df.melt(id_vars=group_vars, value_vars=calc_vars)

    # Remove invalid values (i.e. -888/-999 for unanswered/unpresented)
    long = long[(long['value'] >= 0) & (long['value'] <= 5)]

    # Convert from 5-scale likert to binary via merge
    # NOTE: Does not affect binary variables, because 0 -> 0 and 1 -> 1
    likert_to_binary = pd.DataFrame({
        'value' : [0, 1, 2, 3, 4, 5], 
        'binary': [0, 1, 1, 0, 0, 0]
    })
    likert_to_binary = dd.from_pandas(likert_to_binary, npartitions=1)
    long = long.merge(likert_to_binary)

    # Conversion to long format gathers measures into one column, 'variable'
    # 'variable' column needs to be added as a grouping variable
    group_vars.append('variable')

    # Calculate proportions and N
    result_long = long.groupby(group_vars).apply(prop_n, meta={'proportion': 'float', 'N': 'int'}).compute()

    # Convert proportion to NA if N < min_n
    result_long.loc[result_long['N'] < min_n, 'proportion'] = np.nan

    return(result_long)

# `calc_prop_dask(df=data, groups=groups, vars=measures, weighted=False)

# %timeit calc_prop(df=data, groups=groups, vars=measures, weighted=False)
# %timeit calc_prop_dask(df=data, groups=groups, vars=measures, weighted=False)`