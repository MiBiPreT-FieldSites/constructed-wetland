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
        foc=config.FOC
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

    # 5. Preview
    print("\nBreakthrough Curve DataFrame (first 5 rows):")
    print(btc_df.head())

    # Optional: return btc_df for further plotting or saving
    return btc_df


if __name__ == "__main__":
    df = main()

