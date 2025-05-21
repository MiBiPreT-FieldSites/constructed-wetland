import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the result file 
time_point = "4"
na_result = pd.read_excel(f"../../results/na_screening_result_T{time_point}.xlsx")  

# Define sampling locations per wetland and depth 
sampling_groups = {
    "CW1": {
        "deep": ["INF", "CW1MF02", "CW1MF06", "CW1MF10", "CW1_EFF"],
        "shallow": ["INF", "CW1MF01", "CW1MF05", "CW1MF09", "CW1_EFF"]
    },
    "CW2": {
        "deep": ["INF", "CW2MF02", "CW2MF06", "CW2MF10", "CW2_EFF"],
        "shallow": ["INF", "CW2MF01", "CW2MF05", "CW2MF09", "CW2_EFF"]
    },
    "CW3": {
        "deep": ["INF", "CW3MF02", "CW3MF06", "CW3MF10", "CW3_EFF"],
        "shallow": ["INF", "CW3MF01", "CW3MF05", "CW3MF09", "CW3_EFF"]
    }
}

# Color mapping 
color_map = {"green": "#2ecc71", "yellow": "#f1c40f", "red": "#e74c3c"}

# Path to the existing output folder 
output_folder = f"../../results/na_traffic_plots/round_T{time_point}"  

# Generate and save plots
for cw, depths in sampling_groups.items():
    for depth, locations in depths.items():
        subset = na_result[na_result["obs_well"].isin(locations)].copy()
        subset["Location"] = pd.Categorical(subset["obs_well"], categories=locations, ordered=True)
        subset = subset.sort_values("Location")
        subset["Color"] = subset["na_traffic_light"].map(color_map)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(subset["Location"], [1] * len(subset), color=subset["Color"], edgecolor='black')

        ax.set_title(f"NA Traffic Light-T{time_point} - {cw} - {depth.capitalize()} Samples")
        ax.set_ylim(0, 1.5)
        ax.set_ylabel("NA Status (Traffic Light)")
        ax.set_xlabel("Sampling Location")
        ax.set_xticks(range(len(subset)))
        ax.set_xticklabels(subset["Location"], rotation=45, ha='right')
        ax.set_yticks([])

        plt.tight_layout()

        # Save to existing folder
        filename = f"{cw}_{depth}_traffic_light.png"
        filepath = os.path.join(output_folder, filename)
        plt.savefig(filepath, dpi=300)
        plt.close()


