from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import add_grouped_by_time_column
from scipy.stats import pearsonr



def chi_squared_test(df, GROUPS = [], increment = 90, display_data = False, name = ''):
    from utils import DEFAULT_GROUPS
    if GROUPS and increment:
        df = add_grouped_by_time_column(df, GROUPS, increment)
        DEFAULT_GROUPS = GROUPS
    
    # chi squared data
    df['below 0'] = df.apply(lambda row: False if row['clearance_between_visit'] > 0 else True, axis = 1 )
    if display_data:
        display(df.head(5))

    data = df.groupby(by = ['below 0', 'time_group'], as_index = False).count()
    data = data[['below 0', 'time_group', 'surname']].rename(columns = {'surname' : 'count'})
    data = data.pivot(index = 'below 0', columns = 'time_group', values = 'count')
    if display_data:
        print('GROUPS:', DEFAULT_GROUPS)
        display(data)

    # chi_squared test
    # chi2 = test statistics, p - pvalue, dof - degrees of freedom, ex = expected frequencies
    chi2, p, dof, ex = chi2_contingency(np.array(data))
    print(f'p-value of chi squred contigency test for {name}: {p} (w. Yates correction - good practice)')

    if display_data:
        print('expected frequencies were:')
        display(pd.DataFrame(ex, index= ['False', 'True']))

def ttest_against_time_threshold(df,time_threshold = 0, visit_nr_threshold=0, related_ttest = True):
    df = df[['visit_number', 'clearance_between_visit', 'time', 'visit_number']]
    if time_threshold and not visit_nr_threshold:
        THRESHOLD_VAR = 'time'
        THRESHOLD = time_threshold
        print('using time (days) threshold')
    elif visit_nr_threshold and not time_threshold:
        THRESHOLD_VAR = 'visit_number'
        THRESHOLD = visit_nr_threshold
        print('using visit nr threshold')
    else : 
        raise Exception('need to divide into left and right using one of the thresholds! (and only one !)')


    left_data = df.loc[df[THRESHOLD_VAR] <= THRESHOLD]['clearance_between_visit']
    right_data = df.loc[df[THRESHOLD_VAR] > THRESHOLD]['clearance_between_visit']


    if related_ttest:
        staistics, p_value = ttest_related(left_data, right_data, alternative = 'greater')
    else :
        staistics, p_value = ttest_not_related(left_data, right_data, alternative = 'greater')

    print('left mean:', round(left_data.mean(),3))
    print('right mean:', round(right_data.mean(),3))
    print('p_value:', p_value)