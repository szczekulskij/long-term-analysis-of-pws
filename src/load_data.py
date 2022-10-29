from turtle import clear
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utils import add_grouped_by_time_column, DEFAULT_GROUPS

POSSIBLE_INPUTS = ['all', 'moved_to_0', 'all_without_0s']

def get_data(format_type, remove_minus_ones = True):

    '''
    This functions reads the data from csv files and transforms it accordingly. (have a look at data.csv file)

    The data in csv file is in form one visit per row
    The data in csv file has holes in it. Aka - we might not have first few visits, or we might not have few visits in between.
    For every visit we could calculate healing in respect to beginning (called total_clearence_in_respect_to_beginning)
    Only when we have 2 visits in the row, can we calculate healing in respect to previous visit (called total_clearence_in_between_visits), 
    Therefore when unable to calculate total_clearence_in_between_visits - instead of empty space, I've put a -1 there.


    Parameters
    ---------------------------------------------------
    format_type: str
        'all' - no changes to data
        'moved_to_0' - move visit_nr of people who didn't have first few visits (Bad practice. Used due to lack of data)
        'all_without_0s' - remove visitors who didn't have the first visit
        

    remove_minus_ones: bool
        Remove visits that didn't have total_clearence_in_between_visits (so they had -1 in place of total_clearence_in_between_visits)
        

    Returns
    ---------------------------------------------------    
    return pd.DataFrame w. visits data
        Each row represents one medical visit which aim was to heal the birth scar (port-wine stain)
        Each row has a data on:
            * surname - surname of patient & nr of patient (ex. 4.Ball)
            * total_clearence_in_between_visits - How sucessful was healing compared to previous visit (in %)
            * total_clearence_in_respect_to_beginning - How sucessful was healing compared to very beginning, before any visits  (in %)
            * time - How many days passed since last visit 
            * visir_number - visit number

    '''
    try : 
        df = pd.read_excel('updated_info.xlsx', sheet_name="wszystkie dane poprawione") 
    except : 
        try :
            df = pd.read_excel('src/updated_info.xlsx', sheet_name="wszystkie dane poprawione") 
        except:
            raise Exception('Data reading went wrong! Fix it !')


    # Fill in data to have surnames in each row
    new_surname = []
    current_surname = ''
    for i in df['nazwisko']:
        if type(i) == str:
            current_surname = i
        new_surname.append(current_surname)
    df['nazwisko'] = new_surname
    df.rename(columns = {'wizyta po ilu zabiegach' : 'visit_number',
                        'total clearence pomiedzy wizytami' : 'total_clearence_in_between_visits',
                        'czas ' : 'time',
                        'nazwisko' : 'surname',
                        'total clearence effect wzgledem poczatku' : 'total_clearence_in_respect_to_beginning'
                        }, inplace = True)


    #Format column order:
    df = get_summed_time_column(df)
    df = add_grouped_by_time_column(df, DEFAULT_GROUPS)
    df['------------'] = ''
    print('default time group has GROUPS defined as:',DEFAULT_GROUPS)
    df = df[['surname', 'time','summed_time','time_group', 'visit_number','total_clearence_in_between_visits', 'total_clearence_in_respect_to_beginning',  '------------', 'previous treatment',]]

    if remove_minus_ones:
        df = df.loc[df['total_clearence_in_between_visits'] != -1]

    if format_type == 'all':
        pass

    elif format_type == 'moved_to_0':
        df = format_by_moving_to_0(df)

    elif format_type == 'all_without_0s':
        df = format_by_removing_non_0s(df)
        
    else :
        raise Exception(f'Wrong format_type input Jan! You input: {format_type}, but has to be one of {POSSIBLE_INPUTS}')

    df = df.reset_index(drop=True)
    return df


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

if __name__ == "__main__":
    df = get_data('all', remove_minus_ones = False)
    print(df)