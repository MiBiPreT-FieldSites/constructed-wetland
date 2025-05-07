import pandas as pd

class DataProcessor:
    """Load cleaned Excel sheets and tag them with sampling dates."""

    def load_round(self, file_path, date_str):
        """
        Read a cleaned Excel file into a DataFrame, rename 'Well name' to 'Well',
        and add a `date` column for time tracking.

        Parameters:
        - file_path: str, path to the cleaned Excel file
        - date_str:  str, sampling date in "YYYY-MM-DD" format

        Returns:
        - df: pandas.DataFrame with columns ['Well', <compound columns...>, 'date']
        """
        # Load Excel file with all columns (no index_col)
        df = pd.read_excel(file_path)

        # Rename 'Well name' to 'Well' for consistency
        if "Well name" in df.columns:
            df.rename(columns={"Well name": "Well"}, inplace=True)

        # Add a new column with the sampling date
        df["date"] = pd.to_datetime(date_str)

        return df



# if __name__ == "__main__":
#     dp = DataProcessor()

#     # Update path and date as needed
#     file_path = "../../../data/cleaned/cw_T0_cleaned.xlsx"
#     date = "2024-08-14"

#     df = dp.load_round(file_path, date)

#     print("Preview of the loaded and renamed DataFrame:")
#     print(df.head())
