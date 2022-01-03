import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DEFAULT_GROUPS = [0,90,180,270,360]


def add_grouped_by_time_column(df, GROUPS):
    labeled_group = []
    for time in df.time:
        group = min(GROUPS, key=lambda x:abs(x-time)) // 90
        labeled_group.append(group)
    df['time_group'] = labeled_group
    return df