import pandas as pd
import numpy as np
import dask
import dask.dataframe as dd

def calc_prop(df, groups=[], vars=[], min_n=5, weighted=True, binary_conversion=False):
    
    if weighted == True:
        weights = df['WEIGHT']
    else:
        weights = [1] * len(df) # unweighted: all weights = 1
    
    df['weight'] = weights
    
    # Survey data is wide; convert to long format
    long = pd.melt(df, id_vars=groups + ['weight'], value_vars=vars, value_name='value')

    # Remove invalid values (i.e. -888/-999 for unanswered/unpresented)
    long = long[long['value'] >= 0]

    if binary_conversion == True:
        long = long[long['value'] <= 5] # 6 is usually "unknown"
        long['value'] = convert_to_binary(values=long['value'])
   
    # Calculate proportions and N
    result = calculate_proportion_ns(long, groups=groups)
    
    # Convert proportion to NA if N < min_n
    result.loc[result_long['N'] < min_n, 'proportion'] = np.nan

    return(result)

def convert_to_binary(values):
    if set(values) == {0, 1}:
            print('Values are already binary, and proportions may be incorrect.')
            print('Consider setting binary_conversion argument to False.')
    return [0 if x > 2 else 1 for x in values]
# Test
# convert_to_binary([1, 1, 2, 2, 3])
# convert_to_binary([1, 1, 0, 0, 1])

# calculates proportion and N
def calculate_proportion_ns(df, groups):
    sum_n = (
        df
        .groupby(groups + ['variable', 'value'], as_index=False)['weight']
        .aggregate([sum, np.size])
        .rename(columns={'sum': 'sum_weights', 'size': 'n'})
    )

    grouped = sum_n.groupby(groups + ['variable'])
    sum_n['proportion'] = grouped['sum_weights'].transform(lambda x: x / sum(x))
    sum_n['N'] = grouped['n'].transform('sum')
    
    return sum_n

# Test
# data = pd.DataFrame({
#     'weight': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     'variable': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
#     'value': [0, 0, 1, 1, 1, 0, 1, 1, 0, 0]
# })
# data = pd.DataFrame({
#     'weight': [1, 1, 1, 1, 1],
#     'variable': ['a', 'a', 'a', 'a', 'a'],
#     'value': [2, 3, 4, 5, 6]
# })
# calculate_proportion_ns(data, groups=[])

# Test
# data = pd.DataFrame({
#     's_': [1, 2, 3, 4, 5, 6, 7, 8, 10, -999],
#     'WEIGHT': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# })
# calc_prop(df=data, groups=[], vars=['s_'])

# data = pd.DataFrame({
#     's_': [0, 0, 1, 0, 1, 1],
#     'WEIGHT': [1, 1, 1, 1, 1, 1]
# })
# calc_prop(df=data, groups=[], vars=['s_'])
# calc_prop(df=data, groups=[], vars=['s_'], binary_conversion=True)

# data = pd.read_csv('../data/test.csv')

# or test on a larger test dataset
# import random
# size = 2000000
# data = pd.DataFrame({
#     'TOID': [random.randint(1, 3) for i in range(size)],
#     'Measure': [random.randint(0, 1) for i in range(size)],
#     'WEIGHT': [random.random() for i in range(size)]
# })
# groups = ['TOID']
# measures = ['Measure']
# calc_prop(df=data, groups=groups, vars=measures, weighted=False)

# data = pd.DataFrame({
#     'TOID': [random.randint(1, 3) for i in range(size)],
#     's_': [random.randint(1, 9) for i in range(size)],
#     'WEIGHT': [random.random() for i in range(size)]
# })
# groups = ['TOID']
# vars = ['s_']
# calc_prop(df=data, groups=groups, vars=vars, weighted=False)

# import time
# %timeit calc_prop(df=data, groups=groups, vars=measures, weighted=False)