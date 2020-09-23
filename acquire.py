#!/usr/bin/env python
# coding: utf-8

# In[1]:


import env
import pandas as pd
import os


# In[2]:


def get_connection(db, user=env.username, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


# In[3]:


def get_telco_data():
    filename = 'telco.csv'
    if os.path.isfile(filename) == False:
        df = pd.read_sql('''SELECT * FROM customers JOIN internet_service_types 
                        USING(internet_service_type_id)
                        JOIN contract_types USING(contract_type_id)
                        JOIN payment_types USING(payment_type_id)''', get_connection('telco_churn'))
        df.to_csv(filename)
    else:
        df = pd.read_csv(filename, index_col=0)
    return df

