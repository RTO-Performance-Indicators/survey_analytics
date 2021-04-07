import pandas as pd
import numpy as np

# set this to get rid of warnings for setting on a slice of copy 
# (which is the desired behaviour here)
pd.options.mode.chained_assignment = None

def calc_multi_measure(df, components, output_name, preserve_NA=True):
    ''' 
    Calculates a survey measure based on multiple components.

    This is relevant for the following measures:
    * Measure 5 - Generic skills and learning experiences
    * Measure 10 - Positive perception of teaching
    * Measure 13 - Positive perception of the assessment process

    Calculates performance measures based on having no negative outcomes in
    a list of components. NA if all components are null, 
    otherwise nulls treated as non-negative outcome. 
    All values <1 or >5 assumed to be NA.

    Returns a pandas series 

    Args:
        df (pandas dataframe): a dataframe with columns for each measure component
        components (list): a list with the column names from df for each component
        output_name (string): the desired name of the resulting series
        preserve_NA (boolean): specifies whether to keep numerical NA values or replace with NaN

    Returns:
        A pandas series named output_name, the same length as the input 
        dataframe with binary (or NaN) values. 
    '''
    # get neccesary columns
    data = df[components].copy()

    # replace NAs
    if preserve_NA == False:
        data.mask((data < 0) | (data > 5), np.nan, inplace=True)
    else:
        data.mask((data > 5), -999, inplace=True)

    # make 5-point variables binary. 
    # Can't just use np.where 
    # because the NaNs would be evaluated and get changed to 1 or 0.
    data.replace(2, 1, inplace=True)
    data.mask((data.isin([3, 4, 5])), 0, inplace=True)

    # this logic is a bit backwards but very concise:
    # make measure equal to 1 by default
    data[output_name] = 1
    # change rows with ANY 0 to 0 (doesn't matter whether the rest are null or 1)
    # technically this is also 
    data.loc[(data[components] == 0).any(1), output_name] = 0
    # change rows will ALL null to NaN
    if preserve_NA == False:
        data.loc[data[components].isnull().all(1), output_name] = np.nan
    else:
        data.loc[(~data[components].isin([0,1])).all(1), output_name] = -999

    return(data[output_name])

def calc_one_question_measure(df,colname,output_name,preserve_NA=True):
    ''' Calculates a survey measure based on one question.

    Calculates performance measures based on a question with responses
    on a scale of 1-5, where 1 is high and 5 is low. 
    All values <1 or >5 assumed to be NA.

    Returns a pandas series.

    Args:
        df (pandas dataframe): a dataframe with columns for each measure component
        colname (string): the name of the column in df with the input data
        output_name (string): the desired name of the resulting series
        preserve_NA (boolean): specifies whether to keep numerical NA values or replace with NaN

    Returns:
        A pandas series named output_name, the same length as the input 
        dataframe with binary (or NaN) values. 

    '''

     # get data
    data = df[colname].copy()

    # replace NAs. 
    if preserve_NA == False:
        # replace NAs. 
        data.mask((data <0) | (data >5), np.nan, inplace=True)
    else:
        data.mask((data >5), -999, inplace=True)

    # make 5-point variables binary. 
    # Can't just use np.where 
    # because the NaNs would be evaluated and get changed to 1 or 0.
    data.replace(2, 1, inplace=True)
    data.mask((data.isin([3, 4, 5])), 0, inplace=True)
    # rename from input variable to output name
    data.rename(output_name, inplace=True)

    return(data)

