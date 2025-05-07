import pandas as pd

class BTCDataFrameBuilder:
    """Build a long-format DataFrame for BTC plotting."""

    def __init__(self, data_frames, site_params, compounds):
        """
        Parameters:
        - data_frames: list of pd.DataFrame from each round
        - site_params: SiteParameters instance
        - compounds: list of compound names (str)
        """
        self.data_frames = data_frames
        self.site_params = site_params
        self.compounds = compounds

    def build(self):
        # 1. Combine all sampling rounds into one DataFrame
        df = pd.concat(self.data_frames, ignore_index=True)

        # 2. Reshape to long format (1 row per compound × well × date)
        df_long = df.melt(
            id_vars=["date", "Well"],
            value_vars=self.compounds,
            var_name="compound",
            value_name="concentration"
        )

        # 3. Set fixed start-of-clock date t₀ = 11 June 2024
        t0 = pd.to_datetime("2024-06-11")
        df_long["days"] = (df_long["date"] - t0).dt.days

        # 4. Compute pore volume coordinate τ = Q * t / Vp
        Q = self.site_params.flow_rate
        Vp = self.site_params.pore_volume
        df_long["tau"] = Q * df_long["days"] / Vp

        # 5. Ensure numeric concentration (in case of string values)
        df_long["concentration"] = pd.to_numeric(df_long["concentration"], errors="coerce")

        # 6. Compute influent concentration C₀ for each date + compound
        def get_influent_value(subgroup):
            inflow = subgroup[subgroup["Well"] == "INF"]
            return inflow["concentration"].iloc[0] if not inflow.empty else pd.NA

        df_long["C0"] = df_long.groupby(["date", "compound"])["concentration"] \
            .transform(lambda x: get_influent_value(df_long.loc[x.index]))

        df_long["C0"] = pd.to_numeric(df_long["C0"], errors="coerce")

        # 7. Compute relative concentration
        df_long["C_rel"] = df_long["concentration"] / df_long["C0"]

        print(f"Before dropna: {len(df_long)} rows")

        # Optional: print a few raw values
        print(df_long[["Well", "compound", "concentration", "C0"]].sample(5))


        # 8. Drop any rows with invalid or missing values
        df_long = df_long.dropna(subset=["concentration", "C0", "C_rel"])

    
        # Create synthetic rows for t0 (all wells, all compounds)
        wells = df_long["Well"].unique()
        compounds = df_long["compound"].unique()

        synthetic_rows = []
        for compound in compounds:
            for well in wells:
                synthetic_rows.append({
                    "date": t0,
                    "days": 0,
                    "tau": 0,
                    "Well": well,
                    "compound": compound,
                    "concentration": 0.0,
                    "C0": 1.0,     # arbitrary, avoids division by zero
                    "C_rel": 0.0
                })

        # Add to the dataframe
        df_long = pd.concat([pd.DataFrame(synthetic_rows), df_long], ignore_index=True)

        # Optional: sort for cleaner plots
        #df_long = df_long.sort_values(by=["compound", "Well", "date"])

        # Optional preview
        print("\n✅ Final BTC DataFrame preview:")
        print(df_long.head(10))
        print("Columns:", df_long.columns.tolist())
        print("Total rows:", len(df_long))

        return df_long
