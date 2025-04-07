#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Oct 23 08:17:09 2024

@author: jorrit
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def cleanup_compound(file_path):
    """ Takes an excel sheet of default format of Constructed Wetland monitoring
    and changes it into a dataframe that can be plotted.

    Parameters
    ----------
    file_path : str
        Path to excel sheet containing sampling data.

    Returns
    -------
    dataframe : pd.DataFrame
        A cleaned up dataframe containing the data from the input Excel sheet.

    """

    dataframe = pd.read_excel(file_path, skiprows=1, sheet_name = "Analyseresultaten", index_col=[0], decimal = ",")

    monster_names = dataframe.loc["Monsteromschrijving"].tolist()
    monster_names[0] = "unit"
    dataframe.columns = monster_names

    # Mentioned rows and rows without any data are not needed and thus removed
    drop_rows = ["Analysis", "Projectcode", "Projectnaam", "Monsteromschrijving", "Rapport status", "Validatie status", "Rapport Datum", "Start Datum"]
    dataframe = dataframe.drop(drop_rows)
    dataframe = dataframe.dropna(axis = "index", how = "all")

    # Couple "Monsternummer" to the standard codes for measurement points and rename columns.
    keyframe = pd.read_excel(file_path, sheet_name = "Watermonstergegevens", decimal = ".")
    rename_dict = pd.Series(keyframe.Meetpunt.values, index = keyframe.Monsternummer).to_dict()
    dataframe.rename(columns = rename_dict, inplace = True)

    # Oxygen concentrations are located in the second tab, so these are added seperately to the dataframe
    oxygen_data = keyframe.loc[:, ("Meetpunt", "Zuurstof")].T
    oxygen_data.rename(columns = oxygen_data.loc["Meetpunt"], inplace = True)
    oxygen_data.drop("Meetpunt", axis = 0, inplace = True)
    oxygen_data.loc[:,"unit"] = "mg/l"
    oxygen_data = oxygen_data[dataframe.columns]
    #oxygen_data = oxygen_data.fillna(0.0)
    dataframe = pd.concat([dataframe, oxygen_data])

    # Compounds under the detection limit have been entered as <*detection limit*.
    # These values are set to 0. 
    dataframe = dataframe.map(lambda x: 0 if isinstance(x, str) and x.startswith('<') else x)

    # For analysis, the entries of the dataframe should be seen as floats.

    for col in dataframe.columns:
        if (col != 'unit'):
            mask = dataframe.index[(dataframe.index != "Zuurstof")].tolist()
            dataframe.loc[mask, col] = dataframe.loc[mask, col].str.strip()
            dataframe[col] = pd.to_numeric(dataframe.loc[:, col], errors='coerce')
    dataframe = dataframe.fillna(0.0)

    
    return(dataframe)


