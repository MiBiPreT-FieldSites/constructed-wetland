import sys

path = "Users/Aseye001/Sona_Phd/MIBIREM/MiBiPreT_FieldSites/constructed-wetland/scripts/analysis"
sys.path.append(path)

import pandas as pd

#Load the Excel file
excel_file = './cw_T0_BTEXN_.xlsx' 
df = pd.read_excel(excel_file)

# Save the file as CSV

df.to_csv('cw_BTEXN_T0.csv', index=False) 