import pandas as pd
import numpy as np

def add_bucketed_time_column_to_df(df, buckets_nr, increment):
    buckets = [i * increment for i in range(buckets_nr)]
    print("buckets: ", buckets)
    patients_label = []
    for patients_time in df.time:
        i = 0
        while True:
            # print(i)
            if patients_time >  buckets[-1]:
                i = len(buckets) - 1
                break
            if (patients_time > buckets[i] and patients_time < buckets[i+1]) or i == len(buckets) - 1:
                break
            i+=1
        patients_label.append(i)
    df['bucket'] = patients_label
    return df



# Deprecated previous version
def old_add_bucketed_time_column_to_df(df, buckets_nr, increment):
    buckets = [i * increment for i in range(buckets_nr)]
    labeled_group = []
    for time in df.time:
        group = min(buckets, key=lambda x:abs(x-time)) // increment
        labeled_group.append(group)
    df['bucket'] = labeled_group
    return df
