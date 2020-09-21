import pandas as pd                 # Python Data Analysis Library
import numpy as np                  # Numerical Python
from datetime import datetime

fs = pd.read_csv("S:/RTOPI/Research projects/Further study/data/further_study.csv", encoding = 'ISO-8859-1')
enrolments = pd.read_csv("S:/RTOPI/Research projects/Further study/data/course_enrolments.csv", encoding = 'ISO-8859-1')

fs['CourseCommencementDate'] = pd.to_datetime(fs['CourseCommencementDate'])
enrolments['CourseCommencementDate'] = pd.to_datetime(enrolments['CourseCommencementDate'])

fs.head()
enrolments.head()

# Merge the Enrolments data from SVTS to further study data
temp = pd.merge(fs, enrolments, how = 'left', 
    left_on = ['TOID', 'ClientIdentifier', 'CourseID', 'CourseCommencementDate'],
    right_on = ['TOID', 'ClientID', 'CourseCode', 'CourseCommencementDate']).drop(['ClientID', 'CourseCode'], axis = 1)


# Check if there are many missing SLKs: 157,003 / 293,054 (53.57%)
print(sum(np.isnan(temp['SLK'])), "out of", temp.shape[0], "rows were not matched to SVTS SupercededCourseEnrolment data.") 

temp.head()

temp[temp['SLK'] == 430038617]
