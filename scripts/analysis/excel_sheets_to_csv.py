import pandas as pd

#Define the Excel file path
excel_file = './cw_T0_standardiz.xlsx'  

#Read all sheets into a dictionary of DataFrames
sheets_dict = pd.read_excel(excel_file, sheet_name=None)

#Convert all sheets to one DataFrame
df_combined = pd.concat(sheets_dict.values(), axis=1, ignore_index=True)

#Save as a single CSV file
df_combined.to_csv('./cw_T0_BTEXN.csv', index=False)