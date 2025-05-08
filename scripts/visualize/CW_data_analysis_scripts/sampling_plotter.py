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
time_point = 3
dates = ["Aug 2024", "Oct 2024", "Dec 2024", "Feb 2025"]

time_point_date = dates[time_point]

file_path = f"../../../data/raw/CW_field_meassurements/Raw_data_lab/240120_Resultaten_ronde_T{time_point}.xlsx"
df = tools.cleanup_compound(file_path)

#%%
# Contaminants to be plotted
#plot_compounds = ["chloride"]
plot_compounds = ["benzeen", "tolueen", "ethylbenzeen", "xylenen (0.7 factor)", "totaal BTEX (0.7 factor)"]
#plot_compounds = ["Ijzer (2+)"]
#plot_compounds = ["Zuurstof"]
#plot_compounds = ["Zuurstof", "nitraat", "sulfaat"]
#plot_compounds = ["sulfide (vrij)", "Mangaan (II)", "Ijzer (2+)"]
#plot_compounds = ["naftaleen", "acenaftyleen", "acenafteen", "fluoreen", "fenantreen", "antraceen"]
# Rename the contaminants to be plotted (optional), put them in the same order as above.
rename_compounds = ["benzene", "toluene", "ethylbenzene", "xylenes", "total BTEX"]
#rename_compounds = ["sulfide (free)", "manganese (II)", "iron (II)"]
#rename_compounds = ["oxygen"]
#rename_compounds = ["Oxygen", "Nitrate", "Solphate"]
#rename_compounds = ["Naphtalene", "Acenaphthylene", "Acenaphtene", "Fluorene", "Fenantrene", "Anthracene"]
# Locations to plot, using the names of location_dictionary.
colors = ["#5c0000", "#89003d", "#f0ab70", "#ffd220", "#66a697", "#004D8A"]
plots = ["CW1_shallow", "CW2_shallow", "CW3_shallow"]
subplots = ["a", "b", "c"]

for i, location in enumerate(plots):
    plot_location = loc[location]
    ax = tools.plot_compound(df, plot_location, plot_compounds, 
                             rename = rename_compounds,
                             normalize = False, 
                             compensate_dilution = True,
                             plot_type="line",
                             ylimit = False,
                             figsize = (6,5),
                             color = colors[:len(plot_compounds)],
                             linestyle='--',
                             marker='o',
                             )                         
    plt.title(f"Concentration in {location}, t={time_point}:{time_point_date}")
    #plt.title(subplots[i], loc="left")

# Display all plots
plt.show()

#["#5c0000", "#89003d", "#f0ab70", "#ffd220", "#66a697", "#789ddf"]
