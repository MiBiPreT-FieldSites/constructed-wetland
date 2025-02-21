import sys

path = "Users/Aseye001/Sona_Phd/MIBIREM/MiBiPreT_FieldSites/constructed-wetland/scripts/analysis"
sys.path.append(path)

import pandas as pd

#Load the Excel file
excel_file = './CW_BTEXN_T0_backup.xlsx' 
df = pd.read_excel(excel_file)

# Save the file as CSV

df.to_csv('CW_BTEXN_T0.csv', index=False) 