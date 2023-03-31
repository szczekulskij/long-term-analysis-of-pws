import matplotlib.pyplot as plt
import sys  
sys.path.insert(0, '/Users/szczekulskij/side_projects/long-term-analysis-of-pws')
from src.generate_df import get_data_df
import scipy.stats as stats
from statistics import mean as get_mean
from scipy.stats import ttest_rel as ttest_related
from scipy.stats import ttest_ind as ttest_not_related

def bucketed_anova(
    bucket_column = "visit_nr",
    metric = "total_GCE",
    buckets = [1,3,6,10,15,],
):

    df = get_data_df(metric = metric)
    data_dict = {}
    data_2d_arr = []
    for i in range(len(buckets) - 1):
        bucket_min = buckets[i]
        bucket_max = buckets[i+1]
        bucket_range = f"{bucket_min} - {bucket_max - 1}"
        # Extra special case handle line:
        if bucket_max == 100:
            bucket_range = f"{bucket_min} +"

        visits_data = list(df.loc[(df[bucket_column] >= bucket_min) & (df[bucket_column] < bucket_max)][metric])
        data_dict[bucket_range] = visits_data
        data_2d_arr.append(visits_data)

    _, p_value = stats.f_oneway(*data_2d_arr)
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

        prev_data = data
        prev_bucket_range = bucket_range


    # Format p-values (either to 0 or non-significant)
    new_p_values = []
    for p_value in p_values:
        if p_value > 0.1:
            p_value = "n.s."
        elif p_value <0.001:
            p_value = 0
        new_p_values.append(p_value)
    p_values = new_p_values
    


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
        height = 54.50
        if p_value == 'n.s.':
            text = f"p-value: {p_value}"
        else : 
            text = f"p-value: {float(p_value)}"
        ax.text(label, height, text, ha="center", va="bottom", size = 18)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)