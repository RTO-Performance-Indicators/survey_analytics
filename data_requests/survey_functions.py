import pandas as pd
import numpy as np
import dask
import dask.dataframe as dd

def calc_prop(df, groups=[], vars=[], min_n=5, weighted=True, binary_conversion=False):
    
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
    long = pd.melt(df, id_vars=group_vars1, value_vars=calc_vars, value_name='value')

    # Remove invalid values (i.e. -888/-999 for unanswered/unpresented)
    long = long[long['value'] >= 0]

    if binary_conversion == True:
        long = long[long['value'] <= 5] # 6 is usually "unknown"
        long['value'] = convert_to_binary(values=long['value'])

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
    d['proportion'] = sum(x['value'] * x['weight']) / sum(x['weight'])
    d['N'] = len(x['value'])
    return pd.Series(d, index=['proportion', 'N'])
# Test
data = pd.DataFrame({
    'weight': [1, 1, 1, 1, 1],
    'variable': ['a', 'a', 'a', 'a', 'a'],
    'value': [2, 3, 4, 5, 6]
})
data.groupby('variable').apply(prop_n) # doesn't work for non-binary variables


def convert_to_binary(values):
    if set(values) == {0, 1}:
            print('Values are already binary, and proportions may be incorrect.')
            print('Consider setting binary_conversion argument to False.')
    return [0 if x > 2 else 1 for x in values]
# Test
# convert_to_binary([1, 1, 2, 2, 3])
# convert_to_binary([1, 1, 0, 0, 1])

# Test
data = pd.DataFrame({
    's_': [1, 2, 3, 4, 5, 6, 7, 8, 10, -999],
    'WEIGHT': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
})
calc_prop(df=data, groups=[], vars=['s_'])

data = pd.DataFrame({
    's_': [0, 0, 1, 0, 1, 1],
    'WEIGHT': [1, 1, 1, 1, 1, 1]
})
calc_prop(df=data, groups=[], vars=['s_'])
calc_prop(df=data, groups=[], vars=['s_'])



# data = pd.read_csv('../data/test.csv')

# or test on a larger test dataset
# import random
# size = 2000000
# data = pd.DataFrame({
#     'TOID': [random.randint(1, 3) for i in range(size)],
#     'Measure': [random.randint(0, 1) for i in range(size)],
#     'WEIGHT': [random.random() for i in range(size)]
# })

# import time
# groups = ['TOID']
# measures = ['Measure']
# %timeit calc_prop(df=data, groups=groups, vars=measures, weighted=False)