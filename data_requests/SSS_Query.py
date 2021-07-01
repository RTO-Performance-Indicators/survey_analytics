# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import re

# %%

# helper function for new survey_query. runs much faster then .apply
# also wide version with for loop of columns is faster than doing on values column of melted df. no idea why though.

def grouped_wm(data, variables, weight_var, grouper, survey, count_type=None):

    results = []
    counts = []
    for value_col in variables:
        # select correct weight for employer survey
        if survey == 'e':
            if value_col in ['hiring_intent', 'barrier_90',
       'barrier_97', 'barrier_99', 'barrier_999', 'barrier_01',
       'barrier_02', 'barrier_03', 'barrier_04', 'barrier_05',
       'barrier_06', 'barrier_07', 'barrier_08', 'barrier_09',
       'barrier_10', 'barrier_11', 'barrier_12', 'barrier_13',
       'barrier_14', 'barrier_15', 'reason24', 'reason25',
       'reason26', 'reason27', 'reason1', 'reason2', 'reason3',
       'reason4', 'reason5', 'reason6', 'reason7', 'reason8',
       'reason9', 'reason10', 'reason11', 'reason12',
       'reason13', 'reason14', 'reason15', 'reason16',
       'reason17', 'reason18', 'reason19', 'reason20',
       'reason21', 'reason22', 'reason23', 'further_research']:
                weight_var = 'weight_all'

        data['product'] = data[value_col].values * data[weight_var].values
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
    data.drop(columns=['product','weights_filtered'],inplace=True)
    results = pd.concat(results, axis=1) if len(results) > 1 else results[0].to_frame()

    if (count_type == 'N_weighted') | (count_type == 'D_weighted'):
        counts = pd.concat(counts, axis=1) if len(results) > 1 else counts[0].to_frame()
    return results, counts
# %%

# helper function for calculating percentages of each value for categorical variables. 
# Way slower than main version as it loops through each value, but still 10x faster than old function for categorical vars.

def cat_grouped_wm(data, cat_vars, weight_var, grouper,NA_values,count_type,unweighted, low_N, survey):
    cat_results = []
    cat_counts = []
    cat_varnames = []

    for value_col in cat_vars:
        # select correct weight for employer survey
        if survey == 'e':
            if value_col in ['hiring_intent', 'barrier_90',
       'barrier_97', 'barrier_99', 'barrier_999', 'barrier_01',
       'barrier_02', 'barrier_03', 'barrier_04', 'barrier_05',
       'barrier_06', 'barrier_07', 'barrier_08', 'barrier_09',
       'barrier_10', 'barrier_11', 'barrier_12', 'barrier_13',
       'barrier_14', 'barrier_15', 'reason24', 'reason25',
       'reason26', 'reason27', 'reason1', 'reason2', 'reason3',
       'reason4', 'reason5', 'reason6', 'reason7', 'reason8',
       'reason9', 'reason10', 'reason11', 'reason12',
       'reason13', 'reason14', 'reason15', 'reason16',
       'reason17', 'reason18', 'reason19', 'reason20',
       'reason21', 'reason22', 'reason23', 'further_research']:
                weight_var = 'weight_all'

        # create array of relevant values and remove those specified as NAs
        values = data[value_col].unique()
        values = set(values) - set(NA_values)

        # create binary column for each value
        for y in values:
            cat_varnames.insert(len(cat_varnames),(value_col + str(y)))
            data[value_col + str(y)] = np.where(data[value_col] == y,1,0)
            data.loc[(data[value_col].isin(NA_values)) |  (data[value_col].isna()),value_col + str(y)] = np.nan

            #weighted calc by each relevant value    
            if unweighted == False: 

                data['product'] = data[value_col + str(y)].where(~data[value_col].isin(NA_values)).values * data[weight_var].where(~data[value_col].isin(NA_values)).values
                data['weights_filtered'] = data[weight_var].where(~data['product'].isnull())
                grouped = data.groupby(grouper, sort=False).sum()
                result = grouped['product'] / grouped['weights_filtered']
                result.name = value_col + str(y)
                cat_results.append(result)

                if count_type == 'N_weighted':
                    numerators = grouped['product']
                    numerators.name = value_col + str(y)
                    cat_counts.append(numerators)

        if count_type == 'D_weighted':
            cat_count = grouped['weights_filtered']
            cat_count.name = value_col + 'count'
            cat_counts.append(cat_count)

    # join all counts if weighted denominators produced        
    

    # tidy up results
    if unweighted == False: 
        data.drop(columns=['product','weights_filtered'],inplace=True)
        cat_results = pd.concat(cat_results, axis=1) if len(cat_results) > 1 else cat_results[0].to_frame()
    
    # unweighted calc done on all cols at once
    else:
        # do an unweighted version    
        cat_results = data[cat_varnames + grouper].groupby(grouper,sort=False).mean()

    # suppress results with low N 
    n = data.groupby(grouper, sort=False).count()
    low_n_indeces = n[cat_results.columns.values] < low_N
    cat_results[low_n_indeces] = np.nan
    
    # add counts
    if (count_type == 'D_weighted') | (count_type == 'N_weighted'):       
        cat_counts = pd.concat(cat_counts, axis=1) if len(cat_results) > 1 else cat_results[0].to_frame()
    elif (count_type == 'N'):
        cat_counts = data[cat_varnames + grouper].groupby(grouper,sort=False).sum()
    elif (count_type == 'D'):
        cat_counts = n[cat_vars]

    if count_type is not None:
        cat_results = pd.merge(cat_results,cat_counts,left_index=True,right_index=True,suffixes=['_result','_count'])

    # sort columns so they're not just in the order the values first appear
    cat_results.reindex(columns=sorted(cat_results.columns))

    return cat_results
