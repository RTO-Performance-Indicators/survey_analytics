import pandas as pd
import numpy as np

# Load further study data and superseded course concordances
fs = pd.read_csv('S:/RTOPI/Research projects/Further study/data/further_study.csv')
superseded = pd.read_excel('S:/TMIPU/Info Library/ISA Data & Information/Superseded Mappings/TGA Superseded Mappings - July 2020 - All courses.xlsx',
                            sheet_name = 'With 1 allocation only')

superseded['course_title_lower'] = superseded['LatestCourseTitle'].str.lower()

# Merge fs with superseded course information
merged = pd.merge(fs, superseded[['Course', 'LatestCourse', 'course_title_lower']],
                  how = 'left',
                  left_on = 's_fs_name_v_fixed', right_on = 'course_title_lower')

# 58,816 / 72,500 (81.13%) rows with fixed course verbatims have matched a superseded course code/title
sum(~pd.isna(merged[~pd.isna(merged['s_fs_name_v_fixed'])]['course_title_lower']))
merged[~pd.isna(merged['s_fs_name_v_fixed'])].shape[0]

# Which fixed verbatims couldn't find a superseded course code?
# There are a couple of bachelor degrees
merged[~pd.isna(merged['s_fs_name_v_fixed']) & pd.isna(merged['LatestCourse'])]['s_fs_name_v_fixed'].value_counts().head(20)