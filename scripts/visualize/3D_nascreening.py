import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os


# Folder containing Excel files for each time point
data_folder = "../../results"  
output_folder = "../../results/na_traffic_3D_plots" 

time_points = ["T0", "T1", "T2", "T3"]
file_template = "na_screening_result_{}.xlsx"  

# Sampling location groups
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

color_map = {"green": "#2ecc71", "yellow": "#f1c40f", "red": "#e74c3c"}

# LOAD AND COMBINE DATA 
combined_data = []

for t in time_points:
    file_path = os.path.join(data_folder, file_template.format(t))
    df = pd.read_excel(file_path)
    df["Time"] = t
    combined_data.append(df)

full_data = pd.concat(combined_data, ignore_index=True)

# GENERATE 3D PLOTS 
for cw, groups in sampling_groups.items():
    for depth, locations in groups.items():
        plot_df = full_data[full_data["obs_well"].isin(locations)].copy()
        plot_df["Color"] = plot_df["na_traffic_light"].map(color_map)

        loc_mapping = {loc: i for i, loc in enumerate(locations)}
        time_mapping = {tp: i for i, tp in enumerate(time_points)}

        plot_df["X"] = plot_df["obs_well"].map(loc_mapping)
        plot_df["Y"] = plot_df["Time"].map(time_mapping)
        plot_df["Z"] = 0
        plot_df["Height"] = 1  # fixed height for visual status

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        for _, row in plot_df.iterrows():
            ax.bar3d(
                x=row["X"], y=row["Y"], z=row["Z"],
                dx=0.5, dy=0.5, dz=row["Height"],
                color=row["Color"], edgecolor='black'
            )

        ax.set_xticks(range(len(locations)))
        ax.set_xticklabels(locations)
        ax.set_yticks(range(len(time_points)))
        ax.set_yticklabels(time_points)
        ax.set_zlim(0, 1.5)

        ax.set_xlabel("Sampling Location")
        ax.set_ylabel("Time Point")
        ax.set_zlabel("NA Status (Traffic Light)")
        ax.set_title(f"3D NA Traffic Plot - {cw} - {depth.capitalize()}")

        plt.tight_layout()
        

        #  Save figure 
        filename = f"{cw}_{depth}_3D_NA_traffic.png"
        save_path = os.path.join(output_folder, filename)
        plt.savefig(save_path, dpi=300)
        plt.close()  # Close figure to avoid display in loop
