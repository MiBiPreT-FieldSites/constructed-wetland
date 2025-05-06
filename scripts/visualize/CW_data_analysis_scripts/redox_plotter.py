#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Sep  2 11:27:02 2024

@author: jorrit
"""

import tools as tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Relative file path to the excel file with the data
redox_path = "./Raw_wetland_redox_data_jan.xlsx"
rain_path = "./CW_Griftpark_6-11-24_12-00_AM_1_Year_1736850068_v2.xlsx"

# The correction factor with regards to 3M KCl electrode reference
correction = 200

# Load in the files as a dataframe and clean up the data
df_redox, df_temp = tools.cleanup_redox(redox_path, correction = correction)
raindata = tools.cleanup_rain(rain_path)

#%%

# The nodes you want to plot for the redox plot
redox_nodes = tools.node_dictionary_2["CW3_20cm"]
#redox_nodes = ['1-4', '2-4', '3-4', '4-4']
# The nodes you want to plot for the temperature plot
temp_nodes  = ['CW1S1', 'CW1S2', 'CW1S3', 'CW1S3', 'CW2S1', 'CW2S2', 'CW2S3', 'CW2S4', 'CW3S1', 'CW3S2', 'CW3S3']
# The start and end date of the data you want to plot, as 'YYYY-MM-DD hh-mm-ss'. Hour, minute and second specification is optional
start_date, end_date  = '2024-09-01', '2025-01-13'

# Plots the redox data, optionally, also plot the rain data alongside.
tools.plot_redox(df_redox, redox_nodes, start_date, end_date,
                 #raindata = raindata,
                 #tempdata = df_temp,
                 #temp_nodes = temp_nodes,
                 resample_rain = "6h",
                 ylimit_redox=(-320, -200),
                 legend_pos=(0.91, 0.97)
                 #legend_pos=(0.35,0.33)
                 )
#plt.title("Redox potentiaal in CW3 op 80cm diepte")

# Plots the temperature data
#tools.plot_temp(df_temp, temp_nodes, start_date, end_date, ylimit=(7,23))
#plt.title("Temperature data for constructed wetland")
