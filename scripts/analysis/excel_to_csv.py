import sys

path = "Users/Aseye001/Sona_Phd/MIBIREM/MiBiPreT_FieldSites/constructed-wetland/scripts/analysis"
sys.path.append(path)

import pandas as pd

#Load the Excel file
excel_file = '../../data/cleaned/na_screening/cw_T2_BTEXN.xlsx' 
df = pd.read_excel(excel_file)

# Save the file as CSV

df.to_csv('../../data/cleaned/na_screening/cw_T2_BTEXN.csv', index=False) 

#import pandas as pd

# Define the Excel file path
#excel_file = './cw_T0_BTEXN.xlsx'  

# Read all sheets into a dictionary of DataFrames
#sheets_dict = pd.read_excel(excel_file, sheet_name=None)

# Convert all sheets to one DataFrame
#df_combined = pd.concat(sheets_dict.values(), ignore_index=True)

# Save as a single CSV file
#df_combined.to_csv('cw_T0_BTEXN.csv', index=False)
