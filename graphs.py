import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_summed_plot(df, agg = 'mean'):
    grouped_by_visit = df.groupby('visit_number', as_index = False).agg({'time' : 'mean', 'total_clearance_between_visit' : 'mean', 'clearance_between_visit' : 'mean'}, as_index = False)
    visits = [0] + list(grouped_by_visit['visit_number'])
    summed_clearances = [0] + list(grouped_by_visit['total_clearance_between_visit'])
    plt.plot(visits, summed_clearances)