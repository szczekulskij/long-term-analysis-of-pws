from numpy.lib.function_base import disp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utils import add_grouped_by_time_column, add_grouped_by_nr_visit_column
from scipy.stats import pearsonr
from src.statistical_tests import chi_squared_test

LINEWIDTH = 5

def get_name(column):
    '''get name from a column'''
    column_word_list = column.split('_')
    name = ''
    for word in column_word_list:
        name+= word
        name+= ' '
    return name

def agg_column_graph(df_, agg = 'mean', title = '', label = '', column = 'total_clearence_in_between_visits', cut_last_x_visits = False):


    df = df_.copy(deep = True)

    if cut_last_x_visits:
        if type(cut_last_x_visits) != int:
            raise Exception(f'cut_last_x_visits variable should be an int but was: {type(cut_last_x_visits)}')
        df = df.loc[df['visit_number'] <= cut_last_x_visits]


    grouped_by_visit = df.groupby('visit_number', as_index = False).agg({'time' : agg, 'total_clearence_in_between_visits' : agg, 'total_clearence_in_respect_to_beginning' : agg}, as_index = False)
    visits = [0] + list(grouped_by_visit['visit_number'])
    plt.title(title, fontsize=16)
    aggregated_column = [0] + list(grouped_by_visit[column])
    plt.plot(visits, aggregated_column, label = label, linewidth = LINEWIDTH)
    plt.xlabel('number of laser sessions', fontsize=16)
    column_name = get_name(column)
    # plt.ylabel(f'{agg} {column_name}', fontsize=16)
    plt.ylabel(f'% mean improvement (total clearence)', fontsize=16)

    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend()

    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)
    

def time_group_based_avg_graph(df, agg = 'mean', title = '', label = '', column = 'total_clearence_in_between_visits', GROUPS = [], increment = 90, display_data_for_chi_square_test = False, base_column = 'time_group', skip_linear_fit = False):


    def get_labels(groups, increment):
        '''
        Given an array of groups - like [0,90,180,270,360] and their increment like 90
        output labels for the plot to be built in form like: ['0-45', '46-90' ...]s
        '''
        output_labels = []
        for i,_ in enumerate(groups):
            if i == 0 :
                label = f'{i} - {int(i * increment + increment/2)}'
            else : 
                label = f'{int(i * increment - increment/2) + 1} - {int(i * increment + increment/2)}'
            output_labels.append(label)
        return output_labels

    from src.utils import DEFAULT_GROUPS
    if base_column not in ['nr_visit_group', 'time_group']:
        raise Exception('base_column has to be one of the following:', ['nr_visit_group', 'time_group'])

    if GROUPS and increment:
        if base_column == 'time_group':
            df = add_grouped_by_time_column(df, GROUPS, increment)
        elif base_column == 'nr_visit_group':
            df = add_grouped_by_nr_visit_column(df, GROUPS, increment)
        DEFAULT_GROUPS = GROUPS
    elif GROUPS:
        raise Exception('You need to input both GROUPS and increment!')


    grouped_by_visit = df.groupby(base_column, as_index = False).agg({'time' : agg, 'total_clearence_in_between_visits' : agg, 'total_clearence_in_respect_to_beginning' : agg}, as_index = False)
    time_groups = np.array(list(grouped_by_visit[base_column]))
    aggregated_column = list(grouped_by_visit[column])
    plt.title(f"sredni mean clearence between visits {title}", fontsize=16)
    plt.plot(time_groups, aggregated_column, label = label, linewidth = LINEWIDTH)
    plt.xlabel('Days passed between two consecutive visits\n (clustered into buckets)', fontsize=16)
    
    try:
        plt.xticks(time_groups, get_labels(DEFAULT_GROUPS, increment))
    except:
        NEW_DEFAULT_GROUPS = []
        for index in time_groups:
            NEW_DEFAULT_GROUPS.append(DEFAULT_GROUPS[index])
        plt.xticks(time_groups, get_labels(NEW_DEFAULT_GROUPS, increment))


    if not skip_linear_fit:
        
        # Get lineary fit graph:
        # x = np.array(time_groups)
        # y = aggregated_column
        m, b = np.polyfit(time_groups, aggregated_column, 1)
        plt.plot(time_groups, m*time_groups + b, '--', linewidth = 2, linestyle = '--')
        # calculate the Pearson's correlation between two variables
        corr, _ = pearsonr(time_groups, aggregated_column)
        print(f'Pearsons correlation of the linear fit for {label}: %.3f' % corr, '(very bad practice though)')



    column_name = get_name(column)
    plt.ylabel(f'% mean improvement\n inbetween visits\n', fontsize=16)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.legend()


    # Return nr of patients_per_bucket
    grouped_by_visit = df.groupby(base_column, as_index = False)
    patients_per_bucket = grouped_by_visit['------------'].count()
    patients_per_bucket.rename(columns = {'------------' : f'patients_in_bucket {label}'}, inplace = True)
    patients_per_bucket[base_column] = patients_per_bucket[base_column] * increment

    # chi squared contigency test
    # chi_squared_test(df, GROUPS, increment, display_data_for_chi_square_test, name = label, column_name = base_column)
    # print()

    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)

    return patients_per_bucket