def cleanup_redox(file_path, correction = 200):
    """ Takes an excel sheet of default format of Constructed Wetland redox and
    temperature data and changes it into two dataframes for redox and temperature
    that can be plotted.

    Parameters
    ----------
    file_path : str
        Path to excel sheet containing redox data.
    correction : int or float (default is 200)
        The correction factor with regards to 3M KCl electrode reference for the redox data

    Returns
    -------
    df_redox : pd.Dataframe
        A cleaned up dataframe containing the redox data from the input Excel sheet.
    df_temp : pd.Dataframe
        A cleaned up dataframe containing the temperature data from the input Excel sheet.

    """
    
    dataframe = pd.read_excel(file_path, sheet_name = 0)

    drop_rows = [0,1,2,3]
    drop_cols = ['batt_volt_Avg', 'RECORD', 'TIMESTAMP']
    
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe.drop(drop_rows)
    
    # Time column is set to datatime datatype and moved to first column of dataframe for ease of reading.
    dataframe['Time'] = pd.to_datetime(dataframe['TIMESTAMP'])
    move_col = dataframe.pop("Time")
    dataframe.insert(0, "Time", move_col)
    dataframe = dataframe.drop(drop_cols, axis = 1)
    
    # Split dataframe into redox and temperature by selecting on the beginning of the column names.
    df_redox = dataframe.filter(regex='^redox')
    df_redox = pd.concat([dataframe['Time'], df_redox], axis = 1)
    df_temp = dataframe.filter(regex='^temp')
    df_temp = pd.concat([dataframe['Time'], df_temp], axis = 1)


    rename_dict = {
        'redox_raw_Avg(1)'  : '1-1', 'redox_raw_Avg(2)'   : '1-2', 'redox_raw_Avg(3)'   : '1-3', 'redox_raw_Avg(4)'   : '1-4',
        'redox_raw_Avg(5)'  : '2-1', 'redox_raw_Avg(6)'   : '2-2', 'redox_raw_Avg(7)'   : '2-3', 'redox_raw_Avg(8)'   : '2-4',
        'redox_raw_Avg(9)'  : '3-1', 'redox_raw_Avg(10)'  : '3-2', 'redox_raw_Avg(11)'  : '3-3', 'redox_raw_Avg(12)'  : '3-4',
        'redox_raw_Avg(13)' : '4-1', 'redox_raw_Avg(14)'  : '4-2', 'redox_raw_Avg(15)'  : '4-3', 'redox_raw_Avg(16)'  : '4-4',
        'redox_raw_Avg(17)' : '5-1', 'redox_raw_Avg(18)'  : '5-2', 'redox_raw_Avg(19)'  : '5-3', 'redox_raw_Avg(20)'  : '5-4',
        'redox_raw_Avg(21)' : '6-1', 'redox_raw_Avg(22)'  : '6-2', 'redox_raw_Avg(23)'  : '6-3', 'redox_raw_Avg(24)'  : '6-4',
        'redox_raw_Avg(25)' : '7-1', 'redox_raw_Avg(26)'  : '7-2', 'redox_raw_Avg(27)'  : '7-3', 'redox_raw_Avg(28)'  : '7-4',
        'redox_raw_Avg(29)' : '8-1', 'redox_raw_Avg(30)'  : '8-2', 'redox_raw_Avg(31)'  : '8-3', 'redox_raw_Avg(32)'  : '8-4',
        'redox_raw_Avg(33)' : '9-1', 'redox_raw_Avg(34)'  : '9-2', 'redox_raw_Avg(35)'  : '9-3', 'redox_raw_Avg(36)'  : '9-4',
        'redox_raw_Avg(37)' : '10-1', 'redox_raw_Avg(38)' : '10-2', 'redox_raw_Avg(39)' : '10-3', 'redox_raw_Avg(40)' : '10-4',
        'redox_raw_Avg(41)' : '11-1', 'redox_raw_Avg(42)' : '11-2', 'redox_raw_Avg(43)' : '11-3', 'redox_raw_Avg(44)' : '11-4',
        'redox_raw_Avg(45)' : '12-1', 'redox_raw_Avg(46)' : '12-2', 'redox_raw_Avg(47)' : '12-3', 'redox_raw_Avg(48)' : '12-4',
        'temp_C_Avg(1)'     : 'T1', 'temp_C_Avg(2)'       : 'T2', 'temp_C_Avg(3)'       : 'T3', 'temp_C_Avg(4)'       : 'T4',
        'temp_C_Avg(5)'     : 'T5', 'temp_C_Avg(6)'       : 'T6', 'temp_C_Avg(7)'       : 'T7', 'temp_C_Avg(8)'       : 'T8',
        'temp_C_Avg(9)'     : 'T9', 'temp_C_Avg(10)'      : 'T10', 'temp_C_Avg(11)'     : 'T11', 'temp_C_Avg(12)'     : 'T12'
        }
    
    rename_dict = {
        'redox_raw_Avg(1)'  : 'CW1S1-1', 'redox_raw_Avg(2)'   : 'CW1S1-2', 'redox_raw_Avg(3)'   : 'CW1S1-3', 'redox_raw_Avg(4)'   : 'CW1S1-4',
        'redox_raw_Avg(5)'  : 'CW1S2-1', 'redox_raw_Avg(6)'   : 'CW1S2-2', 'redox_raw_Avg(7)'   : 'CW1S2-3', 'redox_raw_Avg(8)'   : 'CW1S2-4',
        'redox_raw_Avg(9)'  : 'CW1S3-1', 'redox_raw_Avg(10)'  : 'CW1S3-2', 'redox_raw_Avg(11)'  : 'CW1S3-3', 'redox_raw_Avg(12)'  : 'CW1S3-4',
        'redox_raw_Avg(13)' : 'CW1S4-1', 'redox_raw_Avg(14)'  : 'CW1S4-2', 'redox_raw_Avg(15)'  : 'CW1S4-3', 'redox_raw_Avg(16)'  : 'CW1S4-4',
        'redox_raw_Avg(17)' : 'CW2S1-1', 'redox_raw_Avg(18)'  : 'CW2S1-2', 'redox_raw_Avg(19)'  : 'CW2S1-3', 'redox_raw_Avg(20)'  : 'CW2S1-4',
        'redox_raw_Avg(21)' : 'CW2S2-1', 'redox_raw_Avg(22)'  : 'CW2S2-2', 'redox_raw_Avg(23)'  : 'CW2S2-3', 'redox_raw_Avg(24)'  : 'CW2S2-4',
        'redox_raw_Avg(25)' : 'CW2S3-1', 'redox_raw_Avg(26)'  : 'CW2S3-2', 'redox_raw_Avg(27)'  : 'CW2S3-3', 'redox_raw_Avg(28)'  : 'CW2S3-4',
        'redox_raw_Avg(29)' : 'CW2S4-1', 'redox_raw_Avg(30)'  : 'CW2S4-2', 'redox_raw_Avg(31)'  : 'CW2S4-3', 'redox_raw_Avg(32)'  : 'CW2S4-4',
        'redox_raw_Avg(33)' : 'CW3S1-1', 'redox_raw_Avg(34)'  : 'CW3S1-2', 'redox_raw_Avg(35)'  : 'CW3S1-3', 'redox_raw_Avg(36)'  : 'CW3S1-4',
        'redox_raw_Avg(37)' : 'CW3S2-1', 'redox_raw_Avg(38)'  : 'CW3S2-2', 'redox_raw_Avg(39)'  : 'CW3S2-3', 'redox_raw_Avg(40)'  : 'CW3S2-4',
        'redox_raw_Avg(41)' : 'CW3S3-1', 'redox_raw_Avg(42)'  : 'CW3S3-2', 'redox_raw_Avg(43)'  : 'CW3S3-3', 'redox_raw_Avg(44)'  : 'CW3S3-4',
        'redox_raw_Avg(45)' : 'CW3S4-1', 'redox_raw_Avg(46)'  : 'CW3S4-2', 'redox_raw_Avg(47)'  : 'CW3S4-3', 'redox_raw_Avg(48)'  : 'CW3S4-4',
        'temp_C_Avg(1)'     : 'CW1S1', 'temp_C_Avg(2)'        : 'CW1S2', 'temp_C_Avg(3)'        : 'CW1S3', 'temp_C_Avg(4)'        : 'CW1S4',
        'temp_C_Avg(5)'     : 'CW2S1', 'temp_C_Avg(6)'        : 'CW2S2', 'temp_C_Avg(7)'        : 'CW2S3', 'temp_C_Avg(8)'        : 'CW2S4',
        'temp_C_Avg(9)'     : 'CW3S1', 'temp_C_Avg(10)'       : 'CW3S2', 'temp_C_Avg(11)'       : 'CW3S3', 'temp_C_Avg(12)'       : 'CW3S4'
        }
    
    # Column names are changed to more concise names for ease of understanding.
    df_redox.rename(columns = rename_dict, inplace = True)
    df_temp.rename(columns = rename_dict, inplace = True)
    
    # For analysis, datatype has to be set to floats
    df_redox.loc[:, df_redox.columns != 'Time'] = df_redox.loc[:, df_redox.columns != 'Time'].apply(pd.to_numeric, errors='coerce') + correction
    df_temp.loc[:, df_temp.columns != 'Time'] = df_temp.loc[:, df_temp.columns != 'Time']. apply(pd.to_numeric, errors='coerce')
    
    df_redox = df_redox.set_index("Time")
    df_redox = df_redox.apply(pd.to_numeric, errors='coerce')
    df_temp = df_temp.set_index("Time")
    df_temp = df_temp.apply(pd.to_numeric, errors='coerce')

    return(df_redox, df_temp)

