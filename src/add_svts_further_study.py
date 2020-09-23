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
# Last updated: 22/09/2020

import pandas as pd
import numpy as np 
from datetime import datetime

# Load data
fs = pd.read_csv('S:/RTOPI/Research projects/Further study/data/further_study.csv', encoding = 'ISO-8859-1')
enrolments = pd.read_csv('S:/RTOPI/Research projects/Further study/data/course_enrolments.csv', encoding = 'ISO-8859-1')
superseded = pd.read_excel('S:/TMIPU/Info Library/ISA Data & Information/Superseded Mappings/TGA Superseded Mappings - July 2020 - All courses.xlsx', sheet_name = 'With 1 allocation only')

# fs['fs_source'] = 'survey'
enrolments = enrolments.drop('EnrolmentStatus', axis = 1)
enrolments = enrolments.rename(columns = {'Description': 'level_description'})
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
merged.fs_source.value_counts()

# TODO: Some course names are still missing despite valid CourseID_y
merged[merged['fs_source'] == '']

# TODO: fs_name_v is still valid even if it's not in SVTS, such as Bachelor degrees
#       Need to identify these, and create a new observation for them
merged[merged['s_fs_name_v_fixed'] != merged['CourseName']]

# Now use course name based on fs_source
merged['fs_course_name'] = merged.apply(lambda x: x['s_fs_name_v_fixed'] if x['fs_source'] == 'survey' else x['CourseName'], axis = 1)

merged.head()

# TODO: Select the correct level description

# Tidy up the columns (drop and rename)
merged = merged.drop(['TOID_y', 'ClientIdentifier_y', 'CourseID_y', 'CourseName', 's_fs_name_v_fixed'], axis = 1)
merged = merged.rename(columns = {'TOID_x': 'TOID', 
                                  'ClientIdentifier_x': 'ClientIdentifier', 
                                  'CourseID_x': 'CourseID',
                                  'CourseCommencementDate_x': 'CourseCommencementDate',
                                  'CourseCommencementDate_y': 'CourseCommencementDate_fs'})
merged['fs_source'] = 'SVTS'

enrolments.shape
temp.shape
fs.shape
merged.shape
merged.head()

sum(pd.isna(fs['SLK']))

# There are still more SLKs in enrolments than in fs
len(enrolments.SLK.unique())
len(fs.SLK.unique())
len(temp.SLK.unique())
len(merged.SLK.unique())