def graph_multiple_time_group_based_avg_graph(df, blizsze = False, GROUPS = [], increment = 90, skip_linear_fit = False, wizyty_iteration = [10,5,3,0]):
    from src.utils import DEFAULT_GROUPS
    if GROUPS and increment:
        DEFAULT_GROUPS = GROUPS
    multiple_patients_per_bucket = pd.DataFrame(DEFAULT_GROUPS, columns =['time_group'])

    plt.figure(figsize=(20,10))
    
    if not blizsze :
        # for i in [20,15,10,5,0]:
        for i in wizyty_iteration:
            # label = f'wizyty {i} i dalsze'
            if i == 0 :
                label = 'all visits'
            else : 
                label = f'visits with nunber {i} and further'
            patients_per_bucket = time_group_based_avg_graph(df.loc[df.visit_number >= i], label = label, GROUPS = GROUPS, increment = increment, skip_linear_fit = skip_linear_fit)
            multiple_patients_per_bucket = multiple_patients_per_bucket.merge(patients_per_bucket, on = 'time_group', how = 'outer').fillna(0).astype('int64')
    else :
        # for i in [20,15,10,5,0]:
        for i in wizyty_iteration:
            patients_per_bucket = time_group_based_avg_graph(df.loc[df.visit_number <= i], label = f'wizyty {i} i blizsze', GROUPS = GROUPS, increment = increment, skip_linear_fit = skip_linear_fit)
            multiple_patients_per_bucket = multiple_patients_per_bucket.merge(patients_per_bucket, on = 'time_group', how = 'outer').fillna(0).astype('int64')

    # plt.title('correlation between time passed between 2 consecutive visits and total clearence(GCE) between visits', fontsize=30)
    plt.title("")
    plt.xlabel("Days passed betweens two consecutive visits", size = 30)
    plt.ylabel("% relative GCE improvement\n(improvement in-between sessions)", size = 30)


    ax = plt.gca()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14.5)

    return multiple_patients_per_bucket


def scatter_plot_against_time(df, label = '', label2 = '', plot_linear_fit = True):
    from scipy.stats import linregress
    x = df['time']
    y = df['total_clearence_in_between_visits']
    results = linregress(x,y)
    print(results.pvalue)
    print(results.rvalue)
    print(results.intercept_stderr)
    # slope, intercept, r_value, pvalue, stderr, intercept_stderr
    m, b = np.polyfit(x, y, 1)
    x = [min(365,i) for i in x]
    plt.scatter(x,y, label = label)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.xlabel('time passed (days)')
    plt.ylabel('total clearance effect between visits', fontsize=16)
    x = np.array(x)
    m, b = np.polyfit(x, y, 1)
    if plot_linear_fit:
        plt.plot(x, m*x + b, '--', linewidth = 2, linestyle = '--', label = label2)
        # calculate the Pearson's correlation between two variables
        corr, _ = pearsonr(x, y)
        print('Pearsons correlation: %.3f' % corr)

def scatter_plot_against_visit_nr(df, label = '', label2 = '', plot_linear_fit = True, plot_type = 'scatter'):
    if plot_type =='scatter':
        x = np.array(df['visit_number'])
        y = np.array(df['total_clearence_in_between_visits'])
        m, b = np.polyfit(x, y, 1)
        plt.scatter(x,y, label = label)
        if plot_linear_fit:
            # Linear fit to all points
            plt.plot(x, m*x + b, '--', linewidth = 2, linestyle = '--', label = label2)
            corr, _ = pearsonr(x, y)
            print('Pearsons correlation: %.3f' % corr)


    elif plot_type == 'box':
        df[['visit_number', 'total_clearence_in_between_visits']].boxplot(by = 'visit_number',  figsize = [20,10])
        display_df = df.groupby('visit_number').count()[['total_clearence_in_between_visits']].rename(columns = {'total_clearence_in_between_visits' : 'count'})
        
        if plot_linear_fit:
            # Linear fit to mean
            linear_fit_df = df.groupby('visit_number', as_index = False).agg({'total_clearence_in_between_visits':'mean'})[['total_clearence_in_between_visits','visit_number']]
            x = linear_fit_df['visit_number']
            y = linear_fit_df['total_clearence_in_between_visits']
            m, b = np.polyfit(x, y, 1)
            plt.plot(x, m*x + b, '--', linewidth = 2, linestyle = '--', label = label2)
            plt.xlim(0, 25)
            corr, _ = pearsonr(x, y)
            print('Pearsons correlation: %.3f' % corr)
    plt.axhline(y=0, color='r', linestyle='-')
    plt.xlabel('visit nr')
    plt.ylabel('total clearance effect between visits', fontsize=16)





def get_graph_GCE_vs_pct_people():
    from src.load_data import get_data
    def get_pct_of_people_over_x(df, x):
        nr = len(data.loc[data['total_clearence_in_respect_to_beginning'] >=x] )
        pct = round(nr/len(df) * 100, 2)
        return pct

    data = get_data(format_type='all', remove_minus_ones = False).groupby(by  = 'surname', as_index = False).agg({'total_clearence_in_respect_to_beginning' : 'max'})
    x = len(data.loc[data['total_clearence_in_respect_to_beginning'] >=25] )
    list_of_limits = [i for i in range(0,100,5)]
    limits_data = [get_pct_of_people_over_x(data, x) for x in list_of_limits]
    for a,b in zip(limits_data, list_of_limits):
        print(f"limit: {b}. |% patients: {a}")

    plt.figure(figsize=(20,10))
    plt.bar(list_of_limits, limits_data, width = 4)
    plt.xlabel("GCE threshold", size = 30)
    plt.ylabel("% of patients over GCE threshold", size = 30)





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