''' 
usage example 
(obviously you don't have to put these straight into the existing dataframe, 
just makes it easy to do a crosstab with src versions)

# read in survey file
file_path = '' # put the filepath here before running, 
suppressed here so the code can go on github without displaying S: drive structure
df = pd.read_csv(file_path, encoding = 'ISO-8859-1')

# calculate student survey measures
df['Measure5_check'] = calc_multi_measure(df,['s_sat_prob','s_sat_team','s_sat_num',
                    's_sat_engwrt','s_sat_sc','s_sat_co'],'Measure5_check')

df['Measure9_check'] = calc_one_question_measure(df,'s_achiev','Measure9_check')

df['Measure10_check'] = calc_multi_measure(df,['s_sat_clr','s_sat_lrn','s_sat_ind'],
                        'Measure10_check')

df['Measure12_check'] = calc_one_question_measure(df,'s_rec_to','Measure12_check')

df['Measure13_check'] = calc_multi_measure(df,['s_sat_a_clr','s_sat_a_app','s_sat_a_cout'],
                        'Measure13_check')

df['Measure16_check'] = calc_one_question_measure(df,'s_sat_tot','Measure16_check')
'''

# turn M1 code into function. not bothering to generalise most of this as it's so specific and not needed in other cases.

def calc_M1(df,with_components=True):
    ''' Creates variables for each component of Measure 1 and the overall measure

    Args:
        df (pandas dataframe): a dataframe with Student Satisfaction Survey data
        with_components (boolean): indicates if all components should be return or just Measure 1 itself
    
    Returns:
        A pandas series with the Measure 1 result for each row in df (if 
        with_components == False) or a pandas dataframe the same length as df 
        with columns for each component of Measure 1 and the current and 
        historical versions of the overall measure.
    '''
    # copy required columns
    columns = ['s_hrs_bt','s_hrs_at','s_jb_bt_new','s_jb_at_new','s_semp_bt',
                's_jben_pr','s_jben_er','s_jben_es','s_compl_t','enrol_type',
                's_jben_nj_new','s_jben_ex']

    data = df[columns].copy()

    # calculate components

    # same emp more hours
    data.loc[:,'M1_semp_more_hours_check'] = -999

    # option to treat jobkeeper as 0 hours - comment out if treating as NA
    data['s_hrs_bt'].replace(-95,0,inplace=True)
    data['s_hrs_at'].replace(-95,0,inplace=True)

    # 1: has job, has valid hours before and after, 
    # has same employer and either promotion or more hours
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & (data['s_semp_bt'] == 1) & 
            ((data['s_jben_pr'] == 1) | ((data['s_hrs_bt'] > 0) & 
            (data['s_hrs_at'] > 0) & (data['s_hrs_at'] > data['s_hrs_bt']))),
            'M1_semp_more_hours_check'] = 1

    # 0: has job, has valid hours before and after, 
    # has different employer or no promotion or increase in hours
    # note: this appears to differ from the final src version which 
    # gives people with data['s_semp_bt'] == 2 an NA value
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & ((data['s_semp_bt'] == 2)|
            (((data['s_hrs_bt'] > 0) & (data['s_hrs_at'] > 0) &(data['s_hrs_at'] 
            <= data['s_hrs_bt']))&(data['s_jben_pr'] == 0))),
            'M1_semp_more_hours_check'] = 0

    ''' option to exclude hours increase due to starting on 
    jobkeeper 0 hours
    data.loc[(data['M1_semp_more_hours_check'] == 1) & 
    (data['s_hrs_bt'] == 0) & (data['s_jben_pr'] == 0),
    'M1_semp_more_hours_check'] = 0'''

    # same emp completed apprenticeship or traineeship
    data.loc[:,'M1_same_emp_A_or_T_check'] = -999
    # 1: has job, same employer, admin enrolment type A or T, 
    # completed course (self-reported)
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) &     (data['s_semp_bt'] == 1) 
    & (data['enrol_type'] == 1) &     (data['s_compl_t'] == 1),
    'M1_same_emp_A_or_T_check'] = 1
    # 0: has job, different employer or not A or T or not completed
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & ((data['s_semp_bt'] == 2) 
    | (data['enrol_type'] == 0) | (data['s_compl_t'].isin([2,3]))),
    'M1_same_emp_A_or_T_check'] = 0

    # same emp prom
    data.loc[:,'M1_same_emp_prom_check'] = -999
    # employed before, same emp, s_jben_er = 1
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & (data['s_semp_bt'] == 1) & 
    (data['s_jben_er'] == 1),'M1_same_emp_prom_check'] = 1
    # 0: employed before, either not same emp or not s_jben_er
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & ((data['s_semp_bt'] == 2) | 
    (data['s_jben_er'] == 0)),'M1_same_emp_prom_check'] = 0

    # same emp new role
    data.loc[:,'M1_same_emp_nr_check'] = -999
    # 1: employed before, same emp, s_jben_pr = 1 
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & (data['s_semp_bt'] == 1) 
    & (data['s_jben_pr'] == 1),'M1_same_emp_nr_check'] = 1
    # 0: employed before, either not same emp or not s_jben_pr
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & ((data['s_semp_bt'] == 2) 
    | (data['s_jben_pr'] == 0)),'M1_same_emp_nr_check'] = 0

    # new emp
    data.loc[:,'M1_new_emp_check'] = -999
    # 1: employed before, different emp, s_jben_nj_new =1
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & (data['s_semp_bt'] == 2) & 
    (data['s_jben_nj_new'] == 1),'M1_new_emp_check'] = 1
    # 0: employed before, either not same emp or not s_jben_pr
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & ((data['s_semp_bt'] == 1) | 
    (data['s_jben_nj_new'] == 0)),'M1_new_emp_check'] = 0

    # grew bus
    data.loc[:,'M1_grew_bus_check'] = -999
    # 1: has business before and after, s_jben_ex =1
    data.loc[(data['s_jb_bt_new'] == 1) & (data['s_jb_at_new'] == 1) & 
    (data['s_jben_ex'] == 1),'M1_grew_bus_check'] = 1
    # 1: no business before, no business after 
    # or business after but s_jben_ex = 0
    data.loc[(data['s_jb_bt_new'].isin([2,3])) | ((data['s_jb_bt_new'] == 1) & 
    ((data['s_jb_at_new'].isin([2,3])) | (data['s_jben_ex'] == 0))),
    'M1_grew_bus_check'] = 0

    # prev emp new bus - logic from src specs
    data.loc[:,'M1_prev_emp_new_bus_check'] = -999
    # 1: has job before business after, s_jben_ex =1
    data.loc[(data['s_jb_bt_new'].isin([2,3])) & (data['s_jb_at_new'] == 1) 
    & (data['s_jben_ex'] == 1),'M1_prev_emp_new_bus_check'] = 1
    # 1: has business before, job before and after, or job before business after 
    # but bs_jben_ex =1
    data.loc[(data['s_jb_bt_new'] == 1) | ((data['s_jb_bt_new'].isin([2,3])) 
    & ((data['s_jb_at_new'].isin([2,3]))|(data['s_jben_ex'] == 0))),
    'M1_prev_emp_new_bus_check'] = 0

    # extra skills
    data.loc[:,'M1_extra_skills_check'] = -999
    # 1: employed before, same emp, s_jben_es = 1 
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & (data['s_semp_bt'] == 1) 
    & (data['s_jben_es'] == 1),'M1_extra_skills_check'] = 1
    # 0: employed before, either not same emp or not s_jben_es
    data.loc[(data['s_jb_bt_new'].isin([1,2,3])) & ((data['s_semp_bt'] == 2) |
     (data['s_jben_es'] == 0)),'M1_extra_skills_check'] = 0

    # got job
    data.loc[:,'M1_got_job_check'] = -999
    # 1: unemployed before and employed after
    data.loc[(data['s_jb_bt_new'].isin([4,5])) & 
    (data['s_jb_at_new'].isin([1,2,3])),'M1_got_job_check'] = 1
    # 0: unemployed before and after
    data.loc[(data['s_jb_bt_new'].isin([4,5])) & 
    (data['s_jb_at_new'].isin([4,5])),'M1_got_job_check'] = 0

    # prev unemp new bus
    data.loc[:,'M1_prev_unemp_new_bus_check'] = -999
    # 1: previously unemployed and s_jb_at_new =1
    data.loc[(data['s_jb_bt_new'].isin([4,5])) & (data['s_jb_at_new'] == 1),
    'M1_prev_unemp_new_bus_check'] = 1
    # 0: previously unemployed and not business after 
    # still unemployed is excluded from the base for this one. 
    # I don't get why but it matches what has been done previously.
    data.loc[(data['s_jb_bt_new'].isin([4,5])) & 
    (data['s_jb_at_new'].isin([2,3])),'M1_prev_unemp_new_bus_check'] = 0

    # calculate overall measure

    components = ['M1_semp_more_hours_check','M1_same_emp_A_or_T_check',
    'M1_same_emp_prom_check','M1_same_emp_nr_check','M1_new_emp_check',
    'M1_grew_bus_check','M1_prev_emp_new_bus_check','M1_extra_skills_check',
    'M1_got_job_check','M1_prev_unemp_new_bus_check']
    
    data.loc[:,'Measure1_check'] = 0
    # change rows with ANY 1 to 1, doesn't matter about mix of 0 and NA
    data.loc[(data[components] == 1).any(1),'Measure1_check'] = 1
    # change rows will no 1 and not all null to 0
    data.loc[(data[components] < 0).all(1),'Measure1_check'] = -999

    components2 = ['M1_semp_more_hours_check','M1_same_emp_A_or_T_check',
    'M1_same_emp_prom_check','M1_same_emp_nr_check','M1_new_emp_check',
    'M1_grew_bus_check','M1_prev_emp_new_bus_check','M1_got_job_check',
    'M1_prev_unemp_new_bus_check']
    
    data.loc[:,'Measure1_hist1_check'] = 0
    # change rows with ANY 1 to 1, doesn't matter about mix of 0 and NA
    data.loc[(data[components2] == 1).any(1),'Measure1_hist1_check'] = 1
    # change rows will no 1 and not all null to 0
    data.loc[(data[components2] < 0).all(1),'Measure1_hist1_check'] = -999

    # remove input columns so output is just new stuff...
    data.drop(columns=columns,inplace=True)
    if with_components == False:
        return(data[['Measure1_check']])
    else:
        return(data)

