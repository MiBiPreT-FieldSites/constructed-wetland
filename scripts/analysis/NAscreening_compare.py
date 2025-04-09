import mibipret.analysis.sample.screening_NA as na
from mibipret.data.check_data import standardize
from mibipret.data.load_data import load_csv
from IPython.display import display
import pandas as pd

# Define one or more CSV file paths for the same site at different times.

file_paths = [
    "../../data/cleaned/na_screening/cw_T0_BTEXN.csv",
    "../../data/cleaned/na_screening/cw_T1_BTEXN.csv",
    "../../data/cleaned/na_screening/cw_T2_BTEXN.csv"
]

# If only one file path is provided as a string, convert it to a list.
if isinstance(file_paths, str):
    file_paths = [file_paths]

# Dictionary to store the screening results for each file.
results = {}

for file in file_paths:
    print(f"Processing file: {file}")
    # Load raw data and units from the CSV file.
    data_raw, units = load_csv(file, verbose=True)
    
    # Standardize the data (clean the data and reduce it to known quantities).
    data, units = standardize(data_raw, reduce=True, verbose=True)
    
    # Calculate additional outputs for debugging or further analysis.
    tot_redct = na.reductors(data, verbose=True, ea_group="ONS")
    tot_oxi = na.oxidators(data, verbose=True, contaminant_group="BTEX")
    e_bal = na.electron_balance(data, verbose=True)
    na_traffic = na.NA_traffic(data, verbose=True)
    tot_cont = na.total_contaminant_concentration(data, verbose=True, contaminant_group="BTEX")
    na_interventation = na.thresholds_for_intervention(data, verbose=True, contaminant_group="BTEX")
    
    # Get the final NA screening table for this dataset.
    data_na = na.screening_NA(data)
    
    # Use the file name as a key for the results dictionary.
    results[file] = data_na

# If there is only one file, display its output directly.
if len(results) == 1:
    display(list(results.values())[0])
else:
    # Combine the outputs side by side for comparison.
    # Create a DataFrame with a MultiIndex for columns where the first level is the file path.
    comparison_table = pd.concat(results, axis=1)
    display(comparison_table)
