# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:45:13 2025

@author: Jorrit Bakker
"""

import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def cleanup_redox(file_path : str,
                  correction : float = 200,
                  rename : dict = None,
                  ):
    """ Takes an Excel sheet of SWAP sensor data and seperates it into two 
    dataframes for redox and temperature that can be used for data analysis.

    Parameters
    ----------
    file_path : str
        Path to excel or csv file containing redox data.
    correction : float, optional
        The correction factor with regards to 3M KCl electrode reference for the redox data. Default is 200
    rename : dictionary, optional
        Dictionary for renaming the SWAP nodes. With initial name as key and new name as value. Default is none.

    Returns
    -------
    df_redox : pd.Dataframe
        A cleaned up dataframe containing the redox data from the input Excel sheet.
    df_temp : pd.Dataframe
        A cleaned up dataframe containing the soil temperature data from the input Excel sheet.
    """
    
    # Handle both Excel files and .csv (or .dat) files as input
    if file_path.endswith("xlsx") or file_path.endswith("xls"):
        dataframe = pd.read_excel(file_path, sheet_name = 0)
    else:
        try:
            dataframe = pd.read_csv(file_path, skiprows = [0], header = None)
        except:
            IOError("File type is not of the expected type or recognized. File should be a csv or Excel")
    
    drop_cols = ['batt_volt_Avg', 'RECORD', 'TIMESTAMP']
    
    # Locate the row containing sensor names and change column headers
    header = dataframe[dataframe.iloc[:,0] == "TIMESTAMP"].index[0]
    dataframe.columns = dataframe.iloc[header]
    # Locate the row where redox data starts, to remove any unnecessary rows above
    start_data = dataframe[dataframe.loc[:,"RECORD"] == "0"].index[0]
    dataframe = dataframe.drop(range(0,start_data))
    
    # Time column is set to datatime datatype and moved to first column of dataframe for ease of reading.
    dataframe['Time'] = pd.to_datetime(dataframe['TIMESTAMP'])
    move_col = dataframe.pop("Time")
    dataframe.insert(0, "Time", move_col)
    # Remove irrelevant columns
    dataframe = dataframe.drop(drop_cols, axis = 1)
    
    # Split dataframe into redox and temperature by selecting on the beginning of the column names.
    df_redox = dataframe.filter(regex='^redox')
    df_redox = pd.concat([dataframe['Time'], df_redox], axis = 1)
    df_temp = dataframe.filter(regex='^temp')
    df_temp = pd.concat([dataframe['Time'], df_temp], axis = 1)
    
    # Column names are changed to more concise names for ease of understanding.
    # Renaming dictionaries are located at the bottom of this script and can be passed to this function.
    if rename:
        df_redox.rename(columns = rename, inplace = True)
        df_temp.rename(columns = rename, inplace = True)
    
    # Set dataframe index to the date-time column for ease of indexing.
    df_redox = df_redox.set_index("Time")
    df_temp = df_temp.set_index("Time")
    # Set datatype to numerical for plotting and data analysis.
    df_redox = df_redox.apply(pd.to_numeric, errors='coerce') + correction
    df_temp = df_temp.apply(pd.to_numeric, errors='coerce')
    
    # Hourly data range from beginning to end date of dataframe, to include missing timeframe.
    date_range_redox = pd.date_range(df_redox.index[0], df_redox.index[-1], freq = "h")
    date_range_temp = pd.date_range(df_temp.index[0], df_temp.index[-1], freq = "h")
    
    # Fill any missing time with NaN values, to clarify which parts of data are missing.
    df_redox = df_redox.reindex(date_range_redox, fill_value=np.nan)
    df_temp = df_temp.reindex(date_range_temp, fill_value=np.nan)

    return(df_redox, df_temp)

# def plot_redox(df_redox : pd.DataFrame(),
#                redox_nodes : list,
#                start_date : str,
#                end_date : str,
#                ylimit : tuple = None,
#                ax = None,
#                **kwargs
#                ):
#     """ Plot redox potential and optionally rainfall data for selected nodes in a timeframe.
    

#     Parameters
#     ----------
#     df_redox : pd.DataFrame
#         Dataframe with SWAP redox data
#     redox_nodes : List
#         List with nodes from the dataframe to be plotted
#     start_date : str
#         The start date of the data to be plotted, as "YYYY-MM-DD"
#     end_date : str
#         The end date of the data to be plotted, as "YYYY-MM-DD"
#     ylimit_redox : tuple, optional
#         Manually set y-axis range for the redox data, as (min_y, max_y). The default is None.
#     ax : obj, optional
#         Axes object of matplotlib, specify when adding this to a pre-exisiting plot object. Default is None.
#     **kwargs :
#         Keyword arguments for plt.plot()

