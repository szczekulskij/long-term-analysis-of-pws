from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utils import add_grouped_by_time_column
from scipy.stats import pearsonr
from scipy.stats import ttest_rel as ttest_related
from scipy.stats import ttest_ind as ttest_not_related
from src.load_data import get_data

def get_stats_for_abstract(df = None, format_type = None):

    if df and not format_type:
        df = df
        print('REMEMBER TO NOT REMOVE -1S!, call format_type instead - it wont remove 0s!')
    elif not df and format_type:
        df = get_data(format_type, remove_minus_ones = False)

    data = df.groupby(by  = 'surname', as_index = False).agg({'total_clearence_in_respect_to_beginning' : 'max'})
    all_patients = len(data)

    x = data.total_clearence_in_respect_to_beginning.median()
    print('median of maximum total clearence:', x)

    x = len(data.loc[data['total_clearence_in_respect_to_beginning'] >=25] )
    x = x / all_patients * 100 
    print('% of patients that had a total_clearence of minimum 25%:', x)

    x = len(data.loc[data['total_clearence_in_respect_to_beginning'] >=50] )
    x = x / all_patients * 100 
    print('% of patients that had a total_clearence of minimum 50%:', x)

    x = len(data.loc[data['total_clearence_in_respect_to_beginning'] >=75] )
    x = x / all_patients * 100 
    print('% of patients that had a total_clearence of minimum 75%:', x)

    x = len(data.loc[data['total_clearence_in_respect_to_beginning'] >=90] )
    x = x / all_patients * 100 
    print('% of patients that had a total_clearence of minimum 90%:', x)

    return data

def get_stats_for_abstract2(df = None, format_type = None, visit_number_buckets = 0):

    if df and not format_type:
        df = df
        print('REMEMBER TO NOT REMOVE 0S!, call format_type instead - it wont remove 0s!')
    elif not df and format_type:
        df = get_data(format_type, remove_minus_ones = False)

    if visit_number_buckets == 0 :
        raise Exception('something went wrong')

    maxes = []
    for next_bucket in visit_number_buckets:
        if next_bucket == 0:
            previous_bucket = 0
            continue
        print('bucket:', next_bucket)
        data = df.loc[(df['visit_number'] <= next_bucket )]
        data = data.groupby(by  = 'surname', as_index = False).agg({'total_clearence_in_respect_to_beginning' : 'max'})
        max_total_clearaence = data.total_clearence_in_respect_to_beginning.median()
        maxes.append(max_total_clearaence)
        previous_bucket = next_bucket

    print(maxes)
    return data


def chi_squared_test(df, GROUPS = [], increment = 90, display_data = False, name = '', column_name = 'time_group'):
    from src.utils import DEFAULT_GROUPS
    if GROUPS and increment:
        df = add_grouped_by_time_column(df, GROUPS, increment)
        DEFAULT_GROUPS = GROUPS
    
    # chi squared data
    df['below 0'] = df.apply(lambda row: False if row['total_clearence_in_between_visits'] > 0 else True, axis = 1 )
    if display_data:
        display(df.head(5))

    data = df.groupby(by = ['below 0', column_name], as_index = False).count()
    data = data[['below 0', column_name, 'surname']].rename(columns = {'surname' : 'count'})
    data = data.pivot(index = 'below 0', columns = column_name, values = 'count')
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
    df = df[['visit_number', 'total_clearence_in_between_visits', 'time']]

    if time_threshold and not visit_nr_threshold:
        THRESHOLD_VAR = 'time'
        THRESHOLD = time_threshold
        print(f'\ntest for days passsed: {THRESHOLD}')
    elif visit_nr_threshold and not time_threshold:
        THRESHOLD_VAR = 'visit_number'
        THRESHOLD = visit_nr_threshold
        print(f'\ntest for nr visits: {THRESHOLD}')
    else : 
        raise Exception('need to divide into left and right using one of the thresholds! (and only one !)')

    left_data = df.loc[df[THRESHOLD_VAR] <= THRESHOLD]['total_clearence_in_between_visits']
    right_data = df.loc[df[THRESHOLD_VAR] > THRESHOLD]['total_clearence_in_between_visits']



    if related_ttest:
        # This is currentely broken due to the sample sizes not being equal!
        # length = len(left_data) if len(left_data) < len(right_data) else len(right_data)
        # left_data_ = left_data.head(length)
        # right_data_ = right_data.head(length)
        # statistics, p_value = ttest_related(left_data_, right_data_, alternative = 'greater')
        statistics, p_value = ttest_related(left_data, right_data, alternative = 'greater')
    else :
        statistics, p_value = ttest_not_related(left_data, right_data, alternative = 'greater')

    print('left mean:', round(left_data.mean(),3))
    print('right mean:', round(right_data.mean(),3))
    print('p_value:', round(p_value,4))