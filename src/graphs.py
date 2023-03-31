import matplotlib.pyplot as plt
import numpy as np

import sys  
sys.path.insert(0, '/Users/szczekulskij/side_projects/long-term-analysis-of-pws')
from src.generate_df import get_data_df
from src.utils import add_bucketed_time_column_to_df


LINEWIDTH = 5


def graph_agg_metric_over_nr_sessions(metric, agg_type = "mean", cut_last_x_visits = False):
    # Get data
    df = get_data_df(metric = metric)
    if cut_last_x_visits:
        df = df.loc[df['visit_nr'] <= cut_last_x_visits]
    grouped_by_visit = df.groupby('visit_nr', as_index = False).agg(agg_type)
    visits = [0] + list(grouped_by_visit['visit_nr'])
    aggregated_column = [0] + list(grouped_by_visit[metric])
    
    # Plot
    plt.figure(figsize=(20,10))
    plt.plot(visits, aggregated_column, label = "o", linewidth = LINEWIDTH)
    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)


def graph_based_on_time_bucket(metric, agg_type = "mean", buckets_nr = 4, increment = 120):
    # Get data
    buckets = [i * increment for i in range(buckets_nr)]
    df = get_data_df(metric = metric)
    df = add_bucketed_time_column_to_df(df, buckets_nr = buckets_nr, increment = increment)
    grouped_by_bucket = df.groupby("bucket", as_index = False).agg(agg_type)
    x = np.array(list(grouped_by_bucket["bucket"]))
    y = list(grouped_by_bucket[metric])

    # Plot
    plt.plot(x, y, linewidth = LINEWIDTH)
    ticks_labels = [f"{buckets[i]} - {buckets[i+1]}" for i in range(len(buckets) - 1)]
    ticks_labels.append(f"{buckets[-1]}+")
    print(ticks_labels)
    plt.xticks(x, ticks_labels)
    plt.axhline(y=0, color='r', linestyle='-')
    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)

    # Calculate nr of patients per bucket
    grouped_by_bucket = df.groupby("bucket", as_index = False)
    patients_per_bucket = grouped_by_bucket[metric].count()
    patients_per_bucket.rename(columns = {metric : f'patients_per_bucket'}, inplace = True)
    patients_per_bucket["bucket"] = ticks_labels
    display(patients_per_bucket)