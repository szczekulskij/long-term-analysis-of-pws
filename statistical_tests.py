from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import add_grouped_by_time_column
from scipy.stats import pearsonr



def chi_squared_test(df, GROUPS = [], increment = 90, display_data = False, name = ''):
    from utils import DEFAULT_GROUPS
    if GROUPS and increment:
        df = add_grouped_by_time_column(df, GROUPS, increment)
        DEFAULT_GROUPS = GROUPS
    
    # chi squared data
    df['below 0'] = df.apply(lambda row: False if row['clearance_between_visit'] > 0 else True, axis = 1 )
    if display_data:
        display(df.head(5))

    data = df.groupby(by = ['below 0', 'time_group'], as_index = False).count()
    data = data[['below 0', 'time_group', 'surname']].rename(columns = {'surname' : 'count'})
    data = data.pivot(index = 'below 0', columns = 'time_group', values = 'count')
    if display_data:
        print('GROUPS:', DEFAULT_GROUPS)
        display(data)

    # chi_squared test
    # chi2 = test statistics, p - pvalue, dof - degrees of freedom, ex = expected frequencies
    chi2, p, dof, ex = chi2_contingency(np.array(data))
    print(f'p-value of chi squred contigency test for {name}: {p} (w. Yates correction - good practice)')

    if display_data:
        print('expected frequencies were:')
        display(pd.DataFrame(ex, index= ['False', 'True']))
