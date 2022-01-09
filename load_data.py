import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import add_grouped_by_time_column, DEFAULT_GROUPS

POSSIBLE_INPUTS = ['all', 'moved_to_0', 'all_without_0s']

def get_data(format_type, remove_minus_ones = True):

    '''
    format_type = 'all' or 'moved_to_0' or 'all_without_0s'
    '''
    if format_type not in POSSIBLE_INPUTS:
        raise Exception(f'Wrong format_type input Jan! You input: {format_type}, but has to be one of {POSSIBLE_INPUTS}')

    # df = pd.read_csv('12.11 malformacje kapilarne lon.csv')
    df = pd.read_csv('nowe_poprawione_dane.csv')

    # Fill in data to have surnames at each column
    new_nazwisko = []
    current_surname = ''
    for i in df['nazwisko']:
        if type(i) == str:
            current_surname = i
        new_nazwisko.append(current_surname)
    df['nazwisko'] = new_nazwisko
    df.rename(columns = {'wizyta po ilu zabiegach' : 'visit_number',
                        'total clearence pomiedzy wizytami' : 'total_clearance_effect_between_visit',
                        'czas ' : 'time',
                        'nazwisko' : 'surname',
                        'total clearence effect wzgledem poczatku' : 'total_clearence_effect_wzgledem_poczatku'
                        }, inplace = True)


    #Format column order:
    df = get_summed_time_column(df)
    df = add_grouped_by_time_column(df, DEFAULT_GROUPS)
    df['------------'] = ''
    print('default time group has GROUPS defined as:',DEFAULT_GROUPS)
    df = df[['surname', 'time','summed_time','time_group', 'visit_number','total_clearance_effect_between_visit', 'total_clearence_effect_wzgledem_poczatku',  '------------']]

    if remove_minus_ones:
        df = df.loc[df['total_clearance_effect_between_visit'] != -1]

    if format_type == 'all':
        return df
    elif format_type == 'moved_to_0':
        return format_by_moving_to_0(df)
    elif format_type == 'all_without_0s':
        return format_by_removing_non_0s(df)
    else :
        raise Exception(f'Wrong format_type input Jan! You input: {format_type}, but has to be one of {POSSIBLE_INPUTS}')

def format_by_moving_to_0(df):
    unique_surnames = set()
    current_decreament = 0
    moved_to_0_visit_nr = []
    for surname, visit_nr in zip(df['surname'], df['visit_number']):
        if surname not in unique_surnames:
            unique_surnames.add(surname)
            current_decreament = visit_nr - 1
        moved_to_0_visit_nr.append(visit_nr - current_decreament)

    df['unmoved_visit_nr'] = df['visit_number']
    df['visit_number'] = moved_to_0_visit_nr
    return df

def format_by_removing_non_0s(df):
    df = format_by_moving_to_0(df) # Returns df that has changed visitor_nr to moved_visitor_nr and have old visitor_nr saved as unmoved_visit_nr
    df = df.loc[df['visit_number'] == df['unmoved_visit_nr']] # Gets rid of all moved rows - aka, all people that didnt start from 0
    return df

def get_summed_time_column(df):
    summed_time = []
    current_surname = '1.Gasek'
    current_summed_time = 0
    for surname, time in zip(df.surname, df.time):
        if surname == current_surname:
            current_summed_time+=time
        else:
            current_surname = surname
            current_summed_time = time
        summed_time.append(current_summed_time)
    df['summed_time'] = summed_time
    return df