def calc_M7(df,with_components=True):
    ''' Calculate measure 7 from survey data

    Args:
        df (pandas dataframe): a dataframe with Student Satisfaction Survey data
        with_components (boolean): indicates if all components should be return or just Measure 7 itself
    
    Returns:
        A pandas series with the Measure 7 result for each row in df (if 
        with_components == False) or a pandas dataframe the same length as df 
        with columns for the AQF levels for the current course and further study
        and measure 7.
    '''

    # copy required columns
    columns = ['course_level','s_fs_lev','s_fs_st']
    data = df[columns].copy()

    # create AQF variables
    current_keys = [211,221,311,312,411,413,421,511,514,521,524,611,613,621,
                912,991,992,999]
    current_course_AQF = [8,8,8,7,6,6,5,4,3,2,1,0,np.nan,np.nan,np.nan,0.5,
                        np.nan,np.nan]
    current_levels = dict(zip(current_keys, current_course_AQF))

    data['CourseAQF'] = data['course_level'].map(current_levels)

    new_keys = [-999,-888,-99,1,2,3,4,5,6,7,10,11]
    new_course_AQF = [np.nan,np.nan,np.nan,1,2,3,4,0,5,6,np.nan,7]
    new_levels = dict(zip(new_keys, new_course_AQF))
    data['fsAQF'] = data['s_fs_lev'].map(new_levels)

    data.loc[:,'Measure7_check'] = -999
    data.loc[data['fsAQF'] > data['CourseAQF'],'Measure7_check'] = 1
    data.loc[(data['fsAQF'] <= data['CourseAQF']) | (data['s_fs_st'] == 2),
    'Measure7_check'] = 0

    if with_components == False:
        return(data['Measure7_check'])
    else:
        return(data[['Measure7_check','fsAQF','CourseAQF']])

    