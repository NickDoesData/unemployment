from fredapi import Fred
fred = Fred(api_key = '05871cd0f022878907be62a7f0839fae')
import pandas as pd



def get_fred_data(df_inputs):
    """Loops through input file to make multiple API calls to FRED. Input file should have column names \
'name' and 'series_id'. 'name' column will be used to rename columns in the returned df."""
    
    
    #initialize empty dataframe, column list
    df = pd.DataFrame()
    cols = []
    
    #loop through input file calling fred api for each series ID
    for index, row in df_inputs.iterrows():
        cols.append(row['name'])
        x = fred.get_series(row['series_id'])
        x.info = fred.get_series_info(row['series_id'])
        df = pd.concat([df, x], axis=1)

    #rename each series ID based on the 'name' columns of the input file
    df.columns = cols

    return df

def order_df(df):
    """Reorders dataframe columns from greatest to least. Helps with df formatting for charts."""
    
    n = len(df.columns)
    new_columns = df.columns[df.ix[df.last_valid_index()].argsort()[::-1]]
    df = df[new_columns]
    
    return df
    