def cleanup_rain(file_path):
    """ Takes an excel sheet of export format from Weatherlink weather data of
    Constructed Wetland and gives a dataframe with rainfall over time.

    Parameters
    ----------
    file_path : str
        Path to excel sheet containing weather data.

    Returns
    -------
    raindata : pd.Dataframe
        A dataframe with rainfall over time.

    """
    
    dataframe = pd.read_excel(file_path, skiprows=1)
    
    
    dataframe.columns = dataframe.iloc[0]
    
    # Column names are first set to source of data, to be able to select the rain data
    # from the Constructed Wetland
    colnames = list(dataframe)
    colnames[0] = "Time"
    dataframe.columns = colnames
    dataframe = dataframe.loc[:, ["Time", "CW pilot GP RWZI"]]
    
    # Once only weather data from Constructed Wetland is present, column names can
    # be set to weather data types.
    dataframe.columns = dataframe.iloc[3]
    dataframe.rename(columns = {"Date & Time" : "Time"}, inplace = True)
    dataframe = dataframe.drop([0,1,2,3])
    
    # Only Rain - mm and time information is needed, so other columns are removed.
    dataframe["Time"] = pd.to_datetime(dataframe['Time'])
    raindata = dataframe.loc[:, ["Time", "Rain - mm"]]
    
    # For analysis, datatype has to be set to floats
    raindata = raindata.set_index("Time")
    raindata = raindata.apply(pd.to_numeric, errors='coerce')

    
    return raindata

def plot_compound(dataframe, locations, compounds, rename = None, normalize = False, compensate_dilution = False, plot_type = "line", ylimit = False, **kwargs):
    """ Plot contaminant concentrations for each location from a dataframe.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe containing compound concentrations for each sample location.
    locations : list
        List with the name of each sample location to be plotted.
    compounds : list
        List with the name of each compound to be plotted.
    normalize : bool
        Flag that normalizes the data to the input concentration.
    **kwargs : 
        Keyword arguments to be passed to df.plot()

    Returns
    -------
    ax : Line plot of requested parameters.

    """
    
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
    
    if not normalize:
        plot_frame = plot_frame.div(1000)
    
    # Select requested locations and compounds
    plot_frame = plot_frame[locations].loc[compounds].T
        
    # Keep information of units of plotted compounds
    plot_units = dataframe["unit"].loc[compounds]
    
    if rename is not None:
        rename_dict = dict(zip(compounds, rename))
        plot_frame.rename(rename_dict, axis = 1, inplace = True)
        plot_units.rename(rename_dict, axis = 0, inplace = True)
    
    # Generate list of each unique unit in the plot.
    units = list(set(plot_units.tolist()))

    plt.rcParams["figure.dpi"] = 600

    # If the compounds to be plotted have two different units, they will be plotted
    # on seperate y-axis.
    if (len(units) != 2) or normalize == True:
        unit = units[0]
        ax = plot_frame.plot.line(**kwargs)
        if normalize:
            ax.set_ylabel("C/C0")
        else:
            ax.set_ylabel(f"Concentration [{unit}]")

    elif len(units) == 2:
        unit_right, unit_left = units[0], units[1]
        cols_secondary = plot_units[plot_units == unit_right].index.tolist()
        ax = plot_frame.plot.line(secondary_y=cols_secondary, **kwargs)
        ax.set_ylabel(f"Concentration [{unit_left}]")
        ax.right_ax.set_ylabel(f"Concentration [{unit_right}]")

    if ylimit != False:
        try:
            ax.set_ylim(ylimit)
        except:
            print("ylimits_redox is not of the correct format and is thus ignored.")

    ax.set_xlabel("Measurement locations")

    return plot_frame, ax