# %%

def Survey_query(data,survey='s',variables=None, cat_vars=None,grouper=None, count_type=None, yearlast=False,rounded=False,combine_years=False,
                unweighted=False,force_weight=False, weight_var='weight', year_var='survey_year',low_N=5,NA_values=None):

    # these are expected to be lists later on, so if not specificed change to empty lists
    if grouper is None:
        grouper = []

    if cat_vars is None:
        cat_vars = []

    if variables is None:
        variables = []

    # set survey-dependent variables. Weight and year default to combined student dataset versions, overrides if employer selected.
    # might be computationally slower, but more user friendly to just specify 'e', not two different variable names.
    # custom variable names for other datasets can be fed in as arguments and won't be changed unless survey argument is set to 'e'
 
        # do unweighted if data fitered to only one rto
        # this is idiot proofing so even if the default weighted version is used, rto level data will only be weighted if you set force_weight to True
    if (len(data['toid'].unique()) == 1) & (force_weight==False):
        print('ONLY ONE RTO DETECTED, UNWEIGHTED CALCULATIONS PRODUCED')
        unweighted = True   

    if survey == 'e':
        # set default year var for employer
        year_var = 'year'

    # do unweighted if grouped by rto (same reason as above)

    if (any(item in grouper for item in ['toid','rto_name','rto_trading_name'])) & (force_weight==False):
        print('GROUPED BY RTO, UNWEIGHTED CALCULATIONS PRODUCED')
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
    if survey == 'e':
        cols.append('weight_all)
    cols = cols + cat_vars

    # merge cleaned columns with grouping variables and weights. Indexes match as they're from the same df to start with.
    data = pd.merge(columns,data[cols],left_index=True,right_index=True)

    if variables != []:      
        # unweighted version
        if unweighted == True:
            data.drop(columns=weight_var,inplace=True)
            result = data[variables + grouper].groupby(grouper,sort=False).mean()

        #weighted version    
        else: 
            result, counts = grouped_wm(data, variables, weight_var, grouper, survey, count_type)

        # suppress results with low N 
        n = data.groupby(grouper, sort=False).count()
        low_n_indeces = n[result.columns.values] < low_N
        result[low_n_indeces] = np.nan

        # add counts
        if count_type == 'N':
        
            numerators = data[variables + grouper].groupby(grouper, sort=False).sum()
            result = pd.merge(result,numerators[result.columns.values],left_index=True,right_index=True,suffixes=['_result','_count'])

        elif count_type == 'D':
            result = pd.merge(result,n[variables],left_index=True,right_index=True,suffixes=['_result','_count'])

        # other kinds of counts already produced in helper function and saved in the counts variable
        elif count_type is not None:
            result = pd.merge(result,counts[variables],left_index=True,right_index=True,suffixes=['_result','_count'])

    if cat_vars != []:
    # calculate results for categorical variables
        cat_result = cat_grouped_wm(data,cat_vars,weight_var,grouper,NA_values,count_type,unweighted,low_N, survey)
        if variables != []:
            result = pd.merge(result,cat_result,left_index=True,right_index=True)
        else:
            result = cat_result

    # rounding
    if rounded == True:
        if count_type is None:
            result = round(result*100,1)
        else:
            result_columns = [col for col in result.columns if '_result' in col]
            result[result_columns] = round(result[result_columns]*100,1)
    
    # sort rows
    result.sort_index(inplace=True)
    return result

