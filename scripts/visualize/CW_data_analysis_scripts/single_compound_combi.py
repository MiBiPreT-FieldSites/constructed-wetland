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

compounds = ["cyanide (totaal)"]

# Rename the contaminants to be plotted (optional), put them in the same order as above.
rename = ["Cyanide"]

# Locations to plot, using the names of location_dictionary.
colors = ["#89003d", "#f0ab70", "#ffd220", "#66a697", "#004D8A"]
plots = ["CW1_shallow", "CW2_shallow", "CW3_shallow"]
titles = ["CW1", "CW2", "CW3"]
# Relative file path to the excel file with the data
time_points = [0,1,2]

normalize = True
compensate_dilution = True
ylimit_list = [(-0.1, 1.2), (-0.1, 30), (-0.1, 1.1)]


df_list = []
for time in time_points:
    file_path = f"./240120_Resultaten_ronde_T={time}.xlsx"
    df_list.append(tools.cleanup_compound(file_path))

#%% 
l = 0
fig, axs = plt.subplots(1,3, figsize = (20,10), layout ="constrained")

compound = compounds

for j, location in enumerate(plots):
    
    include_ytick = False
    
    if j == 0:
        include_ytick = True
        
    ax = axs.flat[l]
    locations = loc[location]
    
    for k, time in enumerate(time_points):
        
        dataframe = df_list[k]
        
        plot_frame = dataframe.drop(columns = "unit", axis=0)
        
        # Influent is the same for each wetland, thus divide by it to normalize data.
        if normalize:
            plot_frame = plot_frame.div(plot_frame["INF"], axis = 0)
        
        if compensate_dilution:
            if not normalize:
                comp_chlor = plot_frame.div(plot_frame["INF"], axis = 0)
                plot_frame = plot_frame.div(comp_chlor.loc["chloride"])
            else:
                plot_frame = plot_frame.div(plot_frame.loc["chloride"])
        
        # Select requested locations and compounds
        plot_frame = plot_frame[locations].loc[compound].T
        
        if rename is not None:
            rename_dict = dict(zip(compound, [rename[0]]))
            plot_frame.rename(rename_dict, axis = 1, inplace = True)
        
        plt.rcParams["figure.dpi"] = 600

        ax.plot(plot_frame, 
                 linestyle='--',
                 marker='o',
                 markersize = 12,
                 lw = 5,
                 color = colors[time],
                 label = f"t = {time}"
                 )
    
    
    ax.set_ylim(ylimit_list[0])
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.tick_params(length = 6, width = 3, labelsize = 25)
    
    ax.tick_params(axis="x", labelrotation = -45)

    if include_ytick:
        #ax.set_ylabel(r"Concentration [$mg/m^3$]", fontsize = 30)
        ax.set_ylabel(r"Relative concentration [$C/C_0$]", fontsize = 30)
    else:
        ax.set_yticklabels([])
        ax.tick_params(axis="y", direction = "in")
    

    ax.set_title(titles[j], fontsize = 40)
    
    l += 1
        
lines_labels = [ax.get_legend_handles_labels()]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, 
           loc = "lower center",
           bbox_to_anchor = (0.5,-0.11),
           fontsize = 40,
           ncol = 5,
           columnspacing = 0.75,
           frameon = False)

fig.supxlabel(r"Measurement locations", fontsize = 40)

plt.show()

