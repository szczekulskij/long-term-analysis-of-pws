import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import add_grouped_by_time_column

LINEWIDTH = 5

def agg_column_graph(df, agg = 'mean', title = '', label = '', column = 'clearance_between_visit'):
    grouped_by_visit = df.groupby('visit_number', as_index = False).agg({'time' : agg, 'total_clearance_between_visit' : agg, 'clearance_between_visit' : agg}, as_index = False)
    visits = [0] + list(grouped_by_visit['visit_number'])
    plt.title(f"sredni zsumowany clearence between visits {title}")
    aggregated_column = [0] + list(grouped_by_visit[column])
    plt.plot(visits, aggregated_column, label = label, linewidth = LINEWIDTH)
    plt.xlabel('visit number')
    plt.ylabel(f'{agg} {column}')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend()
    

def time_group_based_avg_graph(df, agg = 'mean', title = '', label = '', column = 'clearance_between_visit', GROUPS = [], increment = 90):
    from utils import DEFAULT_GROUPS

    if GROUPS and increment:
        df = add_grouped_by_time_column(df, GROUPS, increment)
        DEFAULT_GROUPS = GROUPS
    elif GROUPS:
        raise Exception('You need to input both GROUPS and increment!')


    grouped_by_visit = df.groupby('time_group', as_index = False).agg({'time' : agg, 'total_clearance_between_visit' : agg, 'clearance_between_visit' : agg}, as_index = False)
    time_groups = list(grouped_by_visit['time_group'])
    aggregated_column = list(grouped_by_visit[column])
    plt.title(f"sredni zsumowany clearence between visits {title}")
    plt.plot(time_groups, aggregated_column, label = label, linewidth = LINEWIDTH)
    plt.xlabel('czas uplyniety (pogrupowany!)')
    try:
        plt.xticks(time_groups, DEFAULT_GROUPS)
    except:
        NEW_DEFAULT_GROUPS = []
        for index in time_groups:
            NEW_DEFAULT_GROUPS.append(DEFAULT_GROUPS[index])
        plt.xticks(time_groups, NEW_DEFAULT_GROUPS)

    plt.ylabel(f'{agg} {column}')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend()


    # Return nr of patients_per_bucket
    grouped_by_visit = df.groupby('time_group', as_index = False)
    patients_per_bucket = grouped_by_visit['------------'].count()
    patients_per_bucket.rename(columns = {'------------' : f'patients_in_bucket {label}'}, inplace = True)
    patients_per_bucket['time_group'] = patients_per_bucket['time_group'] * increment
    return patients_per_bucket

def graph_multiple_time_group_based_avg_graph(df, blizsze = False, GROUPS = [], increment = 90):
    from utils import DEFAULT_GROUPS
    if GROUPS and increment:
        DEFAULT_GROUPS = GROUPS
    multiple_patients_per_bucket = pd.DataFrame(DEFAULT_GROUPS, columns =['time_group'])

    plt.figure(figsize=(20,10))
    
    if not blizsze :
        # for i in [20,15,10,5,0]:
        for i in [10,5,0]:
            patients_per_bucket = time_group_based_avg_graph(df.loc[df.visit_number >= i], label = f'wizyty {i} i dalsze', GROUPS = GROUPS, increment = increment)
            multiple_patients_per_bucket = multiple_patients_per_bucket.merge(patients_per_bucket, on = 'time_group', how = 'outer').fillna(0).astype('int64')
        plt.title('wizyty dalsze')
    else :
        # for i in [20,15,10,5,0]:
        for i in [10,5,0]:
            patients_per_bucket = time_group_based_avg_graph(df.loc[df.visit_number <= i], label = f'wizyty {i} i blizsze', GROUPS = GROUPS, increment = increment)
            multiple_patients_per_bucket = multiple_patients_per_bucket.merge(patients_per_bucket, on = 'time_group', how = 'outer').fillna(0).astype('int64')
        plt.title('wizyty blizsze')
    return multiple_patients_per_bucket



#############################################################################
############################ DEPRECATED GRAPHS ############################

def time_based_avg_graph(df, agg = 'mean', label = ''):
    grouped_by_visit = df.groupby('time', as_index = False).agg({'time' : 'mean', 'total_clearance_between_visit' : 'mean', 'clearance_between_visit' : 'mean'}, as_index = False)
    time = [0] + list(grouped_by_visit['time'])
    aggregated_column = [0] + list(grouped_by_visit['clearance_between_visit'])
    plt.plot(time, aggregated_column, label = label)
    plt.xlabel('visit number')
    plt.ylabel('mean poprawa')
    plt.axhline(y=0, color='r', linestyle='-')


def plot_all_users(df, title = ''):
    unique_surnames = df.surname.unique()
    grouped = df.groupby(df.surname)
    plt.figure(figsize=(30,15))
    for surname in unique_surnames:
        df_new = grouped.get_group(surname)
        visits = [0] + list(df_new['visit_number'])
        aggregated_column = [0] + list(df_new['total_clearance_between_visit'])
        plt.plot(visits, aggregated_column, label = surname)
    
    plt.xlabel('visit number')
    plt.ylabel('mean clearance_between_visit')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend()
    plt.title(title)
    plt.xlim(0,20)