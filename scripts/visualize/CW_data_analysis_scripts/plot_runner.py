from main import main  # Builds the BTC DataFrame

from btc_plotting import (
    plot_single_compound_at_well,
    plot_multiple_compounds_at_well,
    plot_all_compounds_all_wells,
    plot_wetlands_side_by_side,
    plot_ade_solution_side_by_side,
    plot_measured_vs_ade
)

# === Load BTC DataFrame ===
btc_df = main()

# === Example 1: Plot single compound at specific well ===
# plot_single_compound_at_well(
#     df=btc_df,
#     compound="benzene",
#     well="CW1_EFF",
#     y="C_rel",
#     x="tau",
#     log_y=False,
#     save=False
# )

# === Example 2: Plot multiple compounds at one well ===
# plot_multiple_compounds_at_well(
#     df=btc_df,
#     compounds=["benzene", "naphthalene"],
#     well="CW3_EFF",
#     y="C_rel",
#     x="tau",
#     save=False
# )

# === Example 3: Save BTC plots for all compounds and wells ===
# plot_all_compounds_all_wells(
#     df=btc_df,
#     y="C_rel",
#     x="tau",
#     output_dir="plots/by_compound_and_well"
# )

# === Example 4: Side-by-side plot for one compound across 3 wetlands ===
# plot_wetlands_side_by_side(
#     df=btc_df,
#     compound="toluene",
#     y="C_rel",
#     x="tau",
#     save=True,
#     output_dir="plots/comparisons"
# )

# === Example 5: ADE vs Measured side-by-side for all wells ===
# plot_ade_solution_side_by_side(
#     df=btc_df,
#     y="C_rel",
#     x="days",
#     ade_column="ADE_adsorption_only",
#     save=True,
#     output_dir="plots/ade_comparison"
# )

# === Example 6: Measured vs ADE for one compound at one well ===
plot_measured_vs_ade(
    df=btc_df,
    compound="naphthalene",
    well="CW1_EFF",
    y="C_rel",
    x="tau",
    ade_column="ADE_adsorption_only",
    save=False  # Change to True to save
)