#     Returns
#     -------
#     fig : obj
#         Figure object of matplotlib
#     ax : obj
#         Axes object of matplotlib
#     """
    
#     # Select date range of data
#     mask = (df_redox.index > start_date) & (df_redox.index <= end_date)
#     df_redox_plot = df_redox[mask]
    
#     # Detect if an axis object is passed to the function, so data will be plotted to the right axis.
#     if ax is None:
#         fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
#     else:
#         fig = None
    
#     # Plot redox potential measured for every input node
#     for i, node in enumerate(redox_nodes):
#         ax.plot(df_redox_plot.index, df_redox_plot[node],
#                 label = node,
#                 **kwargs)

#     ax.set_xlabel("Time", fontsize=9)
#     ax.set_ylabel("Redox potential [mV]", fontsize=9)
    
#     # try-except structure to handle ylimits of wrong format
#     if ylimit:
#         try:
#             ax.set_ylim(ylimit)
#         except:
#             print("ylimits_redox is not of the correct format and is thus ignored.")
    
#     ax.set_xlabel('Date', fontsize=9)
#     ax.set_ylabel(r'Redox potential [$mV$]', fontsize=9)
    
#     # Modify axis ticks with the goal to make it more readable.
#     ax.xaxis.set_major_locator(mdates.MonthLocator())
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
#     ax.tick_params(axis='x', rotation=0, pad=15, labelsize=7)

#     ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
#     ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
#     ax.tick_params(axis='x', which='minor', length=4, width=1, labelsize=7)
    
#     # When part of pre-exisiting figure, only ax needs to be returned, otherwise, fig is generated inside this function so it has to be returned as well.
#     if fig is None:
#         return(ax)
#     else:
#         fig.tight_layout() 
#         return(fig, ax)
    
#     return(fig, ax)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter

def plot_redox(df_redox: pd.DataFrame,
               redox_nodes: list,
               start_date: str,
               end_date: str,
               ylimit: tuple = None,
               ax=None,
               **kwargs
               ):
    """ Plot redox potential for selected nodes in a timeframe, with auto‐formatted dates.
    """
    # Filter to the requested date range
    mask = (df_redox.index > start_date) & (df_redox.index <= end_date)
    df_redox_plot = df_redox[mask]

    # Create new figure/axes if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6), dpi=300,
                               constrained_layout=False)  # we'll do tight_layout later
    else:
        fig = None

    # Plot each node
    for node in redox_nodes:
        ax.plot(df_redox_plot.index, df_redox_plot[node],
                label=node, **kwargs)

    # Axis labels (with a bit more size & padding)
    ax.set_xlabel('Date', fontsize=10, labelpad=6)
    ax.set_ylabel(r'Redox potential [$mV$]', fontsize=10, labelpad=6)

    # Optional y‐limits
    if ylimit:
        try:
            ax.set_ylim(ylimit)
        except Exception:
            print("ylimit format error; ignoring.")

    # --- AUTO DATE LOCATOR & FORMATTER ---
    locator = AutoDateLocator(minticks=4, maxticks=7)
    formatter = ConciseDateFormatter(locator)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # Tweak tick appearance
    ax.tick_params(axis='x', which='major',
                   rotation=25, labelsize=8, pad=6)
    ax.tick_params(axis='y', labelsize=8)

    # Final layout adjustments
    if fig is not None:
        fig.tight_layout()
        return fig, ax
    else:
        return ax


# def plot_temp(df_temp : pd.DataFrame(),
#               temp_nodes : list,
#               start_date : str,
#               end_date : str,
#               mean : bool = False,
#               ylimit : tuple = None,
#               ax = None,
#               **kwargs
#               ):
#     """ Plot temperature for a selection of nodes in a specified timeframe.
    

#     Parameters
#     ----------
#     df_temp : pd.DataFrame
#         Dataframe with temperature data
#     temp_nodes : List
#         List with nodes from the dataframe to be plotted
#     start_date : str
#         The start date of the data to be plotted, as "YYYY-MM-DD"
#     end_date : str
#         The end date of the data to be plotted, as "YYYY-MM-DD"
#     mean : Bool, optional
#         When set to True, plots the mean soil temperature of the given nodes. The default is False.
#     ylimit : tuple, optional
#         Manually set y-axis range for the redox data, as (min_y, max_y). The default is False.
#     ax : obj, optional
#         Axes object of matplotlib, specify when adding this to a pre-exisiting plot. Default is None.
#     **kwargs :
#         Keyword arguments for plt.plot()

#     Returns
#     -------
#     fig : obj
#         Figure object of matplotlib
#     ax : obj
#         Axes object of matplotlib

#     """
    
#     # Select date range of data
#     mask = (df_temp.index > start_date) & (df_temp.index <= end_date)
#     df_temp = df_temp[mask]
    
