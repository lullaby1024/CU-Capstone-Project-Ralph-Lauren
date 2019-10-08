# # Data Cleaning

# ## Overview
import pandas as pd
sales = pd.read_excel("./data/Capstone Project Data Extract - Sales.xlsx", header=2)
traffic = pd.read_excel("./data/Capstone Project Data Extract - Traffic.xlsx", header=2)
sales_t = pd.read_excel("./data/Capstone Project Data Extract - Sales - Tannersville.xlsx", header=0)
traffic_t = pd.read_excel("./data/Capstone Project Data Extract - Traffic - Tannersville.xlsx", header=0)
sales_new = pd.read_excel("./data/Capstone Project Data Extract - Sales - Aug Sept.xlsx", header=0)
traffic_new = pd.read_excel("./data/Capstone Project Data Extract - Traffic - Aug Sept.xlsx", header=0)

# Take out data for FY2020, Sept
sales = sales[sales.Month != 'FY2020 - September']
traffic = traffic[traffic.Month != 'FY2020 - September']

# Take out data for TANNERSVILLE FOC/TANNERSVILLE
sales = sales[sales['Unnamed: 1'] != 'TANNERSVILLE FOC']
traffic = traffic[traffic['Unnamed: 1'] != 'TANNERSVILLE FOC']

sales_new = sales_new[sales_new['Unnamed: 1'] != 'TANNERSVILLE FOC']
sales_new = sales_new[sales_new['Unnamed: 1'] != 'TANNERSVILLE']
traffic_new = traffic_new[traffic_new['Unnamed: 1'] != 'TANNERSVILLE FOC']
traffic_new = traffic_new[traffic_new['Unnamed: 1'] != 'TANNERSVILLE']

# Merging data for FY2020, Sept
sales = pd.concat([sales, sales_new[sales_new.Month == 'FY2020 - September']],
                 ignore_index=True)
traffic = pd.concat([traffic, traffic_new[traffic_new.Month == 'FY2020 - September']],
                   ignore_index=True)

# Merging data for Tannersville
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

# ## Renaming columns
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
sales.date = pd.to_datetime(sales.date, format='%b-%d-%Y')
traffic.date = pd.to_datetime(traffic.date, format='%b-%d-%Y')

# ## Merging tables
assert sales.store.unique().all() == traffic.store.unique().all()
assert sales.date.nunique() == traffic.date.nunique()

df = pd.merge(sales, traffic,
              on=['store', 'store_name', 'year', 'month','month_end', 'week', 'date'])

df.head(5)
df.to_csv ('sales-traffic data cleaned.csv', index=None, header=True)