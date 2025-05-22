from site_params import SiteParameters
from compound_props import CompoundProperties
from data_processor import DataProcessor
from btc_builder import BTCDataFrameBuilder
import config


def main():
    # 1. Create SiteParameters instance (includes foc)
    site = SiteParameters(
        bulk_density=config.BULK_DENSITY,
        porosity=config.POROSITY,
        flow_rate=config.FLOW_RATE,
        bulk_volume=config.BULK_VOLUME,
        foc=config.FOC,
        pore_volume=config.PORE_VOLUME
    )

    # 2. Create CompoundProperties for each compound
    compounds = {
        name: CompoundProperties(**props)
        for name, props in config.COMPOUND_INFO.items()
    }

    # 3. Load all data rounds
    dp = DataProcessor()
    rounds = [dp.load_round(path, date) for path, date in config.FILE_PATHS]

    # 4. Build the BTC DataFrame
    builder = BTCDataFrameBuilder(rounds, site, list(compounds.keys()))
    btc_df = builder.build()

    # 4.5 Add Kd and R
    btc_df["Kd"] = btc_df["compound"].map(
    lambda c: compounds[c].compute_Kd(site)
    )

    btc_df["R"] = btc_df["compound"].map(
        lambda c: compounds[c].retardation(site)
    )


    print("\nBTC DataFrame (from main.py):")
    print(btc_df.head())
    print("Rows:", len(btc_df))
    print("Columns:", btc_df.columns.tolist())

    # 5. Add ADE solution (adsorption only)
    from ade_solution import ADESolution  # adjust the path if needed

    # Initialize with site-specific transport parameters
    ade = ADESolution(
        dispersion_length=0.1,      # α in meters
        velocity=0.58,               # v in m/day
        transport_distance=20      # L in meters
    )

    # Add the erfc-based analytical solution to the BTC DataFrame
    btc_df = ade.add_to_dataframe(btc_df)

    # 6. Preview
    print("\nBreakthrough Curve DataFrame (first 5 rows):")
    print(btc_df.head())

    # 7. Save full BTC DataFrame to Excel
    btc_df.to_excel("btc_full_output.xlsx", index=False)
    print(" BTC DataFrame saved to 'btc_full_output.xlsx'")

    # Optional: return btc_df for further plotting or saving
    return btc_df


if __name__ == "__main__":
    df = main()

