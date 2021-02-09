# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import re

# %%

# helper function for new survey_query. runs much faster then .apply
# also wide version with for loop of columns is faster than doing on values column of melted df. no idea why though.

def grouped_wm(data, variables, weight_var, grouper, count_type=None):

    results = []
    counts = []
    for value_col in variables:

        data['product'] = data[value_col] * data[weight_var]
        data['weights_filtered'] = data[weight_var].where(~data['product'].isnull())
        grouped = data.groupby(grouper, sort=False).sum()
        result = grouped['product'] / grouped['weights_filtered']
        result.name = value_col
        results.append(result)

        if count_type == 'N_weighted':

            numerators = grouped['product']
            numerators.name = value_col
            counts.append(numerators)

        elif count_type == 'D_weighted':

            denominators = grouped['weights_filtered']
            denominators.name = value_col
            counts.append(denominators)

    data = pd.concat(results, axis=1) if len(results) > 1 else results[0].to_frame()

    if (count_type == 'N_weighted') | (count_type == 'N_weighted'):
        counts = pd.concat(counts, axis=1) if len(results) > 1 else counts[0].to_frame()
    return data, counts
# %%

def Survey_query(data,survey='s',variables=[], grouper=[], count_type=None, supress_lowN=5,yearlast=False,rounded=False,combine_years=False,unweighted=False,force_weight=False, weight_var='WEIGHT', year_var='SurveyYear',low_N=5):

    # set survey-dependent variables. Weight and year default to combined student dataset versions, overrides if employer selected.
    # might be computationally slower, but more user friendly to just specify 'e', not two different variable names.
    # custom variable names for other datasets can be fed in as arguments and won't be changed unless survey argument is set to 'e'
    
    if survey == 's':
        # do unweighted if data fitered to only one rto
        # this is idiot proofing so even if the default weighted version is used, rto level data will only be weighted if you set force_weight to True
        if (len(data['TOID'].unique()) == 1) & (force_weight==False):
            unweighted = True   

    elif survey == 'e':
        # do unweighted if data fitered to only one rto
        if len(data['e_toid'].unique()) == 1 & (force_weight==False):
            unweighted = True
        # set weight and year vars
        year_var = 'year'
        weight_var = 'Weight'

    # do unweighted if grouped by rto (same reason as above)

    if (any(item in grouper for item in ['TOID','RTOName','RTOTradingName','e_toid','rtoname','e_rto_name'])) & (force_weight==False):
        unweighted = True

    # add survey year to grouping variables in appropriate location
    # again adding slight runtime to the function but makes it more user friendly as I want to group by year by default.
    if combine_years == False:
        if yearlast == False:
            grouper.insert(0,year_var)
        else:
            grouper.append(year_var)
    else:
        # code assumes a grouper, adding a dummy column prevents errors with groupbys
        # imo not worth adding ungrouped calculations instead as we rarely pool years of data (main exceptions being the CIF and COD toll which I wouldn't be using this for)
        # (even though they'd only run if combine_years specified, it makes the function even bulkier to maintain).

        data['group_dummy'] = 1
        grouper.insert(0,'group_dummy')
        
    # filter data to relevant columns and valid values only

    columns = data[variables]    
    # replace invalid values with nan.
    columns.mask((columns <0) | (columns >5),np.nan,inplace=True)
    # make 5-point variables binary. Can't just use np.where because the NaNs would be evaluated and get changed to 0.
    columns.replace(2,1,inplace=True)
    columns.mask((columns > 2) ,0,inplace=True)
    # create list of other columns we need (grouping and weight)
    cols = grouper.copy()
    cols.append(weight_var)
    # merge cleaned columns with grouping variables and weights. Indexes match as they're from the same df to start with.
    data = pd.merge(columns,data[cols],left_index=True,right_index=True)
        
    # unweighted version
    if unweighted == True:
        data.drop(columns=weight_var,inplace=True)
        result = data.groupby(grouper,sort=False).mean()

    #weighted version    
    else: 
       result, counts = grouped_wm(data, variables, weight_var, grouper, count_type)

    # suppress results with low N 
    n = data.groupby(grouper, sort=False).count()
    low_n_indeces = n[result.columns.values] < low_N
    result[low_n_indeces] = np.nan

    # rounding
    if rounded == True:
        result = round(result*100,1)

    # add counts
    if count_type == 'N':
        numerators = data.groupby(grouper, sort=False).sum()
        result = pd.merge(result,numerators[result.columns.values],left_index=True,right_index=True,suffixes=['_result','_count'])

    elif count_type == 'D':
        result = pd.merge(result,n[result.columns.values],left_index=True,right_index=True,suffixes=['_result','_count'])

    # other kinds of counts already produced in helper function and saved in the counts variable
    elif count_type is not None:
        result = pd.merge(result,counts[result.columns.values],left_index=True,right_index=True,suffixes=['_result','_count'])

    return result