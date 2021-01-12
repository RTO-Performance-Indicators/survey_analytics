# The purpose of this script is to append further study recorded in SVTS
# to the further study verbatim cleaned from the Student Satisfaction Survey.
# 
# Note 1: This script should be run AFTER: 
#         1 - clean_further_study.py
#         2 - course_enrolments.sql (go to Research RTOPI/projects/Further study/data/)
#
# Note 2: The script relies on enrolments data extracted via SQL,
#         and may need to be updated regularly.
#
# Note 3: Changes to this script should be managed using GIT and GitHub
#
# Last updated: 25/09/2020

import pandas as pd
import numpy as np 
import Levenshtein
from datetime import datetime

# Load data
fs = pd.read_csv('S:/RTOPI/Research projects/Further study/data/further_study.csv', encoding = 'ISO-8859-1')
enrolments = pd.read_csv('S:/RTOPI/Research projects/Further study/data/course_enrolments.csv', encoding = 'ISO-8859-1')
superseded = pd.read_excel('S:/TMIPU/Info Library/ISA Data & Information/Superseded Mappings/TGA Superseded Mappings - July 2020 - All courses.xlsx', sheet_name = 'With 1 allocation only')

enrolments = enrolments.drop('EnrolmentStatus', axis = 1)
enrolments = enrolments.rename(columns = {'Description': 'level_description'})
enrolments['level_description'] = enrolments['level_description'].str.lower()
superseded = superseded[['Course', 'LatestCourseTitle']]

# Conform datetimes to enable joins
fs['CourseCommencementDate'] = pd.to_datetime(fs['CourseCommencementDate'])
enrolments['CourseCommencementDate'] = pd.to_datetime(enrolments['CourseCommencementDate'])

# Add Latest course name to svts enrolments (because I couldn't get the SQL to work)
# TODO: Fix course name extraction using SQL and remove from this script
enrolments = pd.merge(enrolments, superseded, left_on = 'CourseCode', right_on = 'Course', how = 'left').drop(['Course'], axis = 1)
enrolments = enrolments.rename(columns = {'ClientID': 'ClientIdentifier',
                                          'CourseCode': 'CourseID',
                                          'LatestCourseTitle': 'CourseName'})
enrolments['CourseName'] = enrolments['CourseName'].str.lower()

# Add the latest SLK to fs data (SLK can change over time)
fs = pd.merge(fs, enrolments,
              left_on = ['TOID', 'ClientIdentifier', 'CourseID', 'CourseCommencementDate'],
              right_on = ['TOID', 'ClientIdentifier', 'CourseID', 'CourseCommencementDate'],
              how = 'left')
fs = fs.drop(['level_description_y', 'CourseName'], axis = 1)
fs = fs.rename(columns = {'level_description_x': 'level_description'})

# Filter SVTS enrolments to students in fs (includes students who did not provide s_fs_name_v),
# and where CourseCommencementDate in SVTS is after CourseCommencementDAte in survey
# WHY IS THE MERGED DATASET SO LARGE??
enrolments_temp = enrolments[np.isin(enrolments['SLK'], fs['SLK'].unique())]
merged = pd.merge(fs, enrolments_temp, left_on = 'SLK', right_on = 'SLK', how = 'left')
merged = merged[merged['CourseCommencementDate_y'] > merged['CourseCommencementDate_x']]

# Ascertain the source of further study course (name)
merged['fs_source'] = merged.apply(lambda x: 'survey & SVTS' if x['s_fs_name_v_fixed'] == x['CourseName'] else '', axis = 1)
merged['fs_source'] = merged.apply(lambda x: 'SVTS' if (pd.notna(x['CourseName'])) & (pd.isna(x['s_fs_name_v_fixed'])) else x['fs_source'], axis = 1)
merged['fs_source'] = merged.apply(lambda x: 'SVTS' if (pd.notna(x['CourseName'])) &  (x['CourseName'] != x['s_fs_name_v_fixed']) else x['fs_source'], axis = 1)
merged['fs_source'] = merged.apply(lambda x: 'survey' if (pd.notna(x['s_fs_name_v_fixed'])) & (pd.isna(x['CourseName'])) else x['fs_source'], axis = 1)
merged['fs_source'] = merged.apply(lambda x: 'survey' if (pd.isna(x['s_fs_name_v_fixed'])) & (pd.notna(x['level_description_y'])) else x['fs_source'], axis = 1)
# merged.fs_source.value_counts()

