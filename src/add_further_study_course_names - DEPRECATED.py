# DEPRECATED
# MOVED CODE TO clean_further_study.py

# # The purpose of this script is further clean the further study verbatim by:
# # 1 - Replace verbatim with course codes with the course name
# # 2 - 
# #
# # Note 1: This script should be run after clean_further_study.py has been run.
# #
# # Last updated: 21/09/2020

# import pandas as pd
# import numpy as np

# # Load further study data and superseded course concordances
# fs = pd.read_csv('S:/RTOPI/Research projects/Further study/data/further_study.csv')
# superseded = pd.read_excel('S:/TMIPU/Info Library/ISA Data & Information/Superseded Mappings/TGA Superseded Mappings - July 2020 - All courses.xlsx',
#                             sheet_name = 'With 1 allocation only')
# superseded['LatestCourseTitle'] = superseded['LatestCourseTitle'].str.lower()

# # Not all are valid course codes, such as 2019 and 2020
# # so there needs to be a check for validity before replacing s_fs_name_v_fixed
# fs[~pd.isna(fs['verbatim_course_code'])][['s_fs_name_v_fixed', 'verbatim_course_code']]

# # However, 2019 and 2020 seem to be valid course codes?
# superseded[superseded['Course'] == '2019'][['Course', 'LatestCourseTitle']]

# # Remove years as valid superseded course codes
# superseded = superseded[~np.isin(superseded['Course'], ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'])]

# # Merge superseded course title to fs data frame
# # fs_temp = fs[~pd.isna(fs['verbatim_course_code'])][['SurveyResponseID','s_fs_name_v_fixed', 'verbatim_course_code']]
# fs_merged = pd.merge(fs, superseded[['Course', 'LatestCourseTitle']], left_on = ['verbatim_course_code'], right_on = ['Course'], how = 'left')

# fs_merged['verbatim_course_code'].value_counts().head(20)

# # Now replace s_fs_name_v_fixed if LatestCourseTitle is not na
# fs_merged['s_fs_name_v_fixed'] = fs_merged.apply(lambda x: x['LatestCourseTitle'] if pd.isna(x['LatestCourseTitle']) == False else x['s_fs_name_v_fixed'], axis = 1)
# fs_merged = fs_merged.drop(['verbatim_course_code', 'Course', 'LatestCourseTitle'], axis = 1)

# # Write to CSV
# fs_merged.to_csv("S:/RTOPI/Research projects/Further study/data/further_study2.csv", index = False)