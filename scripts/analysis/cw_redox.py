# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:59:39 2025

@author: Jorrit Bakker
"""

import redox_tools as tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%
# Relative file path to the excel file with the data
file_path = "../../data/redox_data/S9081 HMVT CR1000X_measurements.dat"

# The correction factor with regards to 3M KCl electrode reference
correction = 200

# Load in the file as Excel and clean it up into a seperate dataframe for temperature and redox data
df_redox, df_temp = tools.cleanup_redox(file_path,
                                        correction = correction,
                                        rename = tools.CW_rename
                                        )

#%%
# The nodes you want to plot for the redox plot using node_dictionary
#redox_nodes = tools.node_dictionary["CW3_80cm"]
# Or alternatively by manually choosing the redox nodes
# Naming as: CW# = which wetland, S# = which position along the wetland, -# = which depth
# Options: CW1, CW2, CW3 | S1, S2, S3, S4 | -1 (20cm), -2 (40cm), -3 (60cm), -4 (80cm)
redox_nodes = ["CW1S1-4", "CW2S1-4", "CW3S1-4"]

# The nodes you want to plot for the temperature plot
temp_nodes  = ['CW1S1', 'CW1S2', 'CW1S3', 'CW1S4', 'CW2S1', 'CW2S2', 'CW2S3', 'CW2S4', 'CW3S1', 'CW3S2', 'CW3S3']
# The start and end date of the data you want to plot, as 'YYYY-MM-DD hh-mm-ss'. Hour, minute and second specification is optional
start_date, end_date = '2024-06-01', '2025-05-21'

# Plots the redox data
fig, ax = tools.plot_redox(df_redox,
                 redox_nodes,
                 start_date,
                 end_date,
                 ylimit = (-300, -200),
                 )
fig.legend(bbox_to_anchor = (0.985, 0.97))

# make room at bottom for your xlabel, and on the right for the legend
fig.tight_layout()  
fig.subplots_adjust(bottom=0.15, right=0.70, left=0.15)

plt.show()

# Plots the temperature data
fig, ax = tools.plot_temp(df_temp,
                 temp_nodes,
                 start_date,
                 end_date,
                 )
fig.legend(bbox_to_anchor = (0.985, 0.97))

fig.tight_layout()  
fig.subplots_adjust(bottom=0.15, right=0.70, left=0.15)
plt.show() 

#%%
# Alternatively, plot temperature and redox in the same figure:
fig, ax1 = tools.plot_redox(df_redox,
                 redox_nodes,
                 start_date,
                 end_date,
                 ylimit = (-300, -200)
                 )

# Twinning the x-axis to allow for second y-axis.
ax2 = ax1.twinx()

# Pass the twinned axes object to the plot_temperature function to plot it on the second y-axis.
ax2 = tools.plot_temp(df_temp,
                 temp_nodes,
                 start_date,
                 end_date,
                 mean = True,
                 ax = ax2,
                 color = "black",
                 alpha = 0.8,
                 )
#fig.legend(bbox_to_anchor = (0.985, 0.97), fontsize = 10)
# Draw legend: smaller text, tighter layout
legend = fig.legend(
    loc='upper right',
    bbox_to_anchor=(1.02, 0.98),
    fontsize=6,            # make the text smaller
    handlelength=1,        # shorten the little line samples
    labelspacing=0.4,      # reduce space between entries
    borderpad=0.4,         # shrink the padding around the legend box
    frameon=False          # optional: remove the gray box background
)

fig.tight_layout()  
fig.subplots_adjust(bottom=0.15, right=0.75, left=0.15)
plt.show()