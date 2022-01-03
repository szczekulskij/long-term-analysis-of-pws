import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def agg_column_graph(df, agg = 'mean', label = '', column = 'clearance_between_visit'):
    grouped_by_visit = df.groupby('visit_number', as_index = False).agg({'time' : agg, 'total_clearance_between_visit' : agg, 'clearance_between_visit' : agg}, as_index = False)
    visits = [0] + list(grouped_by_visit['visit_number'])
    summed_clearances = [0] + list(grouped_by_visit[column])
    plt.plot(visits, summed_clearances, label = label)
    plt.xlabel('visit number')
    plt.ylabel(f'{agg} {column}')
    plt.axhline(y=0, color='r', linestyle='-')
    

def time_group_based_avg_graph(df, agg = 'mean', label = '', column = 'clearance_between_visit'):
    grouped_by_visit = df.groupby('time_group', as_index = False).agg({'time' : 'mean', 'total_clearance_between_visit' : 'mean', 'clearance_between_visit' : 'mean'}, as_index = False)
    time = [0] + list(grouped_by_visit['time_group'])
    summed_clearances = [0] + list(grouped_by_visit[column])
    plt.plot(time, summed_clearances, label = label)
    plt.xlabel('visit group')
    plt.ylabel('mean poprawa')
    plt.axhline(y=0, color='r', linestyle='-')



#############################################################################
############################ LESS USEFUL GRAPHS ############################

def time_based_avg_graph(df, agg = 'mean', label = ''):
    grouped_by_visit = df.groupby('time', as_index = False).agg({'time' : 'mean', 'total_clearance_between_visit' : 'mean', 'clearance_between_visit' : 'mean'}, as_index = False)
    time = [0] + list(grouped_by_visit['time'])
    summed_clearances = [0] + list(grouped_by_visit['clearance_between_visit'])
    plt.plot(time, summed_clearances, label = label)
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
        summed_clearances = [0] + list(df_new['total_clearance_between_visit'])
        plt.plot(visits, summed_clearances, label = surname)
    
    plt.xlabel('visit number')
    plt.ylabel('mean clearance_between_visit')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend()
    plt.title(title)
    plt.xlim(0,20)