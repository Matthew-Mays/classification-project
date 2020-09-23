#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.model_selection import train_test_split
from acquire import get_telco_data


# In[77]:


def prep_telco_data():
    # Use acquire file to import telco data
    df = get_telco_data()
    # Drop duplicates if there are any
    df.drop_duplicates(inplace=True)
    #
    payment_type_cols = [1, 2, 3, 4]
    df['is_automatic_payment'] = df.payment_type_id.replace(payment_type_cols, [0,0,1,1])
    no_internet = ['streaming_movies', 'tech_support', 'streaming_tv', 'online_security', 'online_backup', 'device_protection']
    df[no_internet] = df[no_internet].replace({'No internet service': 0, 'No': 1, 'Yes': 2})
    binary_cols = ['churn', 'partner', 'dependents', 'phone_service', 'multiple_lines', 'paperless_billing']
    df[binary_cols] = df[binary_cols].replace('Yes', 1).replace('No', 0)
    df.rename(columns={'gender':'male'}, inplace=True)
    df['male'] = df['male'].replace('Male', 1).replace('Female', 0)
    df['total_charges'] = df.total_charges.where((df.tenure != 0), 0)
    df = df.astype({'total_charges':'float64'})
    df['phone_lines'] = df['multiple_lines'].replace({'No phone service': 0, 'No': 1, 'Yes': 2})
    df.drop(columns='multiple_lines')
    df.rename(columns={'tenure':'monthly_tenure'}, inplace=True)
    df['yearly_tenure'] = round(df.monthly_tenure / 12, 2)
    df['part_depend'] = df['partner'] + df['dependents']
    df = df.drop(df[((df['monthly_tenure'].sort_values() == 0))].index)
    internet_types = [1, 2, 3]
    df['fiber'] = df['internet_service_type_id'].replace(internet_types, [0, 1, 0])
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    return train, validate, test


# In[ ]:




