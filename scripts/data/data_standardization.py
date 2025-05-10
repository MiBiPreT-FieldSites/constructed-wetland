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

    # Define a dictionary mapping Dutch to English.
    translation_dict = {
        "Analysis": "Analysis",
        "Projectcode": "Project code",
        "Projectnaam": "Project name",
        "Monsteromschrijving": "Sample description",
        "Rapport status":	"Report status",
        "Validatie status":	"Validation status",
        "Rapport Datum":	"Report Date",
        "Start Datum":	"Start Date",
        "DOC":	"DOC",
        "TOC":	"TOC",
        "METALEN":	"METALS",
        "Ijzer (2+)":	"Iron II",
        "Mangaan (II)":	"MN II",
        "ANORGANISCHE VERBINDINGEN":	"INORGANIC COMPOUNDS",
        "cyanide (totaal)":	"cyanid",
        "fosfor (totaal)":	"phosphor",
        "VLUCHTIGE AROMATEN":	"VOLATILE AROMATICS",
        "benzeen":	"benzene",
        "tolueen":	"toluene",
        "ethylbenzeen":	"ethylbenzene",
        "o-xyleen":	"o-xylene",
        "p- en m-xyleen": "(m+p)-xylene",
        "xylenen (0.7 factor)":	"sum xylenes (factor 0.7)",
        "totaal BTEX (0.7 factor)":	"total BTEX (factor 0.7)",
        "naftaleen":	"naphthalene",
        "FENOLEN":	"PHENOLS",
        "fenol":	"phenol",
        "m-cresol":	"m-cresol",
        "o-cresol":	"o-cresol",
        "p-cresol":	"p-cresol",
        "som cresolen":	"som cresols",
        "2-ethylfenol":	"2-ethylphenol",
        "3-ethylfenol":	"3-ethylphenol",
        "2,4-dimethylfenol":	"2,4-dimethylphenol",
        "2,5-dimethylfenol":	"2,5-dimethylphenol",
        "3,5+2,3-dimethylfenol+4-ethylfenol":	"3,5+2,3-dimethylphenol+4-ethylphenol",
        "2,6-dimethylfenol":	"2,6-dimethylphenol",
        "3,4-dimethylfenol":	"3,4-dimethylphenol",
        "som C2-alkylfenolen":	"som C2-alkylphenolen",
        "2,3,5-trimethylfenol":	"2,3,5-trimethylphenol",
        "3,4,5-trimethylfenol":	"3,4,5-trimethylphenol",
        "2-isopropylfenol":	"2-isopropylphenol",
        "som C3-alkylfenolen":	"som C3-alkylphenolen",
        "thymol":	"thymol",
        "p-(tert)butylfenol":	"p-(tert)butylphenol",
        "som C4-alkylfenolen":	"som C4-alkylphenolen",
        "POLYCYCLISCHE AROMATISCHE KOOLWATERSTOFFEN":	"POLYCYCLIC AROMATIC HYDROCARBONS",
        "naftaleen":	"naphthalene",
        "acenaftyleen":	"acenaphthylene",
        "acenafteen":	"acenaphtene",
        "fluoreen":	"fluorene",
        "fenantreen":	"phenanthrene",
        "antraceen":	"anthracene",
        "fluoranteen":	"fluoranthene",
        "pyreen":	"pyrene",
        "benzo(a)antracee":	"benzo(a)anthracene",
        "chryseen":	"chrysene",
        "benzo(b)fluoranteen":	"benzo(b)fluoranthene",
        "benzo(k)fluoranteen":	"benzo(k)fluoranthene",
        "benzo(a)pyreen":	"benzo(a)pyrene",
        "dibenz(a,h)antraceen":	"dibenz(a,h)anthracene",
        "benzo(ghi)peryleen":	"benzo(g,h,i)perylene",
        "indeno(1,2,3-cd)pyreen":	"indeno(1,2,3-cd)pyrene",
        "pak-totaal (16 van EPA)":	"sum PAH (16 EPA)",
        "pak-totaal (10 van VROM) (0.7 factor)":	"sum PAH (VROM) (factor 0.7)",
        "MINERALE OLIE":	"MINERAL OIL",
        "fractie C10-C12":	"fraction C10-C12",
        "fractie C12-C22":	"fraction C12-C22",
        "fractie C22-C30":	"fraction C22-C30",
        "fractie C30-C40":	"fraction C30-C40",
        "totaal olie C10 - C40":	"total oil C10 - C40",
        "DIVERSE NATCHEMISCHE BEPALINGEN":	"VARIOUS NAT CHEMICAL DETERMINATIONS",
        "chloride":	"chloride",
        "nitriet":	"nitrite",
        "nitriet-N":	"nitrite - N",
        "nitraat":	"nitrate",
        "nitraat-N":	"nitrate - N",
        "sulfaat":	"sulphates",
        "Zuurstof": "Oxygen"
    }

    # Translate the index using the dictionary.
    dataframe.index = dataframe.index.map(lambda x: translation_dict.get(x, x))

    print("\nDataFrame after translating the index:")
    print(dataframe)

    # Turn the index into a regular column with the header "Well name"
    dataframe_reset = dataframe.reset_index()
   
    # Mentioned rows and rows without any data are not needed and thus removed
    drop_rows = ["Analysis", "Project code", "Project name", "Report status", "Validation status", "Report Date", "Start Date"]
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

    dataframe_reset_sorted["Well name"] = dataframe_reset_sorted["Well name"].replace(translation_dict)
 # Compounds under the detection limit have been entered as <*detection limit*.
    # These values are set to 0. 
    dataframe_reset_sorted = dataframe_reset_sorted.map(lambda x: 0 if isinstance(x, str) and x.startswith('<') else x)

    # For analysis, the entries of the dataframe should be seen as floats.
    excluded_cols = ["Well name", "unit"]

    # Create a boolean mask based on the 'Header' column.
    # This mask is True for rows where the Header is NOT "Zuurstof" or "Monsteromschrijving"
    mask = ~dataframe_reset_sorted["Well name"].isin(["Oxygen", "Sample description"])

    for col in dataframe_reset_sorted.columns:
        if col not in excluded_cols:
            # Apply the cleaning operations only for rows matching the mask
            dataframe_reset_sorted.loc[mask, col] = dataframe_reset_sorted.loc[mask, col].str.strip()
            dataframe_reset_sorted.loc[mask, col] = pd.to_numeric(dataframe_reset_sorted.loc[mask, col], errors='coerce')
    dataframe_reset_sorted = dataframe_reset_sorted.fillna(0.0)
    
    # After cleaning, update the "unit" column for the row where "Well name" is "Monsteromschrijving"
    dataframe_reset_sorted.loc[dataframe_reset_sorted["Well name"] == "Sample description", "unit"] = "-"
    
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
