# README

This module contains Python functions to calculate survey measures.

This are primarily used to verify the measures calculated by survey providers and provided to us in the interim and final data sets.

## Usage

To import the module:

```
import sys
sys.path.append('C:\\Users\\[GitHub repo folder]\\survey_analytics')
from calculate_measures import calculate_measures
```

To use the functions:

```
# Based on multiple variables
df['measure5_check'] = calc_multi_measure(df=df, components=['s_sat_prob','s_sat_team','s_sat_num','s_sat_engwrt','s_sat_sc','s_sat_co'], output_name='measure5_check')

# Based on a single variable
df['measure9_check'] = calc_one_question_measure(df=df, colname='s_achiev', output_name='measure9_check')
```

## Reference

The table below shows the performance measures and the correct function to use to calculate the performance measure.

| Measure | Survey | Description | Function |
|:--------|:-------|:------------|----------|
| Measure 1 | Student | Proportion of students with an improved employment status after training |  |
| Measure 5 | Student | Proportion of students satisfied with generic skills and learning experiences | calc_multi_measure |
| Measure 6 | Employer | Proportion of employers reporting improvement in generic skills and learning experiences | calc_multi_measure |
| Measure 7 | Student | Proportion of students who went on to further study at a higher level |  |
| Measure 8 | Student | Proportion of students employed in the same occupation/industry as their course |  |
| Measure 9 | Student | Proportion of students who achieved their main reason for study | calc_one_question_measure |
| Measure 10 | Student | Proportion of students who reported a positive perception of teaching | calc_multi_measure |
| Measure 12 | Student | Proportion of students who would recommend the RTO | calc_one_question_measure |
| Measure 13 | Student | Proportion of students who reported a positive perception of the assessment process | calc_multi_measure |
| Measure 14 | Employer | Proportion of employers who are satisfied with training provided by an RTO | calc_one_question_measure |
| Measure 15 | Employer | Proportion of employers who would recommend the RTO | calc_one_question_measure |
| Measure 16 | Student | Proportion of students satisfied with the RTO | calc_one_question_measure |
