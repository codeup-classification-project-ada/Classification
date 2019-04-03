# this file will hold all necessary functions for transforming and preparing the telco Telco datafram
# 
import pandas as pd

def df_head(dataframe):
    
#     print('df head:')
    return dataframe.head()

def df_tail(dataframe):    
#     print('df tail:')
    return dataframe.tail()
    
def df_shape(dataframe):
#     print('df shape:')
    return dataframe.shape

def df_describe(dataframe):
#     print('df described:')
    return dataframe.describe()
    

# #     index_dtype = 
# #     return index_dtype

def df_types(dataframe):
#     print('df types:')
    return dataframe.dtypes

def peekatdata(dataframe):
    peekatda = dataframe\
        .pipe(df_head)\
        .pipe(df_tail)\
        .pipe(df_describe)
        # .pipe(df_types)\
#         .pipe(df_shape)\
        
    return peekatda