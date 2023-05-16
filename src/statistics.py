import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import sys  
sys.path.insert(0, '/Users/szczekulskij/side_projects/research_projects/long-term-analysis-of-pws')
from src.generate_df import get_data_df


def get_medians(metric, buckets_visit_nr = [0,2,5,10,15,20], agg_type = "median"):

    if type(buckets_visit_nr) != list: raise Exception()
    df = get_data_df(metric=metric)
    print("metrics: ", metric)

    for bucket in buckets_visit_nr:
        data = df.loc[(df['visit_nr'] <= bucket)]
        maxes = data.groupby(by  = 'surname', as_index = False).agg('max')
        if agg_type == "median":
            median_of_max = maxes[metric].median()
            print(f"for first {bucket} visits, the median maximal {metric} was {round(median_of_max,2)}")
        elif agg_type == "mean":
            mean_of_max = maxes[metric].mean()
            print(f"for first {bucket} visits, the mean maximal {metric} was {round(mean_of_max,2)}")
        else :
            raise Exception("wrong type of agg_type passed in!")


