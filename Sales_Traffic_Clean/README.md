# Sales/Traffic Data Cleaning Instructions

### Two files provided in this folder:
1. **Sales traffic Clean.ipynb**
the python code used for sales/traffic data cleaning
2. **helper_table_holidays.csv**
the holidays used for noise pattern removal, contains: public holidays, promotion days, reservations(non-public holidays, eg.father's day), and severe weathers(eg. tornado warnings)

*note: when you run the function, please keep the holidays file "helper_table_holidays.csv" in the same folder with "Sales traffic Clean.ipynb"*

### How to use the files:
1. **sales cleaning** 
-function：clean_sales_data
-input parameters: input_flie_path: the path of the original sales data file need to be cleaned in .csv format, output_file_path: the path of the cleaned sales data file in .csv format
-output: a .csv file with the cleaned sales data in the output_file_path
-output file format: it contains date, sales_original, sales_cleaned, trend, holidays pattern, weekly pattern, yearly pattern.
example:
```
input_file_path = "salea_traffic_cleaned_for_pattern_removal/1208_Orlando_FOA_sales_traffic_data.csv"
output_file_path = '/Users/yawenhan/Desktop/1208_Orlando_FOA_FOA_sales_cleaned.csv'
clean_sales_data(input_file_path, output_file_path)
```

2. **traffic cleaning**
-- function：clean_traffic_data
-- input parameters: input_flie_path: the path of the original traffic data file need to be cleaned in .csv format, output_file_path: the path of the cleaned traffic data file in .csv format
--output: a .csv file with the cleaned traffic data in the output_file_path
--output file format: it contains date, traffic_original, traffic_cleaned, trend, holidays pattern, weekly pattern, yearly pattern.
example:
```
input_file_path = "salea_traffic_cleaned_for_pattern_removal/1208_Orlando_FOA_sales_traffic_data.csv"
output_file_path = '/Users/yawenhan/Desktop/1208_Orlando_FOA_traffic_cleaned.csv'
clean_traffic_data(input_file_path, output_file_path)
```