def plot_compound_combi(dataframe, locations, compounds, ax,
                        rename = None,
                        normalize = False,
                        compensate_dilution = False,
                        ylimit = False,
                        **kwargs):
    """ Plot contaminant concentrations for each location from a dataframe.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe containing compound concentrations for each sample location.
    locations : list
        List with the name of each sample location to be plotted.
    compounds : list
        List with the name of each compound to be plotted.
    normalize : bool
        Flag that normalizes the data to the input concentration.
    **kwargs : 
        Keyword arguments to be passed to df.plot()

    Returns
    -------
    ax : Line plot of requested parameters.

    """
    
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
    
    if not normalize:
        plot_frame = plot_frame.div(1000)
    
    # Select requested locations and compounds
    plot_frame = plot_frame[locations].loc[compounds].T
        
    # Keep information of units of plotted compounds
    plot_units = dataframe["unit"].loc[compounds]
    
    if rename is not None:
        rename_dict = dict(zip(compounds, rename))
        plot_frame.rename(rename_dict, axis = 1, inplace = True)
        plot_units.rename(rename_dict, axis = 0, inplace = True)
    
    # Generate list of each unique unit in the plot.
    units = list(set(plot_units.tolist()))

    plt.rcParams["figure.dpi"] = 600

    # If the compounds to be plotted have two different units, they will be plotted
    # on seperate y-axis.

    unit = units[0]
    plot_frame.plot.line(ax = ax, **kwargs)

def plot_redox(df_redox, redox_nodes, start_date, end_date,
               raindata = False, resample_rain = False, tempdata = False, temp_nodes = None, colors = None,
               ylimit_redox = False, legend_pos = (0.9, 1), **kwargs):
    """ Plot redox potential and optionally rainfall data for selected nodes in a timeframe.
    

    Parameters
    ----------
    df_redox : pd.DataFrame
        Dataframe with redox data
    redox_nodes : List
        List with nodes from the dataframe to be plotted
    start_date : str
        The start date of the data to be plotted, as "YYYY-MM-DD"
    end_date : str
        The end date of the data to be plotted, as "YYYY-MM-DD"
    raindata : pd.DataFrame, optional
        Dataframe with rainfall data, will be plotted with redox data. The default is False.
    resample_rain : Bool, optional
        Time length to resample the rain data to. The default is False.
    ylimit_redox : tuple, optional
        Manually set y-axis range for the redox data, as (min_y, max_y). The default is False.
    legend_pos : tuple, optional
        Manually set legend position, as (x_pos, y_pos), relative to origin. The default is (0.9, 1).

    Returns
    -------
    None.

    """
    
    
    mask = (df_redox.index > start_date) & (df_redox.index <= end_date)
    df_redox_plot = df_redox[mask]

    fig, ax1 = plt.subplots(figsize=(10, 7), dpi=600)

    # If rainfall data is provided, it will be plotted alongside the redox data.
    if isinstance(raindata, pd.DataFrame):
        mask = (raindata.index > start_date) & (raindata.index <= end_date)
        raindata_plot = raindata[mask]
        if isinstance(resample_rain, str):
            try:
                raindata_plot = raindata_plot.resample(resample_rain).sum()
            except:
                print("Invalid time input for resampling. Defaulted to days.")
                print("Examples of valid entries; '1h' for 1 hour, '300min' for 300 minutes, '2D' for 2 days and 'W' for a week.")
                raindata_plot = raindata_plot.resample("D").sum()
        else:
            resample_rain = "15min"
        
        # Twinning the x-axis allows for a second y-axis.
        ax2 = ax1.twinx()
        ax2.fill_between(raindata_plot.index, raindata_plot["Rain - mm"], color='blue', alpha=0.5, label = f"Rainfall per {resample_rain}")  
        ax2.set_ylabel("Rainfall [mm]", fontsize = 20)
        ax2.tick_params(labelsize = 16, which = "both")
    # If no raindata is provided and there is temperature data provided, it will be plotted alongside the redox data.
    if isinstance(tempdata, pd.DataFrame) and raindata == False:
        mask = (tempdata.index > start_date) & (tempdata.index <= end_date)
        tempdata_plot = tempdata[mask]
        tempdata_plot.loc[:,'mean_temperature'] = tempdata_plot.loc[:,temp_nodes].mean(axis=1)
        
        # Twinning the x-axis allows for a second y-axis.
        ax2 = ax1.twinx()
        ax2.plot(tempdata_plot.index, tempdata_plot["mean_temperature"], "--", color='black', label = f"Mean temperature", alpha = 0.8, **kwargs)  
        ax2.set_ylabel("Temperature [ºC]", fontsize = 20)
        ax2.tick_params(labelsize = 16, which = "both")
        
    for i, node in enumerate(redox_nodes):
        if colors == None:
            ax1.plot(df_redox_plot.index, df_redox_plot[node], label = f"Node {node}", **kwargs)
        else:
            ax1.plot(df_redox_plot.index, df_redox_plot[node], color = colors[i], label = f"Node {node}", **kwargs)

    ax1.set_xlabel("Time", fontsize = 20)
    ax1.set_ylabel("Redox potential [mV]", fontsize = 20)


    try:
        fig.legend(bbox_to_anchor=legend_pos, fontsize = 16)
    except:
        print("Invalid legend_pos, used plot default instead.")
        fig.legend(fontsize = 14)
    
    if ylimit_redox != False:
        try:
            ax1.set_ylim(ylimit_redox)
        except:
            print("ylimits_redox is not of the correct format and is thus ignored.")
    
    # Modify axis ticks with the goal to make it more readable.
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax1.tick_params(axis='x', rotation=0, pad=15)

    ax1.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax1.tick_params(axis='x', which='minor', length=4, width=1)
    
    ax1.tick_params(labelsize = 16, which = "both")
    ax1.tick_params(axis ='x', which = "major", length=0, width = 0, pad = 25)
    if isinstance(tempdata, pd.DataFrame) or isinstance(raindata, pd.DataFrame):
        ax2.tick_params(labelsize = 16)
    
    fig.tight_layout()
    if isinstance(tempdata, pd.DataFrame) or isinstance(raindata, pd.DataFrame):
        return(ax1, ax2)
    else:
        return(ax1)


