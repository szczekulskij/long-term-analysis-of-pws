import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

POSSIBLE_INPUTS = ['all', 'moved_to_0', 'all_without_0s']

def get_data(format_type):
    '''
    format_type = 'all' or 'moved_to_0' or 'all_without_0s'
    '''
    if format_type not in POSSIBLE_INPUTS:
        raise Exception(f'Wrong format_type input Jan! You input: {format_type}, but has to be one of {POSSIBLE_INPUTS}')

    df = pd.read_csv('12.11 malformacje kapilarne lon.csv')
    # Fill in data to have surnames at each column
    new_nazwisko = []
    current_surname = ''
    for i in df['nazwisko']:
        if type(i) == str:
            current_surname = i
        new_nazwisko.append(current_surname)
    df['nazwisko'] = new_nazwisko
    df.rename(columns = {'wizyta po ilu zabiegach' : 'visit_number',
                        'poprawa' : 'clearance_between_visit',
                        'czas ' : 'time',
                        'nazwisko' : 'surname',
                        'total clearence effect miedzy sasiednimi wizytami' : 'total_clearance_between_visit'
                        }, inplace = True)

    summed_clearance = []
    current_surname = '1.Gasek'
    current_summed_clearance = 0
    for surname, clearance in zip(df['surname'], df['clearance_between_visit']):
        if surname == current_surname:
            current_summed_clearance+=clearance
        else:
            current_surname = surname
            current_summed_clearance = clearance
        summed_clearance.append(current_summed_clearance)

    df['total_clearance_summed'] = summed_clearance

    #Format column order:
    df['------------'] = ''
    df = df[['surname', 'time', 'visit_number','total_clearance_between_visit', 'total_clearance_summed', '------------', 'clearance_between_visit']]

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