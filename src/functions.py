import pandas as pd
import numpy as np

def measures(df, measures = [], group = [], weighted = True, weight = 'WEIGHT'):
    
    

    # id_vars: columns to keep when data frame is melted down to a tidy data set
    id_vars = group.copy()
    if weighted == True:
        id_vars.append(weight)

    # groups: after melting, the 'variable' column, containing the measure variable,
    # becomes a new grouping variable
    groups = group.copy()
    groups.append('variable')

    # Convert from wide to tidy data set
    long = pd.melt(df, id_vars = id_vars, value_vars = measures)
    long = long[~np.isnan(long['value'])]

    # Nested function to return 'proportions' and 'N'
    def prop_and_n(x):
        d = {}
        d['N'] = x['value'].count()
        if weighted == True:
            d['proportion'] = np.average(x['value'], weights = x[weight])
        else:
            d['proportion'] = np.average(x['value'])

        return pd.Series(d, index = ['proportion', 'N'])

    # Apply the nested function to the data frame
    long = long.groupby(groups).apply(prop_and_n)

    # N must be greater than 5 for reporting
    long.loc[long['N'] < 5, 'proportion'] = np.NaN

    return long

def calc_binary_proportion(series, weights = 1,  missing = [-999, -99, -888, -88]):
    
    import pandas as pd
    import numpy as np

    # Is columns a pandas series?
    if isinstance(series, pd.Series) == False:
        raise TypeError("The 'series' argument must be a pandas series")
    
    if weights == 1:
        weights = pd.Series([weights] * len(series))

    # Remove missing observations
    weights = weights[(~np.isin(series, missing)) & (~pd.isna(series))]
    series = series[(~np.isin(series, missing)) & (~pd.isna(series))]
    
    # Make sure column is binary
    if len(series.unique()) != 2:
        raise ValueError("The series does not appear to contain binary values")
    
    # Calculate proportion, N, and weighted N
    proportions = np.average(series, weights = weights, returned = True)
    N = series.count()

    result = {'proportion': [proportions[0]],
              'N': [N],
              'N_wt': [proportions[1]]}
    
    return pd.DataFrame(data = result)

# test the function
temp = pd.Series(data = [1, 1, 0, 0, np.nan])
calc_binary_proportion(series = temp)

