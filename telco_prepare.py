# this file will hold all necessary functions for acquiring, transforming, and preparing the Telco datafram
import env
import pandas as pd
from sklearn.preprocessing import LabelEncoder

#   this version uses mysql
def get_mysqlconnection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+mysqlconnector://{user}:{password}@{host}/{db}'

#   this version uses pysql
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers;', get_connection('titanic_db'))
    
def get_iris_data():
    Sql_str = 'SELECT m.*, s.species_name FROM measurements as m JOIN species as s ON m.species_id=s.species_id'                         
    return pd.read_sql(Sql_str,  get_connection('iris_db')) 

def get_telco_data():
    return pd.read_sql('SELECT c.*, ct.contract_type, ist.internet_service_type, pt.payment_type\
    FROM customers as c\
    JOIN contract_types as ct USING (contract_type_id)\
    JOIN internet_service_types as ist USING (internet_service_type_id)\
    JOIN payment_types as pt USING (payment_type_id);', get_connection('telco_churn'))

def create_tenure_year(df):
    df[['tenure_year']] = df[['tenure']] / 12
    return df

def encode_churn(df):
    encoder = LabelEncoder()
    encoder.fit(df.churn)
    return df.assign(churn_encoded = encoder.transform(df.churn))

def fix_telco_total_charges(df):
    df['total_charges'] = df['total_charges'].convert_objects(convert_numeric=True)
    df['total_charges'].replace(' ', (df['monthly_charges'] * df['tenure']), inplace=True)
    df.drop(df[df.total_charges == 0].index, inplace=True)   
    return(df)

def get_phone_id(df):
    rvalue = 0
    if df.multiple_lines.lower() == 'yes':
        rvalue = 2
    elif df.multiple_lines.lower() != 'yes' and df.phone_service.lower() == 'yes':
        rvalue = 1
    else:
        rvalue = 0
    return(rvalue)

def create_tenure_yr_int(df):
    df[['tenure_yr_int']] = df[['tenure_year']].astype(int)   
    return df

def reorder_internet_service_id(df):
    new_value = df.internet_service_type_id
    if df.internet_service_type_id == 3:
        new_value = 0
    return(new_value)

def prep_telco_data(df):
    df = fix_telco_total_charges(df)
    df['percent_var_tc_from_act_tc'] = (df['monthly_charges'] * df['tenure']) / df['total_charges']
    df = encode_churn(df)
    df = create_tenure_year(df)
    df = create_tenure_yr_int(df)
    df['phone_id'] = df.apply(get_phone_id, axis=1)
    df['internet_service_type_id'] = df.apply(reorder_internet_service_id, axis=1)
    return df

       
