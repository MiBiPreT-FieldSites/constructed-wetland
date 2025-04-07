#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 08:15:48 2024

@author: jorrit
"""
 
import tools as tools
from tools import location_dictionary as loc
import numpy as np
import matplotlib.pyplot as plt

#%%
# Relative file path to the excel file with the data
time_point = "3"
file_path = f"../CW_field_measurements/240120_Resultaten_ronde_T={time_point}.xlsx"
df = tools.cleanup_compound(file_path)

#%%
# Contaminants to be plotted
#plot_compounds = ["chloride"]
#plot_compounds = ["benzeen", "tolueen", "ethylbenzeen", "xylenen (0.7 factor)", "totaal BTEX (0.7 factor)"]
plot_compounds = ["Ijzer (2+)"]
#plot_compounds = ["Zuurstof"]
#plot_compounds = ["Ijzer (2+)","Mangaan (II)", "sulfaat"]
# Rename the contaminants to be plotted (optional), put them in the same order as above.
#rename_compounds = ["benzene", "toluene", "ethylbenzene", "xylenes", "total BTEX"]
#rename_compounds = ["iron (II)", "manganese (II)", "sulfate"]
rename_compounds = ["oxygen"]
# Locations to plot, using the names of location_dictionary.
colors = ["#5c0000", "#89003d", "#f0ab70", "#ffd220", "#66a697", "#004D8A"]
plots = ["CW1_ondiep", "CW2_ondiep", "CW3_ondiep"]
subplots = ["a", "b", "c"]

for i, location in enumerate(plots):
    plot_location = loc[location]
    ax = tools.plot_compound(df, plot_location, plot_compounds, 
                             rename = rename_compounds,
                             normalize = False, 
                             plot_type="line",
                             ylimit = False,
                             figsize = (6,5),
                             color = colors[:len(plot_compounds)],
                             linestyle='--',
                             marker='o',
                             )
    #plt.title(f"Concentration in {location}, t = {time_point}")
    plt.title(subplots[i], loc="left")

# Display all plots
plt.show()

#["#5c0000", "#89003d", "#f0ab70", "#ffd220", "#66a697", "#789ddf"]
