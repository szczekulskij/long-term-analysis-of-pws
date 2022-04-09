def outliers_filtering(df, outlier_filter_type = 'quantile', outlier_column = 'total_clearence_in_between_visits', quantile = 0.1):
    '''

    Parameters
    -----------
    df: pd.DataFrame
    outlier_filter_type: str
        either "quantile" or ...

    outlier_column: str
        either `total_clearence_in_between_visits` or `total_clearence_in_respect_to_beginning`

    Returns
    -----------
    df: filtered df
    removed_outliers: df with outliers
    '''
    STARTING_DF = df.copy(deep = True)
    POSSIBLE_FILTERS = ['quantile']
    POSSIBLE_COLUMNS = ['total_clearence_in_between_visits', 'total_clearence_in_between_visits']

    # Handle parameters
    if outlier_filter_type not in POSSIBLE_FILTERS:
        raise Exception(f'Choose filtering from the list of possible filters: {POSSIBLE_FILTERS}')

    if outlier_column not in POSSIBLE_COLUMNS:
        raise Exception(f'not possible outlier column. Choose one of the possible columns: {POSSIBLE_COLUMNS}')


    # Returns & function calls
    if outlier_filter_type == 'quantile':
        df = quantile_filter(df, outlier_column, quantile)

    elif outlier_filter_type == '':
        pass

    removed_outliers = get_disjoin(STARTING_DF, df)
    return df, removed_outliers


# Define helper functions:
def quantile_filter(df, outlier_column = 'total_clearence_in_between_visits', quantile = 0.1):
    if quantile > 0.5:
        raise Exception('Provide lower quantile only!')
    LOWER_QUANTILE = quantile
    UPPER_QUANTILE = 1 - quantile

    lower_quantile = df[outlier_column].quantile(LOWER_QUANTILE)
    upper_quantile = df[outlier_column].quantile(UPPER_QUANTILE)

    return df.loc[(df[outlier_column] >= lower_quantile) & (df[outlier_column] <= upper_quantile)]

def get_disjoin(df1,df2):
    df = df1.merge(df2, on= list(df1.columns), how='outer', indicator=True)\
            .query('_merge != "both"')\
            .drop(columns='_merge')
    return df