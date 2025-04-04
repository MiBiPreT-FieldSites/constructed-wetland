import pandas as pd

def cleanup_compound(file_path):
    """ Takes an excel sheet of default format of Constructed Wetland monitoring
    and changes it into a dataframe that can be plotted.

    Parameters
    ----------
    file_path : str
        Path to excel sheet containing sampling data.

    Returns
    -------
    dataframe : pd.DataFrame
        A cleaned up dataframe containing the data from the input Excel sheet.

    """
   
    dataframe = pd.read_excel(file_path, skiprows=1, sheet_name = "Analyseresultaten", index_col=[0], decimal = ",")
    
    # Assign name for the index column
    dataframe.index.name = "Well name"
    
    # Extract the row with the index label "Monsteromschrijving" and convert it into a list
    monster_names = dataframe.loc["Monsteromschrijving"].tolist()
    
    # Change the first element of this list to "unit"
    monster_names[0] = "unit"
    #print(monster_names)

    # Update the dataFrame’s columns to the new names stored in monster_names
    dataframe.columns = monster_names

    # Turn the index into a regular column with the header "Well name"
    dataframe_reset = dataframe.reset_index()
   
    # Mentioned rows and rows without any data are not needed and thus removed
    drop_rows = ["Analysis", "Projectcode", "Projectnaam", "Rapport status", "Validatie status", "Rapport Datum", "Start Datum"]
    dataframe_reset_filtered = dataframe_reset[~dataframe_reset["Well name"].isin(drop_rows)]
    dataframe_reset_filtered = dataframe_reset_filtered.dropna(axis = "index", how = "all", subset=dataframe_reset_filtered.columns[1:])

    #print(dataframe_reset_filtered)

    # Couple "Monsternummer" to the standard codes for measurement points and rename columns.
    keyframe = pd.read_excel(file_path, sheet_name = "Watermonstergegevens", decimal = ".")
    rename_dict = pd.Series(keyframe.Meetpunt.values, index = keyframe.Monsternummer).to_dict()
    dataframe_reset_filtered.rename(columns = rename_dict, inplace = True)

    # Dfine desired column order
    desired_order = ["Well name", "unit", "INF", "CW1MF01", "CW1MF02", "CW1MF05", "CW1MF06", "CW1MF09", "CW1MF10", "CW1_EFF", "CW2MF01", "CW2MF02", "CW2MF05", "CW2MF06", "CW2MF09", "CW2MF10", "CW2_EFF", "CW3MF01", "CW3MF02", "CW3MF05", "CW3MF06", "CW3MF09", "CW3MF10", "CW3_EFF"]
    # Reorder the DataFrame column
    dataframe_reset_sorted = dataframe_reset_filtered[desired_order]

    # Oxygen concentrations are located in the second tab, so these are added seperately to the dataframe
    oxygen_data = keyframe.loc[:, ("Meetpunt", "Zuurstof")].T
    oxygen_data.rename(columns = oxygen_data.loc["Meetpunt"], inplace = True)
    oxygen_data.drop("Meetpunt", axis = 0, inplace = True)
    oxygen_data.loc[:,"unit"] = "mg/l"
    oxygen_data.loc[:,"Well name"] = "Zuurstof"
    oxygen_data = oxygen_data[dataframe_reset_sorted.columns]

    dataframe_reset_sorted = pd.concat([dataframe_reset_sorted, oxygen_data])

 # Compounds under the detection limit have been entered as <*detection limit*.
    # These values are set to 0. 
    dataframe_reset_sorted = dataframe_reset_sorted.map(lambda x: 0 if isinstance(x, str) and x.startswith('<') else x)

    # For analysis, the entries of the dataframe should be seen as floats.
    excluded_cols = ["Well name", "unit"]

    # Create a boolean mask based on the 'Header' column.
    # This mask is True for rows where the Header is NOT "Zuurstof" or "Monsteromschrijving"
    mask = ~dataframe_reset_sorted["Well name"].isin(["Zuurstof", "Monsteromschrijving"])

    for col in dataframe_reset_sorted.columns:
        if col not in excluded_cols:
            # Apply the cleaning operations only for rows matching the mask
            dataframe_reset_sorted.loc[mask, col] = dataframe_reset_sorted.loc[mask, col].str.strip()
            dataframe_reset_sorted.loc[mask, col] = pd.to_numeric(dataframe_reset_sorted.loc[mask, col], errors='coerce')
    dataframe_reset_sorted = dataframe_reset_sorted.fillna(0.0)
    
    # After cleaning, update the "unit" column for the row where "Well name" is "Monsteromschrijving"
    dataframe_reset_sorted.loc[dataframe_reset_sorted["Well name"] == "Monsteromschrijving", "unit"] = "-"
    
    dataframe_transposed = dataframe_reset_sorted.transpose()

    return(dataframe_transposed)

if __name__ == "__main__":
     # Relative file path to the excel file with the data
    time_point = "3"
    file_path = f"../../data/raw/CW_field_meassurements/Raw_data_lab/240120_Resultaten_ronde_T{time_point}.xlsx"
    
      #Call the cleanup_compound function to clean up the data
    cleaned_data = cleanup_compound(file_path)

      # Save the cleaned DataFrame to a new Excel file
    output_file = f"../../data/cleaned/cw_T{time_point}_cleaned.xlsx"
    cleaned_data.to_excel(output_file, index=True, header=False)
    print(f"Cleaned data has been saved to '{output_file}'.")
