import matplotlib.pyplot as plt
import pandas as pd
import sys  
sys.path.insert(0, '/Users/szczekulskij/side_projects/research_projects/long-term-analysis-of-pws')
from src.generate_df import get_data_df
from scipy.stats import f_oneway
from statistics import mean as get_mean
from scipy.stats import ttest_rel as ttest_related
from scipy.stats import ttest_ind as ttest_not_related
# from scipy.stats import interval as confidence_interval
from scipy import stats
import statsmodels.stats.api as sms



def bucketed_anova(
    bucket_column = "visit_nr",
    metric = "total_GCE",
    buckets = [1,3,6,10,15,],
    ttest_type = None,
    p_value_text_height = None,
    last_bucket_label = None
):
    if ttest_type not in ["greater", "less"] : raise Exception("Wrong ttest_type!")
    df = get_data_df(metric = metric)
    data_dict = {}
    data_2d_arr = []
    for i in range(len(buckets) - 1):
        bucket_min = buckets[i]
        bucket_max = buckets[i+1]
        bucket_range = f"{bucket_min} - {bucket_max - 1}"
        if i == len(buckets) - 2 and last_bucket_label:
            bucket_range = last_bucket_label
        visits_data = list(df.loc[(df[bucket_column] >= bucket_min) & (df[bucket_column] < bucket_max)][metric])
        data_dict[bucket_range] = visits_data
        data_2d_arr.append(visits_data)

    _, p_value = f_oneway(*data_2d_arr)
    print('\n\n\n')
    print('anova results:')
    print(f'buckets: {buckets}')
    print(f'p_value: {p_value}\n')

    means = []
    p_values = []
    prev_data = ''
    prev_bucket_range = ''
    bucket_ranges = []
    for bucket_range, data in data_dict.items():
        means.append(round(get_mean(data),5))
        bucket_ranges.append(bucket_range)
        if prev_data == '' :
            prev_data = data
            prev_bucket_range = bucket_range
            continue
        left_mean = round(get_mean(prev_data),5)
        right_mean = round(get_mean(data),5)
        _, p_value = ttest_not_related(prev_data, data, alternative = ttest_type)
        p_value = round(p_value,5)
        print(f'statistics between {prev_bucket_range} bucket and {bucket_range} bucket')
        print(f'means: {round(left_mean,2)} vs {round(right_mean,2)}')
        print(f"p-value: {round(p_value,3)}\n")
        p_values.append(round(p_value,3))

        prev_data = data
        prev_bucket_range = bucket_range


    # Format p-values (either to 0 or non-significant)
    # new_p_values = []
    # for p_value in p_values:
    #     if p_value > 0.2:
    #         p_value = "n.s."
    #     elif p_value <0.001:
    #         p_value = 0
    #     new_p_values.append(p_value)
    # p_values = new_p_values
    


    # Handle right ticks:
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
        index += 1
        if type(X_axis_index) == list:
            for i in X_axis_index:
                x_ticks.append(i)
        else :
            x_ticks.append(X_axis_index)
    plt.xticks(x_ticks, buckets)




    # Handle labels:
    ax = plt.gca()
    labels_places = []
    for i in range(len(x_ticks) - 1):
        if i%2 == 1:
            continue
        before = x_ticks[i]
        after = x_ticks[i+1]
        label_place = (before+after)/2
        labels_places.append(label_place)

    for label, p_value  in zip(labels_places, p_values):
        if p_value == 'n.s.':
            text = f"p-value: {p_value}"
        else : 
            text = f"p-value: {float(p_value)}"
        ax.text(label, p_value_text_height, text, ha="center", va="bottom", size = 18)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)



    ## Add extra place to generate the CI df
    CI_data = []
    for index in range(len(data_2d_arr)-1):
        left_lift = data_2d_arr[index]
        right_list = data_2d_arr[index+1]
        cm = sms.CompareMeans(sms.DescrStatsW(left_lift), sms.DescrStatsW(right_list))
        a, b = cm.tconfint_diff(alpha=0.05, alternative='two-sided', usevar='unequal')
        a,b = round(a,2), round(b,2)
        CI_data.append((a,b))

    ## Lil transformation of CI_data
    print(CI_data)
    


