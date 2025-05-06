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
        # 1. Combine all rounds
        df = pd.concat(self.data_frames, ignore_index=True)

        # 2. Reshape to long format
        df_long = df.melt(
            id_vars=["date", "Well"],
            value_vars=self.compounds,
            var_name="compound",
            value_name="concentration"
        )

        # 3. Calculate elapsed days since first date
        t0 = df_long["date"].min()
        df_long["days"] = (df_long["date"] - t0).dt.days

        # 4. Calculate pore volume coordinate τ = Q × t / Vp
        Q = self.site_params.flow_rate
        Vp = self.site_params.pore_volume
        df_long["tau"] = Q * df_long["days"] / Vp

        # 5. Calculate relative concentration C/C0 using 'INF' well
        df_long["C0"] = df_long.groupby(["date", "compound"])["concentration"] \
                               .transform(lambda x: x[df_long["Well"] == "INF"].iloc[0])
        df_long["C_rel"] = df_long["concentration"] / df_long["C0"]

        return df_long