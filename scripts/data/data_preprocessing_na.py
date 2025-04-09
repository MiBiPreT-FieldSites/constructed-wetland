
import pandas as pd

def extract_contaminants(file_path, contaminants_of_interest, time_point, convert_to_int=False, columns_to_int=None):
    """
    Reads a standardized Excel file where:
      - Row 0 is used as column headers (e.g., "Well name", "benzene", "toluene", etc.).
      - Row 1 holds the 'unit' information for each contaminant column.
      - Subsequent rows hold the actual measurement data.
      
    The function:
      1. Leaves "Well name" as a normal column (i.e., does not set it as the DataFrame's index).
      2. Selects the "Well name" column plus only those columns (possibly duplicated) matching
         or starting with each contaminant in `contaminants_of_interest`.
      3. Inserts a new "Coding" column as the *first* column. For row 0:
         - The "Well name" cell is forced to "-",
         - The "Coding" cell is forced to "unit".
         For subsequent rows, the "Coding" cell is generated as:
             "NL_CW_W_{counter:02d}" if time_point == "0"
             "NL_CW_W_{time_point}{counter:02d}" otherwise.
         The counter starts at 1 for row 1, so row 1 => "NL_CW_W_01", row 2 => "NL_CW_W_02", etc.
      4. Converts numeric columns (except row 0) to integers.
      
    Parameters:
      file_path (str): Path to the Excel file.
      contaminants_of_interest (list): List of contaminant names (headers) to extract 
                                       (duplicates are handled by checking if col.startswith(cont + ".") or col == cont).
      time_point (str): The sampling time point, used in the code generation (e.g., "0").
      convert_to_int (bool, optional): If True, attempts to convert the specified columns to integers.
      columns_to_int (list, optional): Column names (exact matches) to convert to int.
      
    Returns:
      pd.DataFrame: Processed DataFrame with:
        - A "Coding" column inserted at the left.
        - The original "Well name" column plus the requested contaminant columns.
        - Row 0 has "Well name" = "-" and "Coding" = "unit".
        - Row 1+ have "Coding" = generated codes.
        - Numeric columns (except row 0) optionally converted to integers.
    """
    
    # 1) Read the file with the first row as headers
    df = pd.read_excel(file_path) 

    # 2) Identify the "Well name" column and find the selected contaminants
    well_name_column = df.columns[0]
    selected_contaminant_cols = []
    for col in df.columns[1:]:  # skip the first column, i.e. "Well name"
        for cont in contaminants_of_interest:
            if col == cont or col.startswith(cont + "."):
                selected_contaminant_cols.append(col)
                break

    # Create a new DataFrame with "Well name" as the first column + the selected contaminants
    new_df = df[[well_name_column] + selected_contaminant_cols].copy()

    # 3) Insert a new "Coding" column as the first column
    coding_values = []
    counter = 1
    for i in range(len(new_df)):
        if i == 0:
            # Row 0 => "Well name" is forced to "-", "Coding" = "unit"
            new_df.loc[new_df.index[i], well_name_column] = "-"
            coding_values.append("unit")
        else:
            # For measurement rows, generate a code
            if time_point.strip() == "0":
                code = f"NL_CW_W_{counter:02d}"
            else:
                code = f"NL_CW_W_{time_point}{counter:02d}"
            coding_values.append(code)
            counter += 1

    coding_series = pd.Series(coding_values, index=new_df.index, name="Coding")
    new_df.insert(0, "Coding", coding_series)

    # 4) Convert specified columns to integers, skipping row 0 (the 'unit' row).
    
    if convert_to_int and columns_to_int is not None:
        measurement_rows = new_df.index[1:]  # skip row 0
        for col in columns_to_int:
            if col in new_df.columns:
                new_df.loc[measurement_rows, col] = (
                    pd.to_numeric(new_df.loc[measurement_rows, col], errors='coerce')
                    .fillna(0)
                    .astype(int)
                )
    
    return new_df


if __name__ == "__main__":
    time_point = "3"
    file_path = f"../../data/cleaned/cw_T{time_point}_cleaned.xlsx"
    
    # Contaminants list
    contaminants_of_interest = [
        "benzene", "toluene", "ethylbenzene", "o-xylene", "(m+p)-xylene", 
        "total BTEX (factor 0.7)", "sum xylenes (factor 0.7)", "naphthalene", 
        "chloride", "nitrite", "nitrite - N", "nitrate", "nitrate - N",
        "sulphates", "Oxygen", "Iron II", "MN II"
    ]
    
    # Columns to convert to integers
    columns_to_convert = [
        "benzene", "toluene", "ethylbenzene", "o-xylene", "(m+p)-xylene",
        "total BTEX (factor 0.7)", "sum xylenes (factor 0.7)", "naphthalene.1"
    ]
    
    selected_data = extract_contaminants(
        file_path,
        contaminants_of_interest,
        time_point,
        convert_to_int=True,
        columns_to_int=columns_to_convert
    )
    
    print(selected_data)
    
    output_file = f"../../data/preprocessed/na_screening/cw_T{time_point}_preprocessed.xlsx"
    # Save without index to see columns "Coding", "Well name", and contaminants
    selected_data.to_excel(output_file, index=False)
    print(f"Cleaned data has been saved to '{output_file}'.")