def plot_temp(df_temp, temp_nodes, start_date, end_date, ylimit = False, legend_pos = (1.1, 1)):
    """ Plot temperature for a selection of nodes in a specified timeframe.
    

    Parameters
    ----------
    df_temp : pd.DataFrame
        Dataframe with temperature data
    temp_nodes : List
        List with nodes from the dataframe to be plotted
    start_date : str
        The start date of the data to be plotted, as "YYYY-MM-DD"
    end_date : str
        The end date of the data to be plotted, as "YYYY-MM-DD"
    ylimit : tuple, optional
        Manually set y-axis range for the redox data, as (min_y, max_y). The default is False.
    legend_pos : tuple, optional
        Manually set legend position, as (x_pos, y_pos), relative to origin. The default is (1.1, 1).

    Returns
    -------
    None.

    """

    mask = (df_temp.index > start_date) & (df_temp.index <= end_date)
    df_temp = df_temp[mask]
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    
    for i, points in enumerate(temp_nodes):
        ax.plot(df_temp.index, df_temp[points], label = points)
        
    if ylimit != False:
        try:
            ax.set_ylim(ylimit)
        except:
            print("ylimits is not of the correct format and is thus ignored.")
            
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (ºC)', fontsize = 18)

    # Modify axis ticks with the goal to make it more readable.    
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax.set_xlabel("Time", fontsize = 18)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax.tick_params(axis='x', rotation=0, pad=15)

    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax.tick_params(axis='x', which='minor', length=4, width=1)
    
    ax.tick_params(labelsize = 16, which = "both")
    ax.tick_params(axis ='x', which = "major", length=0, width = 0, pad = 25)
    plt.legend(fontsize = 18)
    
def plot_rain(raindata,
              resample_rain,
              start_date,
              end_date,
              **kwargs
              ):
    mask = (raindata.index > start_date) & (raindata.index <= end_date)
    raindata_plot = raindata[mask]
    if isinstance(resample_rain, str):
        try:
            raindata_plot = raindata_plot.resample(resample_rain).sum()
        except:
            print("Invalid time input for resampling. Defaulted to days.")
            print("Examples of valid entries; '1h' for 1 hour, '300min' for 300 minutes, '2D' for 2 days and 'W' for a week.")
            raindata_plot = raindata_plot.resample("D").sum()
    else:
        resample_rain = "15min"
        
    fig, ax1 = plt.subplots(figsize=(14, 6), dpi=600)
    # Twinning the x-axis allows for a second y-axis.

    ax1.fill_between(raindata_plot.index, raindata_plot["Rain - mm"], color='blue', alpha=0.5, label = f"Rainfall per {resample_rain}")  
    ax1.set_ylabel("Rainfall [mm]", fontsize = 18)
    ax1.set_xlabel("Time", fontsize = 18)
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax1.tick_params(axis='x', rotation=0, pad=15)

    ax1.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax1.tick_params(axis='x', which='minor', length=4, width=1)
    
    ax1.tick_params(labelsize = 16, which = "both")
    ax1.tick_params(axis ='x', which = "major", length=0, width = 0, pad = 25)
    plt.legend(fontsize = 18)

