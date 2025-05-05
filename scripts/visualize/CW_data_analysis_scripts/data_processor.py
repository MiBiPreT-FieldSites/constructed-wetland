import pandas as pd

class DataProcessor:
    """Load cleaned Excel files and tag them with sampling date."""

    def load_round(self, file_path, date_str):
        """
        Reads a cleaned Excel file and adds a 'date' column.

        Parameters:
        - file_path: str, path to cleaned Excel file
        - date_str: str, e.g., "2024-08-15"

        Returns:
        - pd.DataFrame with columns: Well, [compound names], date
        """
        df = pd.read_excel(file_path, index_col=0)
        df = df.reset_index().rename(columns={"index": "Well"})
        df["date"] = pd.to_datetime(date_str)
        return df

