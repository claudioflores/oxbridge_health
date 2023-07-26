import pandas as pd


def pandas_merge_plus(df1, df2, left_on, right_on, validate, no_matches=False):
    if validate not in ['left', 'right', 'both', 'none']:
        raise Exception('Incorrect validate value used. Correct values are: "left", "right", "both", or "none".')     
    aux1 = df1[left_on]
    aux2 = df2[right_on]    
    cols_dict = {x: y for x, y in zip(aux1.columns, aux2.columns)}
    for col in cols_dict:
        if aux1[col].dtypes != aux2[cols_dict[col]].dtypes:
            print(aux1[col].dtypes, aux2[cols_dict[col]].dtypes)
            raise Exception("Column types used to merge '" +col+"' are different")
        set1 = set(aux1[col])
        set2 = set(aux2[cols_dict[col]])
        if validate=='left':
            superset_bool = set1>=set2
        elif validate=='right':
            superset_bool = set1<=set2
        elif validate=='both':
            superset_bool = set1==set2
        else:
            superset_bool = True
        if superset_bool is not True:
            raise Exception("Column '"+col+"' doesn't pass the validation superset check")            
    df = df1.merge(df2, left_on=left_on, right_on=right_on)
    df = df.drop(columns=[x for x in right_on if x not in left_on])    
    if no_matches is True and len(df)==0:
        raise Exception('Merged dataframe is empty.')
    return df
    

df1 = pd.read_csv('problem1_dataframe1.csv')
df2 = pd.read_csv('problem1_dataframe2.csv')

# print(list(pandas_merge_plus(df1, df2, ['Year_Model'], ['Year'], 'none'))) # Checks no duplicate columns are created in merge
# print(pandas_merge_plus(df1, df2, ['Color'], ['Color'], 'left')) # No Exception: passes superset condition
# print(pandas_merge_plus(df1, df2, ['Color'], ['Color'], 'right')) # Raise Exception: superset condition
# print(pandas_merge_plus(df1, df2, ['Color'], ['Color'], 'rigt')) # Raise Exception: wrong validate input
# print(pandas_merge_plus(df1, df2, ['Brand'], ['Brand'], 'both')) # Raise Exception: sets are not equal
# print(pandas_merge_plus(df1, df2, ['Brand'], ['Year'], 'both')) # Raise Exception: column types are different
# print(pandas_merge_plus(df1, df2, ['Color', 'Year_Model', 'Brand', 'Type', 'N_Doors'], ['Color', 'Year', 'Brand', 'Type', 'Doors'], 'none', no_matches=True)) # Raise Exception: DataFrame is empty
# print(pandas_merge_plus(df1, df2, ['Color', 'Year_Model', 'Brand', 'Type', 'N_Doors'], ['Color', 'Year', 'Brand', 'Type', 'Doors'], 'none')) # No Exception: DataFrame is empty
print(pandas_merge_plus(df1, df2, ['Color', 'Year_Model', 'Brand', 'Type'], ['Color', 'Year', 'Brand', 'Type'], 'none')) # No Exception
