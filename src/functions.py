import pandas as pd
import numpy as np

def measures(df, measures = [], group = [], weighted = True, weight = 'WEIGHT'):
    
    import pandas as pd
    import numpy as np

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