# TODO: Some course names are still missing despite valid CourseID_y
# merged[merged['fs_source'] == '']

# TODO: Some coures names are also very similar between survey and svts,
#       but because they are different, they are recognised as a separate course,
#       and listed as source = survey (survey_valid code below)
# merged['similarity'] = merged.apply(lambda x: Levenshtein.distance(x['s_fs_name_v_fixed'], x['CourseName']), axis = 1)
# merged.sort_values(['similarity'])

# Lots of verbatim are incredibly similar to the svts course name,
# but some may legitimately be different, particularly the cert ii and cert iii courses
# where people have gone on to do the cert ii, then subsequently the cert iii
# merged[merged['similarity'] == 1][['SLK', 's_fs_name_v_fixed', 'CourseName']]
# Meanwhile, sometimes the cert ii doesn't exist, and it must have been the cert iii that
# studied.
# merged[merged['SLK'] == 339925402][['SLK', 's_fs_name_v_fixed', 'CourseName']]
# merged[merged['SLK'] == 249640142][['SLK', 's_fs_name_v_fixed', 'CourseName']]

# So, check whether the course name is legitimate
# merged['valid_course_name'] = np.isin(merged['s_fs_name_v_fixed'], superseded['LatestCourseTitle'])
# merged.valid_course_name.value_counts()

# And because of the imperfect match, the fs_source has been allocated to 'svts'
# merged[merged.similarity == 1].fs_source.value_counts()



# fs_name_v is still valid even if it's not in SVTS, such as Bachelor degrees
# Need to identify these, and create a new observation for them
survey_valid = merged[(merged['s_fs_name_v_fixed'] != merged['CourseName']) & (pd.notna(merged['s_fs_name_v_fixed']))]
survey_valid['fs_source'] = 'survey'
survey_valid = survey_valid[['SurveyResponseID', 'SurveyYear', 'TOID_x', 'ClientIdentifier_x',
                             'CourseID_x', 'SupercededCourseID', 'CourseCommencementDate_x',
                             'CourseLevelDesc',
                             's_fs_name_v_fixed', 'level_description_x', 'fs_source']]
survey_valid = survey_valid.rename(columns = {'TOID_x': 'TOID',
                                              'ClientIdentifier_x': 'ClientIdentifier',
                                              'CourseID_x': 'CourseID',
                                              'CourseCommencementDate_x': 'CourseCommencementDate',
                                              's_fs_name_v_fixed': 'fs_course_name',
                                              'level_description_x': 'level_description'})

# Now use course name based on fs_source
svts_valid = merged[merged['fs_source'] != 'survey']
svts_valid = svts_valid[['SurveyResponseID', 'SurveyYear', 'TOID_x', 'ClientIdentifier_x',
                             'CourseID_x', 'SupercededCourseID', 'CourseCommencementDate_x',
                             'CourseLevelDesc',
                             'CourseName', 'level_description_y', 'fs_source']]
svts_valid = svts_valid.rename(columns = {'TOID_x': 'TOID',
                                         'ClientIdentifier_x': 'ClientIdentifier',
                                         'CourseID_x': 'CourseID',
                                         'CourseCommencementDate_x': 'CourseCommencementDate',
                                         'CourseName': 'fs_course_name',
                                         'level_description_y': 'level_description'})

# Row bind survey_valid and svts_valid
further_study_df = survey_valid.append(svts_valid)

further_study_df = further_study_df[['SurveyResponseID', 'SurveyYear', 'TOID', 'SupercededCourseID', 'CourseLevelDesc', 'fs_course_name', 'level_description', 'fs_source']]

# Remove any duplicates
further_study_df = further_study_df.drop_duplicates()

# Write to csv
further_study_df.to_csv('S:/RTOPI/Research projects/Further study/Output/further_study.csv', index = False)