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
df['measure5_check'] = calc_multi_measure(df=df, components=['s_sat_prob','s_sat_team','s_sat_num','s_sat_engwrt','s_sat_sc'], output_name='measure5_check')

# Based on a single variable
df['measure9_check'] = calc_one_question_measure(df=df, colname='s_achiev', output_name='measure9_check')
```

## Reference

The table below shows the performance measures and the correct function to use to calculate the performance measure.

| Measure | Survey | Description | Function |
|:--------|:-------|:------------|----------|
| Measure 1 | Student | Improved employment status after training |  |
| Measure 5 | Student | Satisfied with generic skills and learning experiences | calc_multi_measure |
| Measure 6 | Employer | Improvement in generic skills and learning experiences | calc_multi_measure |
| Measure 7 | Student | Went on to further study at a higher level |  |
| Measure 8 | Student | Employed in the same occupation/industry as their course |  |
| Measure 9 | Student | Achieved their main reason for study | calc_one_question_measure |
| Measure 10 | Student | Positive perception of teaching | calc_multi_measure |
| Measure 12 | Student | Recommend the RTO | calc_one_question_measure |
| Measure 13 | Student | Positive perception of the assessment process | calc_multi_measure |
| Measure 14 | Employer | Satisfied with training provided by an RTO | calc_one_question_measure |
| Measure 15 | Employer | Recommend the RTO | calc_one_question_measure |
| Measure 16 | Student | Satisfied with the RTO | calc_one_question_measure |