def plot_compound_redox(df_redox,
                        df_compound,
                        redox_nodes,
                        compounds,
                        location,
                        rename,
                        redox_start_date,
                        redox_end_date,
                        legend_pos,
                        normalize = True,
  
                        **kwargs
                        ):

    locations_redox = location_combi_dictionary[location]
    locations_compound = location_dictionary[location]
    
    mask = (df_redox.index > redox_start_date) & (df_redox.index <= redox_end_date)
    df_redox_plot = df_redox[mask]
    df_redox_plot = df_redox_plot[redox_nodes]

    node_rename_dictionary = {
        "1-1"  : "CW1MF01", "1-2"  : "CW1MF01", "1-3"  : "CW1MF02", "1-4"  : "CW1MF02",
        "2-1"  : "CW1MF03", "2-2"  : "CW1MF03", "2-3"  : "CW1MF04", "2-4"  : "CW1MF04",
        "3-1"  : "CW1MF09", "3-2"  : "CW1MF09", "3-3"  : "CW1MF10", "3-4"  : "CW1MF10",
        "4-1"  : "CW1MF11", "4-2"  : "CW1MF11", "4-3"  : "CW1MF12", "4-4"  : "CW1MF12",
        "5-1"  : "CW2MF01", "5-2"  : "CW2MF01", "5-3"  : "CW2MF02", "5-4"  : "CW2MF02",
        "6-1"  : "CW2MF03", "6-2"  : "CW2MF03", "6-3"  : "CW2MF04", "6-4"  : "CW2MF04",
        "7-1"  : "CW2MF09", "7-2"  : "CW2MF09", "7-3"  : "CW2MF10", "7-4"  : "CW2MF10",
        "8-1"  : "CW2MF11", "8-2"  : "CW2MF11", "8-3"  : "CW2MF12", "8-4"  : "CW2MF12",
        "9-1"  : "CW3MF01", "9-2"  : "CW3MF01", "9-3"  : "CW3MF02", "9-4"  : "CW3MF02",
        "10-1" : "CW3MF03", "10-2" : "CW3MF03", "10-3" : "CW3MF04", "10-4" : "CW3MF04",
        "11-1" : "CW3MF09", "11-2" : "CW3MF09", "11-3" : "CW3MF10", "11-4" : "CW3MF10",
        "12-1" : "CW3MF11", "12-2" : "CW3MF11", "12-3" : "CW3MF12", "12-4" : "CW3MF12",
        }
    
    node_rename_dictionary = {
        'redox_raw_Avg(1)'  : 'CW1S1-1', 'redox_raw_Avg(2)'   : 'CW1S1-2', 'redox_raw_Avg(3)'   : 'CW1S1-3', 'redox_raw_Avg(4)'   : 'CW1S1-4',
        'redox_raw_Avg(5)'  : 'CW1S2-1', 'redox_raw_Avg(6)'   : 'CW1S2-2', 'redox_raw_Avg(7)'   : 'CW1S2-3', 'redox_raw_Avg(8)'   : 'CW1S2-4',
        'redox_raw_Avg(9)'  : 'CW1S3-1', 'redox_raw_Avg(10)'  : 'CW1S3-2', 'redox_raw_Avg(11)'  : 'CW1S3-3', 'redox_raw_Avg(12)'  : 'CW1S3-4',
        'redox_raw_Avg(13)' : 'CW1S4-1', 'redox_raw_Avg(14)'  : 'CW1S4-2', 'redox_raw_Avg(15)'  : 'CW1S4-3', 'redox_raw_Avg(16)'  : 'CW1S4-4',
        'redox_raw_Avg(17)' : 'CW2S1-1', 'redox_raw_Avg(18)'  : 'CW2S1-2', 'redox_raw_Avg(19)'  : 'CW2S1-3', 'redox_raw_Avg(20)'  : 'CW2S1-4',
        'redox_raw_Avg(21)' : 'CW2S2-1', 'redox_raw_Avg(22)'  : 'CW2S2-2', 'redox_raw_Avg(23)'  : 'CW2S2-3', 'redox_raw_Avg(24)'  : 'CW2S2-4',
        'redox_raw_Avg(25)' : 'CW2S3-1', 'redox_raw_Avg(26)'  : 'CW2S3-2', 'redox_raw_Avg(27)'  : 'CW2S3-3', 'redox_raw_Avg(28)'  : 'CW2S3-4',
        'redox_raw_Avg(29)' : 'CW2S4-1', 'redox_raw_Avg(30)'  : 'CW2S4-2', 'redox_raw_Avg(31)'  : 'CW2S4-3', 'redox_raw_Avg(32)'  : 'CW2S4-4',
        'redox_raw_Avg(33)' : 'CW3S1-1', 'redox_raw_Avg(34)'  : 'CW3S1-2', 'redox_raw_Avg(35)'  : 'CW3S1-3', 'redox_raw_Avg(36)'  : 'CW3S1-4',
        'redox_raw_Avg(37)' : 'CW3S2-1', 'redox_raw_Avg(38)'  : 'CW3S2-2', 'redox_raw_Avg(39)'  : 'CW3S2-3', 'redox_raw_Avg(40)'  : 'CW3S2-4',
        'redox_raw_Avg(41)' : 'CW3S3-1', 'redox_raw_Avg(42)'  : 'CW3S3-2', 'redox_raw_Avg(43)'  : 'CW3S3-3', 'redox_raw_Avg(44)'  : 'CW3S3-4',
        'redox_raw_Avg(45)' : 'CW3S4-1', 'redox_raw_Avg(46)'  : 'CW3S4-2', 'redox_raw_Avg(47)'  : 'CW3S4-3', 'redox_raw_Avg(48)'  : 'CW3S4-4',
        'temp_C_Avg(1)'     : 'CW1S1', 'temp_C_Avg(2)'        : 'CW1S2', 'temp_C_Avg(3)'        : 'CW1S3', 'temp_C_Avg(4)'        : 'CW1S4',
        'temp_C_Avg(5)'     : 'CW2S1', 'temp_C_Avg(6)'        : 'CW2S2', 'temp_C_Avg(7)'        : 'CW2S3', 'temp_C_Avg(8)'        : 'CW2S4',
        'temp_C_Avg(9)'     : 'CW3S1', 'temp_C_Avg(10)'       : 'CW3S2', 'temp_C_Avg(11)'       : 'CW3S3', 'temp_C_Avg(12)'       : 'CW3S4'
        }

    df_redox_plot.rename(columns = node_rename_dictionary, inplace = True)

    not_in_redox = list(set(locations_redox) - set(df_redox_plot.columns))

    redox_quantiles = df_redox_plot.quantile([0.1, 0.5, 0.9])

    for loc in not_in_redox:
        redox_quantiles[loc] = np.nan

    df_compound_plot = df_compound[locations_compound].loc[compounds]
    
    if rename is not None:
        rename_dict = dict(zip(compounds, rename))
        df_compound_plot.rename(rename_dict, axis = 0, inplace = True)

    redox_quantiles = redox_quantiles[locations_redox]

    downerror = redox_quantiles.iloc[1,:] - redox_quantiles.iloc[0,:]
    uperror = redox_quantiles.iloc[2,:] - redox_quantiles.iloc[1,:]

    if normalize:
        df_compound_plot = df_compound_plot.div(df_compound_plot["INF"], axis = 0)

    fig, ax1 = plt.subplots(figsize=(8, 6), dpi=300)
    ax2 = ax1.twinx()

    ax2.errorbar(redox_quantiles.columns, redox_quantiles.iloc[1,:],
                 yerr = [downerror, uperror],
                 marker = "o",
                 linestyle = "none",
                 color = "black",
                 capsize = 5,
                 label = "redox"
                 )

    ax2.set_ylabel("Redox potential [mV]")
    
    for compound in df_compound_plot.index:
        ax1.plot(df_compound_plot.columns,
                 df_compound_plot.loc[compound],
                 label = str(compound),
                 **kwargs)
    
    ax1.set_xlabel("Measurement locations")
    if normalize:  
        ax1.set_ylabel("C/C0")
    else: 
        ax1.set_ylabel("Concentration [µg/L]")
    fig.legend(bbox_to_anchor = legend_pos)
    return(fig, ax1, ax2)

