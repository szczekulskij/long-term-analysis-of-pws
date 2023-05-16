import matplotlib.pyplot as plt
import numpy as np

import sys  
sys.path.insert(0, '/Users/szczekulskij/side_projects/research_projects/long-term-analysis-of-pws')
from src.generate_df import get_data_df
from src.utils import add_bucketed_time_column_to_df
from statistics import mean


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
    # plt.figure(figsize=(20,10))
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
    visits_per_bucket = grouped_by_bucket[metric].count()
    visits_per_bucket.rename(columns = {metric : 'visits_per_bucket'}, inplace = True)
    visits_per_bucket["bucket"] = ticks_labels
    display(visits_per_bucket)



## Figure 6 graphs:
SURNAMES = ["17.Górszczak", "13.Zborowski", "35.Twardzik"]
DATA = {
    # It's all in total's GCE
    "13.Zborowski" : {
        "max" : 77.37903,
        "break_time" : 1867,
        "after_break" : 57.2239,
        "after_2_visits" : 81.18361
    },
    
    "17.Górszczak" : {
        "max" : 76.61975,
        "break_time" : 1647,
        "after_break" : 31.79399,
        "after_2_visits" : 69.8795
    },
    
    "35.Twardzik" : {
        "max" : 84.65033,
        "break_time" : 1860,
        "after_break" : 51,
        "after_2_visits" : 74 
    }
}
def plot_fig5A_graphs():
    y_labels = ["before treatment", "after treatment", "after break", "after 2 extra sessions"]
    fig, axs = plt.subplots(3, sharex=True, sharey=True)
    fig.supylabel("% improvement (GCE)", size = 30)
    fig.set_size_inches(20,10)

    i = 0 
    for surname, patients_data in DATA.items():
        max = patients_data["max"]
        # break_time = patients_data["break_time"])
        after_break = patients_data["after_break"]
        after_2_visits = patients_data["after_2_visits"]
        data = [0, max, after_break, after_2_visits]

        axs[i].plot(y_labels, data, linewidth = LINEWIDTH)
        for label in (axs[i].get_xticklabels() + axs[i].get_yticklabels()):
            label.set_fontsize(21)
        i+=1


def plot_fig5B_graph():
    max_GCE = []
    break_time = []
    after_break_GCE = []
    after_2_visits_GCE = []
    relative_GCE_improvement_list = []
    for surname, patients_data in DATA.items():
        max_GCE.append(patients_data["max"])
        break_time.append(patients_data["break_time"])
        after_break_GCE.append(patients_data["after_break"])
        after_2_visits_GCE.append(patients_data["after_2_visits"])

        relative_GCE_improvement = patients_data["after_2_visits"] / patients_data["after_break"] * 100
        relative_GCE_improvement_list.append(relative_GCE_improvement)

    means = [
        0,
        mean(max_GCE),
        mean(after_break_GCE),
        mean(after_2_visits_GCE)
    ]
    y_labels = ["before treatment", "after treatment", "after break", "after 2 extra sessions"]
    plt.plot(y_labels, means, linewidth = LINEWIDTH)
    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(21)


    # Get other statistics
    print("% mean improvement (GCE) before treatment: ", 0)
    print("% mean improvement (GCE) after treatment: ", round(mean(max_GCE),2))
    print("% mean improvement (GCE) after break: ", round(mean(after_break_GCE),2))
    print("% mean improvement (GCE) after 2 extra visits: ",  round(mean(after_2_visits_GCE),2))
    print("% mean relative improvement (GCE) after 2 extra visits: ",  round(mean(relative_GCE_improvement_list),2))