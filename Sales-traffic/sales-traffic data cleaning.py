# # Data Cleaning

# ## Overview

import pandas as pd
sales = pd.read_excel("./data/Capstone Project Data Extract - Sales.xlsx", header=2)
traffic = pd.read_excel("./data/Capstone Project Data Extract - Traffic.xlsx", header=2)
sales_t = pd.read_excel("./data/Capstone Project Data Extract - Sales - Tannersville.xlsx", header=0)
traffic_t = pd.read_excel("./data/Capstone Project Data Extract - Traffic - Tannersville.xlsx", header=0)

# Merging tables for Tannersville
sales = sales[sales['Unnamed: 1'] != 'TANNERSVILLE FOC']
traffic = traffic[traffic['Unnamed: 1'] != 'TANNERSVILLE FOC']

sales.Date = pd.to_datetime(sales.Date, format='%b-%d-%Y')
sales_t.Date = pd.to_datetime(sales_t.Date, format='%b-%d-%Y')
traffic.Date = pd.to_datetime(traffic.Date, format='%b-%d-%Y')
traffic_t.Date = pd.to_datetime(traffic_t.Date, format='%b-%d-%Y')

sales_t = sales_t[(sales_t.Date >= min(sales.Date)) & (sales_t.Date <= max(sales.Date))]
traffic_t = traffic_t[(traffic_t.Date >= min(traffic.Date)) & (traffic_t.Date <= max(traffic.Date))]

sales = pd.concat([sales, sales_t], ignore_index=True)
traffic = pd.concat([traffic, traffic_t], ignore_index=True)

sales.info()

sales.head(5)

sales.describe()


# *Remark*
# - No missing values
# - Negative `sales unit` and `sales retail` (refund/store adjustment)

traffic.info()

traffic.head(5)

traffic.describe()

sales.rename(columns={"Unnamed: 1": "store_name",
                      "Group Division": "group_division",
                      "Unnamed: 3": "group_name",
                      "Unnamed: 6": "month_end",
                      "SLS UNT": "sales_unit",
                      "SLS RTL": "sales_retail"},
             inplace=True)

sales.columns = map(str.lower, sales.columns)

sales.head(5)

traffic.rename(columns={"Unnamed: 1": "store_name", 
                        "Unnamed: 4": "month_end",
                        "Traffic Out": "traffic"},
               inplace=True)

traffic.columns = map(str.lower, traffic.columns)

traffic.head(5)

# ## Cleaning data types
sales.info()
traffic.info()

# ## Merging tables
assert sales.store.unique().all() == traffic.store.unique().all()
assert sales.date.nunique() == traffic.date.nunique()
set(traffic.date.unique()) - set(sales.date.unique())

traffic[traffic.date == '2019-08-29']


# **Remark:** Mismatch between sales/traffic data. Sales is missing data for 2019-08-29. For consistency, we will retain records until 2019-08-28 (using inner join by default in Python).

df = pd.merge(sales, traffic,
              on=['store', 'store_name', 'year', 'month','month_end', 'week', 'date'])

df.head(5)
df.to_csv ('sales-traffic data cleaned.csv', index=None, header=True)