def plot_time_compound(dataframe,
                       locations,
                       compounds,
                       rename = None,
                       normalize = False,
                       compensate_dilution = False,
                       plot_type = "line",
                       ylimit = False,
                       **kwargs
                        ):
    """ Plot contaminant concentrations for each location from a dataframe.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe containing compound concentrations for each sample location.
    locations : list
        List with the name of each sample location to be plotted.
    compounds : list
        List with the name of each compound to be plotted.
    normalize : bool
        Flag that normalizes the data to the input concentration.
    **kwargs : 
        Keyword arguments to be passed to df.plot()

    Returns
    -------
    ax : Line plot of requested parameters.

    """

    plot_frame = dataframe.drop(columns = "unit", axis=0)
    
    # Influent is the same for each wetland, thus divide by it to normalize data.
    if normalize:
        plot_frame = plot_frame.div(plot_frame["INF"], axis = 0)
    
    if compensate_dilution:
        plot_frame = plot_frame.div(plot_frame.loc["chloride"])
    
    # Select requested locations and compounds
    plot_frame = plot_frame[locations].loc[compounds].T
        
    # Keep information of units of plotted compounds
    plot_units = dataframe["unit"].loc[compounds]\
        
    print(plot_frame.head)
    
    if rename is not None:
        rename_dict = dict(zip(compounds, rename))
        plot_frame.rename(rename_dict, axis = 1, inplace = True)

    
    plt.rcParams["figure.dpi"] = 300

    plt.plot(plot_frame[location_dictionary[locations]])
    
    unit = list(set(plot_units.tolist()))
        
    if normalize:
        plt.ylabel("C/C0")
    else:
        plt.ylabel(f"Concentration [{unit}]")
        
    plt.xlabel("Measurement locations")
    
    plt.legend()

def plot_multi_compound(dataframe_list,
                        compound,
                        location,
                        depth = "deep",
                        normalize = False,
                        palette = ["#491212FF", "#F27127FF", "#F24C27FF", "#BF281BFF", "#CE471CFF"]
                        ):
    """ Plot contaminant concentrations for each location from a dataframe.
    
    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe containing compound concentrations for each sample location.
    locations : list
        List with the name of each sample location to be plotted.
    compounds : list
        List with the name of each compound to be plotted.
    normalize : bool
        Flag that normalizes the data to the input concentration.
    **kwargs : 
        Keyword arguments to be passed to df.plot()

    Returns
    -------
    ax : Line plot of requested parameters.

    """
    plot_frame_list = []
    for i in range(len(dataframe_list)):
        dataframe = dataframe_list[i]
        plot_frame = dataframe.drop(columns = "unit", axis=0)
    
        # Influent is the same for each wetland, thus divide by it to normalize data.
        if normalize:
            plot_frame = plot_frame.div(plot_frame["INF"], axis = 0)
        
        try:
            plot_frame = plot_frame.loc[compound]
            
            # Keep information of units of plotted compounds
            unit = dataframe["unit"].loc[compound]
        
            plot_frame_list.append(plot_frame)
        except:
            plot_frame_list.append("none")
        
    
    plt.rcParams["figure.dpi"] = 300
    for i in range(len(plot_frame_list)):
        df = plot_frame_list[i]
        if not isinstance(df, str):
            plt.plot(df[location_dictionary[location]], label = f"ronde {i}", color = palette[i], marker = "o")
        
    if normalize:
        plt.ylabel("C/C0")
    else:
        plt.ylabel(f"Concentratie [{unit}]")
        
    plt.xlabel("Meetlocaties")
    
    plt.title(f"{compound} concentraties in {location}")
    
    plt.legend()
    
