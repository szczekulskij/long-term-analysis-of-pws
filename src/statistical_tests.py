import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean as get_mean
from scipy.stats import chi2_contingency
import scipy.stats as stats
from scipy.stats import ttest_rel as ttest_related
from scipy.stats import ttest_ind as ttest_not_related


from src.utils import add_grouped_by_time_column
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
    df['mean improvement below 0'] = df.apply(lambda row: False if row['total_clearence_in_between_visits'] > 0 else True, axis = 1 )
    if display_data:
        display(df.head(5))


    df.rename(columns = {'time_group' : 'days passed'}, inplace = True)
    column_name = 'days passed'
    data = df.groupby(by = ['mean improvement below 0', column_name], as_index = False).count()
    data = data[['mean improvement below 0', column_name, 'surname']].rename(columns = {'surname' : 'count'})
    data = data.pivot(index = 'mean improvement below 0', columns = column_name, values = 'count')
    if display_data:
        print('GROUPS:', DEFAULT_GROUPS)
        display(data)

    # chi_squared test
    # chi2 = test statistics, p - pvalue, dof - degrees of freedom, ex = expected frequencies
    chi2, p, dof, ex = chi2_contingency(np.array(data))
    print(f'p-value of chi squred contigency test for {name}: {p} (w. Yates correction - good practice)')

    expected_frequences = pd.DataFrame(ex, index= ['False', 'True'])
    if display_data:
        print('expected frequencies were:')
        display(expected_frequences)

    return data, expected_frequences





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


def bucket_anova_n_plot(
    bucket_column = 'visit_number',
    variable_column = 'total_clearence_in_respect_to_beginning',
    buckets = [1,3,6,10,15],
):

    df = get_data(format_type='all', remove_minus_ones = False)
    data_dict = {}
    data_2d_arr = []
    for i in range(len(buckets) - 1):
        bucket_min = buckets[i]
        bucket_max = buckets[i+1]
        bucket_range = f"{bucket_min} - {bucket_max - 1}"

        visits_data = list(df.loc[(df[bucket_column] >= bucket_min) & (df[bucket_column] < bucket_max)][variable_column])
        data_dict[bucket_range] = visits_data
        data_2d_arr.append(visits_data)

    _, p_value = stats.f_oneway(*data_2d_arr)
    print('\n\n\n')
    print('anova results:')
    print(f'buckets: {buckets}')
    print(f'p_value: {p_value}\n')

    to_be_plot_data = []
    means = []
    p_values = []
    prev_data = ''
    prev_bucket_range = ''
    bucket_ranges = []
    for bucket_range, data in data_dict.items():
        means.append(round(get_mean(data),2))
        bucket_ranges.append(bucket_range)
        if prev_data == '' :
            prev_data = data
            prev_bucket_range = bucket_range
            continue

        left_mean = round(get_mean(prev_data),2)
        right_mean = round(get_mean(data),2)
        _, p_value = ttest_not_related(prev_data, data, alternative= 'less')
        p_value = round(p_value,5)
        print(f'statistics between {prev_bucket_range} bucket and {bucket_range} bucket')
        print(f'means: {left_mean} vs {right_mean}')
        print(f"p-value: {p_value}\n")
        p_values.append(p_value)
        to_be_plot_data.append([bucket_range, left_mean, right_mean, p_value])

        prev_data = data
        prev_bucket_range = bucket_range



    # Move it to func

    p_values[2] = 'n.s.'
    plt.figure(figsize=(20,10))
    index = 1
    x_ticks = []
    buckets = []
    for i, bucket_range in enumerate(bucket_ranges):
        if i == 0 or i == len(bucket_ranges) - 1:
            buckets.append(bucket_range)
        else : 
            buckets.append(bucket_range)
            buckets.append(bucket_range)

    for i, mean in enumerate(means):
        X_AXIS_INCREMENT = 0.5
        BREAK_INCREMENT = 2

        if index == 1:
            X_axis_index = X_AXIS_INCREMENT * index
            data = mean

        elif i == len(means) - 1 :
            X_axis_index = X_AXIS_INCREMENT * index
            data = mean

        else :
            X_axis_index = [index * X_AXIS_INCREMENT, (index + 2) * X_AXIS_INCREMENT ]
            data = [mean, mean]
            index += BREAK_INCREMENT

        plt.bar(X_axis_index, data, 0.4)
        # print(X_axis_index)
        index += 1


        # Get ticks
        if type(X_axis_index) == list:
            for i in X_axis_index:
                x_ticks.append(i)
        else :
            x_ticks.append(X_axis_index)


        
    plt.xticks(x_ticks, buckets)
    plt.xlabel('number of laser sessions (clustered into buckets)', fontsize=17)
    plt.ylabel('% mean improvement\n(total clearance)\n', fontsize=19)
    ax = plt.gca()


    # Handle labels:
    labels_places = []
    for i in range(len(x_ticks) - 1):
        if i%2 == 1:
            continue
        before = x_ticks[i]
        after = x_ticks[i+1]
        label_place = (before+after)/2
        labels_places.append(label_place)

    for label, p_value  in zip(labels_places, p_values):
        height = 54.50
        if p_value == 'n.s.':
            text = 'n.s.'
        else : 
            text = f"p-value: {p_value}"
        ax.text(label, height, text, ha="center", va="bottom", size = 18)
    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)

    plt.show()
