import matplotlib.pyplot as plt
import sys  
sys.path.insert(0, '/Users/szczekulskij/side_projects/long-term-analysis-of-pws')
from src.generate_df import get_data_df


LINEWIDTH = 5


def graph_agg_metric_over_nr_sessions(metric, agg_type = "mean", cut_last_x_visits = False):
    plt.figure(figsize=(20,10))
    df = get_data_df(metric = metric)
    if cut_last_x_visits:
        df = df.loc[df['visit_nr'] <= cut_last_x_visits]

    grouped_by_visit = df.groupby('visit_nr', as_index = False).agg(agg_type)
    visits = [0] + list(grouped_by_visit['visit_nr'])
    aggregated_column = [0] + list(grouped_by_visit[metric])
    plt.plot(visits, aggregated_column, label = "o", linewidth = LINEWIDTH)
    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)

    # Customizable
    plt.axvline(x=2, color='b', linestyle='--')
    plt.axvline(x=5, color='b', linestyle='--')
    plt.axvline(x=9, color='darkorange', linestyle='-',  lw = 9)

    ## NeW
    plt.xlabel("number of laser sessions", size = 30)
    plt.ylabel("mean improvement (total clearence)", size = 30)