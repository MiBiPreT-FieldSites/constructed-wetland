import sys

path = "Users/Aseye001/Sona_Phd/MIBIREM/MiBiPreT_FieldSites/constructed-wetland/scripts/analysis"
sys.path.append(path)

import pandas as pd

#Load the Excel file
# Relative file path to the excel file with the data
time_point = "3"
excel_file = f"../../data/preprocessed/na_screening/cw_T{time_point}_preprocessed.xlsx"
df = pd.read_excel(excel_file)

# Save the file as CSV
output_file = f"../../data/preprocessed/na_screening/cw_T{time_point}_preprocessed.csv"
df.to_csv(output_file, index=False)

#df.to_csv('../../data/cleaned/cw_T3_BTEXN.csv', index=False) 

#import pandas as pd

# Define the Excel file path
#excel_file = './cw_T0_BTEXN.xlsx'  

# Read all sheets into a dictionary of DataFrames
#sheets_dict = pd.read_excel(excel_file, sheet_name=None)

# Convert all sheets to one DataFrame
#df_combined = pd.concat(sheets_dict.values(), axis=1, ignore_index=True)

# Save as a single CSV file
#df_combined.to_csv('cw_T0_BTEXN.csv', index=False)
