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
# Contaminants to be plotted

compounds = ["benzeen", "tolueen", "ethylbenzeen", "xylenen (0.7 factor)", "totaal BTEX (0.7 factor)"]

# Rename the contaminants to be plotted (optional), put them in the same order as above.
rename = ["Benzene", "Toluene", "Ethylbenzene", "Xylenes", "Total BTEX"]

# Locations to plot, using the names of location_dictionary.
colors = ["#5c0000", "#89003d", "#f0ab70", "#ffd220", "#66a697", "#004D8A"]
plots = ["CW1_shallow", "CW2_shallow", "CW3_shallow"]
titles = ["CW1", "CW2", "CW3"]
# Relative file path to the excel file with the data
time_points = [0,1,2,3]

normalize = True
compensate_dilution = True
ylimit = (-0.1, 3)

#%% 
k = 0
fig, axs = plt.subplots(4,3, figsize = (20,19), layout ="constrained")

for i, time_point in enumerate(time_points):
    file_path = f"../../../data/raw/CW_field_meassurements/Raw_data_lab/240120_Resultaten_ronde_T{time_point}.xlsx"
    df = tools.cleanup_compound(file_path)
   
    include_xtick = False
    title = False
    if i == 0: 
        title = True
    elif i == 3:
        include_xtick = True
    
    for j, location in enumerate(plots):
        
        include_ytick = False
        
        if j == 0:
            include_ytick = True
            
        ax = axs.flat[k]
        locations = loc[location]
        
        tools.plot_compound_combi(df, locations, compounds, ax,
                                  rename = rename,
                                  normalize = normalize,
                                  compensate_dilution = compensate_dilution,
                                  color = colors[:len(compounds)],
                                  linestyle='--',
                                  marker='o',
                                  markersize = 12,
                                  lw = 5
                                  )
        
        ax.set_ylim(ylimit)
        ax.get_legend().remove()
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.tick_params(length = 6, width = 3, labelsize = 10)
        if include_xtick:
            ax.tick_params(axis="x", labelrotation = -45)
        else:
            ax.set_xticklabels([])
            ax.tick_params(axis="x", direction = "in")
        
        if include_ytick:
            ax.set_ylabel(f"t = {time_point}", fontsize = 25)
        else:
            ax.set_yticklabels([])
            ax.tick_params(axis="y", direction = "in")
        
        if title:
            ax.set_title(titles[j], fontsize = 25)
        
        
        k += 1
        

lines_labels = [ax.get_legend_handles_labels()]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, 
           loc = "lower center",
           bbox_to_anchor = (0.5,-0.001),
           fontsize = 15,
           ncol = 5,
           columnspacing = 0.75,
           frameon = False)

fig.supxlabel(r"Measurement locations", fontsize = 15)
fig.supylabel(r"Relative concentration [$C/C_{0}$]", fontsize = 35)
#fig.supylabel(r"Concentration [$g/m^3$]", fontsize = 25)    

plt.show()