node_dictionary = {
    "CW1_20cm" : ["1-1", "2-1", "3-1", "4-1"],
    "CW1_40cm" : ["1-2", "2-2", "3-2", "4-2"],
    "CW1_60cm" : ["1-3", "2-3", "3-3", "4-3"],
    "CW1_80cm" : ["1-4", "2-4", "3-4", "4-4"],
    "CW2_20cm" : ["5-1", "6-1", "7-1", "8-1"],
    "CW2_40cm" : ["5-2", "6-2", "7-2", "8-2"],
    "CW2_60cm" : ["5-3", "6-3", "7-3", "8-3"],
    "CW2_80cm" : ["5-4", "6-4", "7-4", "8-4"],
    "CW3_20cm" : ["9-1", "10-1", "11-1", "12-1"],
    "CW3_40cm" : ["9-2", "10-2", "11-2", "12-2"],
    "CW3_60cm" : ["9-3", "10-3", "11-3", "12-3"],
    "CW3_80cm" : ["9-4", "10-4", "11-4", "12-4"]
    }

node_dictionary_2 = {
    "CW1_20cm" : ["CW1S1-1", "CW1S2-1", "CW1S3-1", "CW1S4-1"],
    "CW1_40cm" : ["CW1S1-2", "CW1S2-2", "CW1S3-2", "CW1S4-2"],
    "CW1_60cm" : ["CW1S1-3", "CW1S2-3", "CW1S3-3", "CW1S4-3"],
    "CW1_80cm" : ["CW1S1-4", "CW1S2-4", "CW1S3-4", "CW1S4-4"],
    "CW2_20cm" : ["CW2S1-1", "CW2S2-1", "CW2S3-1", "CW2S4-1"],
    "CW2_40cm" : ["CW2S1-2", "CW2S2-2", "CW2S3-2", "CW2S4-2"],
    "CW2_60cm" : ["CW2S1-3", "CW2S2-3", "CW2S3-3", "CW2S4-3"],
    "CW2_80cm" : ["CW2S1-4", "CW2S2-4", "CW2S3-4", "CW2S4-4"],
    "CW3_20cm" : ["CW3S1-1", "CW3S2-1", "CW3S3-1", "CW3S4-1"],
    "CW3_40cm" : ["CW3S1-2", "CW3S2-2", "CW3S3-2", "CW3S4-2"],
    "CW3_60cm" : ["CW3S1-3", "CW3S2-3", "CW3S3-3", "CW3S4-3"],
    "CW3_80cm" : ["CW3S1-4", "CW3S2-4", "CW3S3-4", "CW3S4-4"]
    }
    

location_dictionary = {
    "CW1_shallow" : ["INF", "CW1MF01", "CW1MF05", "CW1MF09", "CW1_EFF"],
    "CW1_deep"    : ["INF", "CW1MF02", "CW1MF06", "CW1MF10", "CW1_EFF"],
    "CW2_shallow" : ["INF", "CW2MF01", "CW2MF05", "CW2MF09", "CW2_EFF"],
    "CW2_deep"    : ["INF", "CW2MF02", "CW2MF06", "CW2MF10", "CW2_EFF"],
    "CW3_shallow" : ["INF", "CW3MF01", "CW3MF05", "CW3MF09", "CW3_EFF"],
    "CW3_deep"    : ["INF", "CW3MF02", "CW3MF06", "CW3MF10", "CW3_EFF"],
    "CW1_ondiep" : ["INF", "CW1MF01", "CW1MF05", "CW1MF09", "CW1_EFF"],
    "CW1_diep"    : ["INF", "CW1MF02", "CW1MF06", "CW1MF10", "CW1_EFF"],
    "CW2_ondiep" : ["INF", "CW2MF01", "CW2MF05", "CW2MF09", "CW2_EFF"],
    "CW2_diep"    : ["INF", "CW2MF02", "CW2MF06", "CW2MF10", "CW2_EFF"],
    "CW3_ondiep" : ["INF", "CW3MF01", "CW3MF05", "CW3MF09", "CW3_EFF"],
    "CW3_diep"    : ["INF", "CW3MF02", "CW3MF06", "CW3MF10", "CW3_EFF"],
    }

location_combi_dictionary = {
    "CW1_shallow" : ["INF", "CW1MF01", "CW1MF03", "CW1MF05", "CW1MF09", "CW1MF11", "CW1_EFF"],
    "CW1_deep"    : ["INF", "CW1MF02", "CW1MF04", "CW1MF06", "CW1MF10", "CW1MF12", "CW1_EFF"],
    "CW2_shallow" : ["INF", "CW2MF01", "CW2MF03", "CW2MF05", "CW2MF09", "CW2MF11", "CW2_EFF"],
    "CW2_deep"    : ["INF", "CW2MF02", "CW2MF04", "CW2MF06", "CW2MF10", "CW2MF12", "CW2_EFF"],
    "CW3_shallow" : ["INF", "CW3MF01", "CW3MF03", "CW3MF05", "CW3MF09", "CW3MF11", "CW3_EFF"],
    "CW3_deep"    : ["INF", "CW3MF02", "CW3MF04", "CW3MF06", "CW3MF10", "CW3MF12", "CW3_EFF"]
    }



