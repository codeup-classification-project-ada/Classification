# this file will hold all necessary functions for acquiring, transforming, and preparing the Telco datafram
import env
import pandas as pd

#   this version uses mysql
def get_mysqlconnection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+mysqlconnector://{user}:{password}@{host}/{db}'

#   this version uses pysql
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_telco_data():
    return pd.read_sql('SELECT c.*, ct.contract_type, ist.internet_service_type, pt.payment_type\
    FROM customers as c\
    JOIN contract_types as ct USING (contract_type_id)\
    JOIN internet_service_types as ist USING (internet_service_type_id)\
    JOIN payment_types as pt USING (payment_type_id);', get_connection('telco_churn'))

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers;', get_connection('titanic_db'))
    
def get_iris_data():
    Sql_str = 'SELECT m.*, s.species_name FROM measurements as m JOIN species as s ON m.species_id=s.species_id'                         
    return pd.read_sql(Sql_str,  get_connection('iris_db')) 

def fix_telco_total_charges(df):
    df['total_charges'] = df['total_charges'].convert_objects(convert_numeric=True)
    df['total_charges'].replace(' ', (df['monthly_charges'] * df['tenure']), inplace=True)
    df.drop(df[df.total_charges == 0].index, inplace=True)
    return(df)

def prep_telco_data(df):
    return df

       