#     # When plotting temperature and redox together, it is more clear to use the mean temperature.
#     if mean:
#         mean_temp = df_temp.loc[:,temp_nodes].mean(axis=1)
#         df_temp['mean_temperature'] = mean_temp
    
#     # Detect if an axis object is passed to the function, so data will be plotted to the right axis.
#     if ax is None:
#         fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
#     else:
#         fig = None
    
#     # Plotting parameters are different when plotting the mean temperature versus every temperature node.
#     if mean:
#             ax.plot(df_temp.index, df_temp["mean_temperature"],
#                     label = "Mean temperature",
#                     **kwargs
#                     )
#     else:
#         for i, node in enumerate(temp_nodes):
#             ax.plot(df_temp.index, df_temp[node],
#                     label = node,
#                     **kwargs
#                     )
    
#     # try-except structure to handle ylimits of wrong format
#     if ylimit:
#         try:
#             ax.set_ylim(ylimit)
#         except:
#             print("ylimits is not of the correct format and is thus ignored.")
            
#     ax.set_xlabel('Date', fontsize=9)
#     ax.set_ylabel('Temperature (ºC)', fontsize=9)

#     # Modify axis ticks to make it more readable.    
#     ax.xaxis.set_major_locator(mdates.MonthLocator())
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
#     ax.tick_params(axis='x', rotation=0, pad=15, labelsize=7)

#     ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
#     ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
#     ax.tick_params(axis='x', which='minor', length=4, width=1, labelsize=7)
    
#     # When part of pre-exisiting figure, only ax needs to be returned, otherwise, fig is generated inside this function so it has to be returned as well.
#     if fig is None:
#         return(ax)
#     else:
#         fig.tight_layout() 
#         return(fig, ax)


def plot_temp(df_temp: pd.DataFrame,
              temp_nodes: list,
              start_date: str,
              end_date: str,
              mean: bool = False,
              ylimit: tuple = None,
              ax=None,
              **kwargs
              ):
    """ Plot temperature for a selection of nodes in a specified timeframe,
        with automatic date‐tick spacing and formatting.
    """
    # --- Filter to the requested date range (unchanged) ---
    mask = (df_temp.index > start_date) & (df_temp.index <= end_date)
    df_temp_plot = df_temp[mask]

    # --- Calculate mean if requested (unchanged) ---
    if mean:
        df_temp_plot['mean_temperature'] = (
            df_temp_plot[temp_nodes].mean(axis=1)
        )

    # --- Create new figure/axes if needed (fontsize & layout tweaked) ---
    if ax is None:
        fig, ax = plt.subplots(
            figsize=(8, 6),
            dpi=300,
            constrained_layout=False         # ◀◀ MODIFIED: we'll tight_layout() later
        )
    else:
        fig = None

    # --- Plotting (unchanged) ---
    if mean:
        ax.plot(df_temp_plot.index,
                df_temp_plot['mean_temperature'],
                label='Mean temperature',
                **kwargs)
    else:
        for node in temp_nodes:
            ax.plot(df_temp_plot.index,
                    df_temp_plot[node],
                    label=node,
                    **kwargs)

    # --- Y‐limits (unchanged) ---
    if ylimit:
        try:
            ax.set_ylim(ylimit)
        except Exception:
            print("ylimit format error; ignoring.")

    # --- Axis labels (font size & padding tweaked) ---
    ax.set_xlabel('Date', fontsize=10, labelpad=6)           # ◀◀ MODIFIED
    ax.set_ylabel('Temperature (ºC)', fontsize=10, labelpad=6)  # ◀◀ MODIFIED

    # --- AUTO DATE LOCATOR & CONCISE FORMATTER (NEW) ---
    locator = AutoDateLocator(minticks=4, maxticks=7)         # ◀◀ MODIFIED
    formatter = ConciseDateFormatter(locator)                 # ◀◀ MODIFIED

    ax.xaxis.set_major_locator(locator)                       # ◀◀ MODIFIED
    ax.xaxis.set_major_formatter(formatter)                   # ◀◀ MODIFIED

    # --- Tweak tick appearance (font sizes & rotation) ---
    ax.tick_params(axis='x', which='major',
                   rotation=25, labelsize=8, pad=6)           # ◀◀ MODIFIED
    ax.tick_params(axis='y', labelsize=8)                     # ◀◀ MODIFIED

    # --- Final layout adjustments (unchanged) ---
    if fig is not None:
        fig.tight_layout()                                     # keep this to avoid clipping
        return fig, ax
    else:
        return ax


# Dictionary which renames each soil node for the Constructed Wetland pilot study
CW_rename = {
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

# Dictionary with nodes for each wetland and depth in the Constructed Wetland pilot study
node_dictionary = {
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
