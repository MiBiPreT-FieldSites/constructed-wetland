import os
import matplotlib.pyplot as plt
import seaborn as sns

def plot_single_compound_at_well(df, compound, well, y="C_rel", x="tau", log_y=False, save=False, output_dir="plots"):
    """Plot BTC for a single compound at a single well."""
    df_comp = df[(df["compound"] == compound) & (df["Well"] == well)]

    if df_comp.empty:
        print(f"⚠️ No data found for {compound} at {well}")
        return

    title = f"{compound} at {well}"
    filename = f"{compound}_{well}_{y}_vs_{x}.png"

    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df_comp, x=x, y=y, marker="o")
    plt.title(f"BTC: {title} ({y} vs {x})")
    plt.xlabel("Elapsed Time (days)" if x == "days" else "Pore Volumes (τ)")
    plt.ylabel("Relative Concentration (C/C₀)" if y == "C_rel" else "Concentration")
    if log_y:
        plt.yscale("log")
    plt.grid(True)
    plt.tight_layout()

    if save:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300)
        print(f"✅ Saved plot to {filepath}")
        plt.close()
    else:
        plt.show()


def plot_multiple_compounds_at_well(df, compounds, well, y="C_rel", x="tau", log_y=False, save=False, output_dir="plots"):
    """Plot BTCs for multiple compounds at a single well on one plot."""
    df_multi = df[(df["compound"].isin(compounds)) & (df["Well"] == well)]

    if df_multi.empty:
        print(f"⚠️ No data found for {compounds} at {well}")
        return

    title = f"{', '.join(compounds)} at {well}"
    filename = f"{'_'.join(compounds)}_{well}_{y}_vs_{x}.png"

    plt.figure(figsize=(9, 6))
    sns.lineplot(data=df_multi, x=x, y=y, hue="compound", marker="o")
    plt.title(f"BTCs at {well} ({y} vs {x})")
    plt.xlabel("Elapsed Time (days)" if x == "days" else "Pore Volumes (τ)")
    plt.ylabel("Relative Concentration (C/C₀)" if y == "C_rel" else "Concentration")
    if log_y:
        plt.yscale("log")
    plt.grid(True)
    plt.legend(title="Compound")
    plt.tight_layout()

    if save:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300)
        print(f"✅ Saved multi-compound plot to {filepath}")
        plt.close()
    else:
        plt.show()


def plot_all_compounds_all_wells(df, y="C_rel", x="tau", output_dir="plots/by_compound_and_well"):
    """Loop through all compounds and wells to save BTC plots."""
    compounds = df["compound"].unique()
    wells = df["Well"].unique()

    for compound in compounds:
        for well in wells:
            plot_single_compound_at_well(
                df,
                compound=compound,
                well=well,
                y=y,
                x=x,
                save=True,
                output_dir=output_dir
            )


def plot_wetlands_side_by_side(df, compound, y="C_rel", x="tau", save=False, output_dir="plots/comparisons"):
    """Compare BTCs for CW1_EFF, CW2_EFF, CW3_EFF for a given compound in one figure."""
    eff_wells = ["CW1_EFF", "CW2_EFF", "CW3_EFF"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for i, well in enumerate(eff_wells):
        df_plot = df[(df["compound"] == compound) & (df["Well"] == well)]
        if df_plot.empty:
            axes[i].text(0.5, 0.5, f"No data\n{well}", ha='center', va='center')
            axes[i].set_title(well)
            continue

        sns.lineplot(data=df_plot, x=x, y=y, marker="o", ax=axes[i])
        axes[i].set_title(f"{compound} at {well}")
        axes[i].set_xlabel("Days" if x == "days" else "Pore Volumes (τ)")
        if i == 0:
            axes[i].set_ylabel("C/C₀" if y == "C_rel" else "Concentration")
        axes[i].grid(True)

    plt.tight_layout()
    if save:
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{compound}_CW_comparison_{y}_vs_{x}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300)
        print(f"✅ Saved side-by-side plot: {filepath}")
        plt.close()
    else:
        plt.show()

import os
import matplotlib.pyplot as plt
import seaborn as sns

def plot_measured_vs_ade(df, compound, well, y="C_rel", ade_column="ADE_adsorption_only", x="tau", log_y=False, save=False, output_dir="plots/ade_vs_measured"):
    """Plot measured vs ADE-predicted BTC for a compound at a single well."""
    df_plot = df[(df["compound"] == compound) & (df["Well"] == well)]

    if df_plot.empty:
        print(f"⚠️ No data for {compound} at {well}")
        return

    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df_plot, x=x, y=y, label="Measured", marker="o")
    sns.lineplot(data=df_plot, x=x, y=ade_column, label="ADE (adsorption)", linestyle="--")

    plt.title(f"{compound} at {well} ({y} vs {x})")
    plt.xlabel("Elapsed Time (days)" if x == "days" else "Pore Volumes (τ)")
    plt.ylabel("Relative Concentration (C/C₀)" if y == "C_rel" else "Concentration")
    if log_y:
        plt.yscale("log")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save:
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{compound}_{well}_ADE_vs_measured_{y}_vs_{x}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300)
        print(f"✅ Saved measured vs ADE plot: {filepath}")
        plt.close()
    else:
        plt.show()



def plot_ade_solution_side_by_side(df, y="C_rel", x="tau", ade_column="ADE_adsorption_only", output_dir="plots/ade_comparison", save=False):
    """Plot ADE solution for each compound at CW1_EFF, CW2_EFF, CW3_EFF side-by-side."""
    eff_wells = ["CW1_EFF", "CW2_EFF", "CW3_EFF"]
    compounds = df["compound"].unique()

    for compound in compounds:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

        for i, well in enumerate(eff_wells):
            df_plot = df[(df["compound"] == compound) & (df["Well"] == well)]
            if df_plot.empty:
                axes[i].text(0.5, 0.5, f"No data\n{well}", ha='center', va='center')
                axes[i].set_title(well)
                continue

            sns.lineplot(data=df_plot, x=x, y=ade_column, ax=axes[i], label="ADE", linestyle="--")
            sns.lineplot(data=df_plot, x=x, y=y, ax=axes[i], label="Measured", marker="o")
            axes[i].set_title(f"{compound} at {well}")
            axes[i].set_xlabel("Days" if x == "days" else "Pore Volumes (τ)")
            if i == 0:
                axes[i].set_ylabel("C/C₀" if y == "C_rel" else "Concentration")
            axes[i].grid(True)

        plt.tight_layout()
        if save:
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{compound}_ADE_comparison_{y}_vs_{x}.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300)
            print(f"✅ Saved ADE side-by-side plot: {filepath}")
            plt.close()
        else:
            plt.show()

