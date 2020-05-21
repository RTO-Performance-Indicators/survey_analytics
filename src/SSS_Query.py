# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import re
filePath = 'S:/RTOPI/Both Surveys/All Final Datasets/Datasets - 2019/StudentSurveys.csv'
#prelimPath = 'S:/RTOPI/Student Survey/Student Survey 2020/3. Data/5. Preliminary Files/2393 RTO preliminary data 1 main 2020-04-06.csv'
savePath = 'S:\\RTOPI\\Data Requests\\RPIJ0175 Apprenticeship data - Julie Anderson\\unformatted data outputs\\'
df = pd.read_csv(filePath, encoding = 'ISO-8859-1')
#prelim_df = pd.read_csv(prelimPath, encoding = 'ISO-8859-1')

# %%
#function to query measures or questions
def Survey_query(survey,data,varnames, export_name=None, grouper=None, with_counts=0,supress_lowN=5,yearlast=False,rounded=False) :
    #set weight and year vars
    if survey == 'student':
        year_var = 'SurveyYear'
        weight_var = 'WEIGHT'
    elif survey == 'employer':
        year_var = 'Year'
        weight_var = 'e_wght_delta'
    #make list object to store results
    result = []
    counts = []
    #add survey year to grouping variables
    if yearlast == False:
        grouper.insert(0,year_var)
    else:
        grouper.insert(len(grouper),year_var)
    #loop through variables of interest and compute agree percentages
    counter = 0
    for i in varnames :
        validobvs = data[(~np.isnan(data[i]))]
        validobvs = data[data[i] >= 0]

        Measurei_W = (validobvs[i]*validobvs[weight_var])  
        validobvs[i + 'w'] = Measurei_W
        if grouper is not None:
            if ('TOID' in grouper) | ('RTOName' in grouper) | ('RTOTradingName' in grouper):
                result.append(validobvs.groupby(grouper).apply(lambda x: x[i].sum()/x[i].count() if x[i].count() > supress_lowN else np.nan))
            else:
                result.append(validobvs.groupby(grouper).apply(lambda x: x[i +"w"].sum()/x[weight_var].sum() if (x[i].count() > supress_lowN) else np.nan))
            
            result[counter] = pd.DataFrame(result[counter], columns=[varnames[counter]])

            if counter == 0:
                result_df = result[counter]
            else:
                result_df = pd.DataFrame.join(result_df,result[counter])
            if with_counts ==1:
                counts.append(validobvs.groupby(grouper).apply(lambda x: x[i].count()))
                count = pd.DataFrame(counts[counter], columns=[varnames[counter]+' N'])                
                result_df = pd.DataFrame.join(result_df,count)
        else:
            result.append(validobvs.groupby([year_var]).apply(lambda x: x[i +"w"].sum()/x[weight_var].sum() if (x[i].count() > supress_lowN) else np.nan))
            result[counter] = pd.DataFrame(result[counter], columns=[varnames[counter]])
            
            if counter == 0:
                result_df = result[counter]
            else:
                result_df = pd.DataFrame.join(result_df,result[counter])
            if with_counts ==1:
                counts.append(validobvs.groupby([year_var]).apply(lambda x: x[i].count()))
                count = pd.DataFrame(counts[counter], columns=[varnames[counter]+' N'])
                result_df = pd.DataFrame.join(result_df,count)            
        counter +=1
    if rounded == True:
        for i in varnames:
            result_df[i] = [round(x*100,1) for x in result_df[i]]
    if export_name is not None:
        result_df.to_excel(savePath + export_name)
    return result_df



# %%
