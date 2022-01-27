import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MAX_VALUE = 360

DEFAULT_GROUPS = [0,90,180,270,360]
DEFAULT_GROUPS_NR_VISIT = [0,5,10,15,20]


def add_grouped_by_time_column(df, GROUPS = DEFAULT_GROUPS, increment = 90):
    labeled_group = []
    for time in df.time:
        group = min(GROUPS, key=lambda x:abs(x-time)) // increment
        labeled_group.append(group)
    df['time_group'] = labeled_group
    return df


def add_grouped_by_nr_visit_column(df, GROUPS = DEFAULT_GROUPS_NR_VISIT, increment = 5):
    labeled_group = []
    for visit_number in df.visit_number:
        group = min(GROUPS, key=lambda x:abs(x-visit_number)) // increment
        labeled_group.append(group)
    df['nr_visit_group'] = labeled_group
    return df