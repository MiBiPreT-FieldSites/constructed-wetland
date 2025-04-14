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
# Electron acceptors
compounds = ["Zuurstof", "nitraat", "sulfaat"]
# Reduced electron acceptors
#compounds = ["sulfide (vrij)", "Mangaan (II)", "Ijzer (2+)"]

# Rename the contaminants to be plotted (optional), put them in the same order as above.
# Rename electron acceptors
rename = ["Oxygen", "Nitrate", "Solphate"]

# Rename reduced electron acceptors
#rename = ["sulfide (free)", "Manganese (II)", "Iron (II)"]

# Locations to plot, using the names of location_dictionary.
colors = ["#89003d", "#f0ab70", "#ffd220", "#66a697", "#004D8A"]
plots = ["CW1_deep", "CW2_deep", "CW3_deep"]
titles = ["CW1", "CW2", "CW3"]
# Relative file path to the excel file with the data
time_points = [0,1,2,3]

normalize = True
compensate_dilution = True
ylimit_list = [(-0.5, 10), (-0.5, 30), (-0.1, 5)]

df_list = []
for time in time_points:
    file_path = f"../../../data/raw/CW_field_meassurements/Raw_data_lab/240120_Resultaten_ronde_T{time}.xlsx"
    df_list.append(tools.cleanup_compound(file_path))

#print(df_list)


#%% 
l = 0
fig, axs = plt.subplots(3,3, figsize = (24,20), layout ="constrained")

for i, compound in enumerate(compounds):
    compound = [compound]
    include_xtick = False
    title = False
    if i == 0: 
        title = True
    elif i == 2:
        include_xtick = True
    
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
            # if normalize:
            #     plot_frame = plot_frame.div(plot_frame["INF"], axis = 0)
            
            # if compensate_dilution:
            #     if not normalize:
            #         comp_chlor = plot_frame.div(plot_frame["INF"], axis = 0)
            #         plot_frame = plot_frame.div(comp_chlor.loc["chloride"])
            #     else:
            #         plot_frame = plot_frame.div(plot_frame.loc["chloride"])
            
            # --- STEP 1: Conditional Normalization (for plotting normalized results) ---

            if normalize:
                norm_frame = plot_frame.copy()

                for cmpd in plot_frame.index:
                    if cmpd != "Zuurstof":
                        try:
                            # Get the scalar INF value for this compound
                            inf_value = plot_frame.at[cmpd, "INF"]
                                
                            # Normalize the full row
                            norm_frame.loc[cmpd] = plot_frame.loc[cmpd] / inf_value

                        except Exception as e:
                            print(f"Skipping {cmpd} due to error: {e}")

                plot_frame = norm_frame


            # --- STEP 2: If chloride correction is requested ---
            if compensate_dilution:
                
                # If normalize is False, we still need to normalize (except Zuurstof) to apply chloride correction
                if not normalize:
                    for cmpd in plot_frame.index:
                        if cmpd != "Zuurstof":
                            try:
                                # Get the scalar INF value for this compound
                                inf_value = plot_frame.at[cmpd, "INF"]
                                    
                                # Normalize the full row
                                norm_frame.loc[cmpd] = plot_frame.loc[cmpd] / inf_value

                            except Exception as e:
                                print(f"Skipping {cmpd} due to error: {e}")

                    plot_frame = norm_frame

            #Now apply chloride-based dilution correction to all compounds
            chloride_correction = plot_frame.loc["chloride"]
            plot_frame = plot_frame.div(chloride_correction)

            
            # Select requested locations and compounds
            plot_frame = plot_frame[locations].loc[compound].T
            
            if rename is not None:
                rename_dict = dict(zip(compound, [rename[i]]))
                plot_frame.rename(rename_dict, axis = 1, inplace = True)
            
            plt.rcParams["figure.dpi"] = 200
    
            ax.plot(plot_frame, 
                     linestyle='--',
                     marker='o',
                     markersize = 12,
                     lw = 5,
                     color = colors[time],
                     label = f"t = {time}"
                     )
        
        
        ax.set_ylim(ylimit_list[i])
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.tick_params(length = 6, width = 2, labelsize = 15)
        if include_xtick:
            ax.tick_params(axis="x", labelrotation = -45)
        else:
            ax.set_xticklabels([])
            ax.tick_params(axis="x", direction = "out")
        
        if include_ytick:
            ax.set_ylabel(f"{rename[i]}", fontsize = 20)
        else:
            ax.set_yticklabels([])
            ax.tick_params(axis="y", direction = "in")
        
        if title:
            ax.set_title(titles[j], fontsize = 20)
        
        l += 1
        
lines_labels = [ax.get_legend_handles_labels()]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, 
           loc = "lower center",
           bbox_to_anchor = (0.5,-0.001),
           fontsize = 20,
           ncol = 5,
           columnspacing = 0.75,
           frameon = False)

fig.supxlabel(r"Measurement locations", fontsize = 20)
fig.supylabel(r"Relative concentration [$C/C_{0}$]", fontsize = 20)
#fig.supylabel(r"Concentration [$g/m^3$]", fontsize = 40)    

plt.show()
