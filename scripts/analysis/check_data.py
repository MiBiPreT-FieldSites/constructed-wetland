#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions for data handling and standardization.

@author: Alraune Zech
"""
import numpy as np
import pandas as pd
import mibiscreen.data.names_data as names
from mibiscreen.data.unit_settings import all_units
from mibiscreen.data.unit_settings import standard_units
from mibiscreen.data.unit_settings import units_env_cond

to_replace_list = ["-",'--','',' ','  ']
to_replace_value = np.nan

def standard_names(name_list,
                   standardize = True,
                   reduce = False,
                   verbose = False,
                   ):
    """Function transforming list of names to standard names.

    Function that looks at the names (of e.g. environmental variables, contaminants,
    metabolites, isotopes, etc) and provides the corresponding standard names.

    Args:
    -------
        name_list: string or list of strings
            names of quantities to be transformed to standard
        standardize: Boolean, default False
            Whether to standardize identified column names
        reduce: Boolean, default False
            Whether to reduce data to known quantities
        verbose: Boolean, default True
            verbosity flag

    Returns:
    -------
        tuple: three list containing names of
                list with identitied quantities in data (but not standardized names)
                list with unknown quantities in data (not in list of standardized names)
                list with standard names of identified quantities

    Raises:
    -------
    None (yet).

    Example:
    -------
    Todo's:
        - complete list of potential contaminants, environmental factors
        - add name check for metabolites?
    """
    names_standard = []
    names_known = []
    names_unknown = []
    names_transform = {}

    dict_names = names.col_dict.copy()

    if isinstance(name_list, str):
        name_list = [name_list]
    elif isinstance(name_list, list):
        for name in name_list:
            if not isinstance(name, str):
                raise ValueError("Entry in provided list of names is not a string:", name)

    for x in name_list:
        y = dict_names.get(x, False)
        x_isotope = x.split('-')[0]
        y_isotopes = names.names_isotopes.get(x_isotope.lower(), False)

        if y_isotopes is not False:
            x_molecule = x.removeprefix(x_isotope+'-')
            y_molecule = names.names_contaminants.get(x_molecule.lower(), False)
            if y_molecule is False:
                names_unknown.append(x)
            else:
                y = y_isotopes+'-'+y_molecule
                names_known.append(x)
                names_standard.append(y)
                names_transform[x] = y
        else:
            y = dict_names.get(x.lower(), False)
            if y is False:
                names_unknown.append(x)
            else:
                names_known.append(x)
                names_standard.append(y)
                names_transform[x] = y

    if verbose:
        print('================================================================')
        print(" Running function 'standard_names()'")
        print('================================================================')
        print("{} of {} quantities identified in name list.".format(len(names_known),len(name_list)))
        print("List of names with standard names:")
        print('----------------------------------')
        for i,name in enumerate(names_known):
            print(name," --> ",names_standard[i])
        print('----------------------------------')
        if standardize:
            print("Identified column names have been standardized")
        else:
            print("\nRenaming can be done by setting keyword 'standardize' to True.\n")
        print('________________________________________________________________')
        print("{} quantities have not been identified in provided data:".format(len(names_unknown)))
        print('---------------------------------------------------------')
        for i,name in enumerate(names_unknown):
            print(name)
        print('---------------------------------------------------------')
        if reduce:
            print("Not identified quantities have been removed from data frame")
        else:
            print("\nReduction to known quantities can be done by setting keyword 'reduce' to True.\n")
        print('================================================================')

    if standardize:
        if reduce:
            return names_standard
        else:
            return names_standard + names_unknown
    else:
        return (names_standard, names_known, names_unknown, names_transform)

def check_data_frame(data_frame,
                     sample_name_to_index = False,
                     inplace = False,
                     ):
    """Checking data on correct format.

    Tests if provided data is a pandas data frame and provides column names.
    Optionally it sets the sample name as index.

    Input
    -----
        data_frame: pd.DataFrame
            quantities for data analysis given per sample
        sample_name_to_index:  Boolean, default False
            Whether to set the sample name to the index of the DataFrame
        inplace: Boolean, default False
            Whether to modify the DataFrame rather than creating a new one.

    Output
    ------
        data: pd.DataFrame
            copy of given dataframe with index set to sample name
        cols: list
            List of column names
    """
    if not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Data has to be a panda-DataFrame or Series \
                          but is given as type {}".format(type(data_frame)))

    if inplace is False:
        data = data_frame.copy()
    else:
        data = data_frame

    if sample_name_to_index:
        if names.name_sample not in data.columns:
            print("Warning: No sample name provided for making index. Consider standardizing data first")
        else:
            data.set_index(names.name_sample,inplace = True)

    if isinstance(data, pd.Series):
        cols = [data.name]
    else:
        cols = data.columns.to_list()

    return data, cols


def check_columns(data_frame,
                  standardize = False,
                  reduce = False,
                  verbose = True):
    """Function checking names of columns of data frame.

    Function that looks at the column names and links it to standard names.
    Optionally, it renames identified column names to the standard names of the model.

    Args:
    -------
        data_frame: pd.DataFrame
            dataframe with the measurements
        standardize: Boolean, default False
            Whether to standardize identified column names
        reduce: Boolean, default False
            Whether to reduce data to known quantities
        verbose: Boolean, default True
            verbosity flag

    Returns:
    -------
        tuple: three list containing names of
                list with identitied quantities in data (but not standardized names)
                list with unknown quantities in data (not in list of standardized names)
                list with standard names of identified quantities

    Raises:
    -------
    None (yet).

    Example:
    -------
    Todo's:
        - complete list of potential contaminants, environmental factors
        - add name check for metabolites?
    """
    if verbose:
        print('==============================================================')
        print(" Running function 'check_columns()' on data")
        print('==============================================================')

    data,cols= check_data_frame(data_frame,
                                sample_name_to_index = False,
                                inplace = True)

    results = standard_names(cols,
                             standardize = False,
                             reduce = False,
                             verbose = False,
                             )

    column_names_standard = results[0]
    column_names_known = results[1]
    column_names_unknown = results[2]
    column_names_transform = results[3]

    if standardize:
        data.columns = [column_names_transform.get(x, x) for x in data.columns]

    if reduce:
        data.drop(labels = column_names_unknown,axis = 1,inplace=True)

    if verbose:
        print("{} quantities identified in provided data.".format(len(column_names_known)))
        print("List of names with standard names:")
        print('----------------------------------')
        for i,name in enumerate(column_names_known):
            print(name," --> ",column_names_standard[i])
        print('----------------------------------')
        if standardize:
            print("Identified column names have been standardized")
        else:
            print("\nRenaming can be done by setting keyword 'standardize' to True.\n")
        print('________________________________________________________________')
        print("{} quantities have not been identified in provided data:".format(len(column_names_unknown)))
        print('---------------------------------------------------------')
        for i,name in enumerate(column_names_unknown):
            print(name)
        print('---------------------------------------------------------')
        if reduce:
            print("Not identified quantities have been removed from data frame")
        else:
            print("\nReduction to known quantities can be done by setting keyword 'reduce' to True.\n")
        print('================================================================')

    return (column_names_known,column_names_unknown,column_names_standard)

def check_units(data,
                verbose = True):
    """Function to check the units of the measurements.

    Args:
    -------
        data: pandas.DataFrames
            dataframe with the measurements where first row contains
            the units or a dataframe with only the column names and units
        verbose: Boolean
            verbose statement (default True)

    Returns:
    -------
        col_check_list: list
            quantities whose units need checking/correction

    Raises:
    -------
        None (yet).

    Example:
    -------
        To be added.
    """
    if verbose:
        print('================================================================')
        print(" Running function 'check_units()' on data")
        print('================================================================')

    if not isinstance(data, pd.DataFrame):
        raise ValueError("Provided data is not a data frame.")
    elif data.shape[0]>1:
        units = data.drop(labels = np.arange(1,data.shape[0]))
    else:
        units = data.copy()

    units_in_data = set(map(lambda x: str(x).lower(), units.iloc[0,:].values))
    ### testing if provided data frame contains any unit
    test_unit = False
    for u in all_units:
        if u in units_in_data:
            test_unit = True
            break
    if not test_unit:
        raise ValueError("Error: The second line in the dataframe is supposed\
                         to specify the units. No units were detected in this\
                         line, check https://mibipret.github.io/mibiscreen/ Data\
                         documentation.")

    # standardize column names (as it might not has happened for data yet)
    check_columns(units,standardize = True, verbose = False)
    col_check_list= []

    for quantity in units.columns:
        if quantity in names.chemical_composition:
            if str(units[quantity][0]).lower() not in standard_units['mgperl']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be milligramm per liter (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['mgperl'][0]))

        if quantity in names.contaminants['all_cont']:
            if str(units[quantity][0]).lower() not in standard_units['microgperl']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be microgramm per liter (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['microgperl'][0]))

        if quantity in list(units_env_cond.keys()):
            unit_type = units_env_cond[quantity]
            if str(units[quantity][0]).lower() not in standard_units[unit_type]:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be in {} (e.g. {}).".format(
                            quantity,units[quantity][0],unit_type,standard_units[unit_type][0]))

        if quantity.split('-')[0] in names.isotopes:
            if str(units[quantity][0]).lower() not in standard_units['permil']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be per mille (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['permil'][0]))

        if quantity in names.metabolites:
            if str(units[quantity][0]).lower() not in standard_units['microgperl']:
                col_check_list.append(quantity)
                if verbose:
                    print("Warning: Check unit of {}!\n Given in {}, but must be microgramm per liter (e.g. {})."
                              .format(quantity,units[quantity][0],standard_units['microgperl'][0]))

    if verbose:
        print('________________________________________________________________')
        if len(col_check_list) == 0:
            print(" All identified quantities given in requested units.")
        else:
            print(" All other identified quantities given in requested units.")
        print('================================================================')

    return col_check_list

def check_values(data_frame,
                 inplace = False,
                 verbose = True,
                 ):
    """Function that checks on value types and replaces non-measured values.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements (without first row of units)
        inplace: Boolean, default False
            Whether to modify the DataFrame rather than creating a new one.
        verbose: Boolean
            verbose statement (default True)

    Returns:
    -------
        data_pure: pandas.DataFrame
            Tabular data with standard column names and without units

    Raises:
    -------
        None (yet).

    Example:
    -------
        To be added.
    """
    if verbose:
        print('================================================================')
        print(" Running function 'check_values()' on data")
        print('================================================================')

    data,cols= check_data_frame(data_frame, inplace = inplace)

    ### testing if provided data frame contains first row with units
    for u in data.iloc[0].to_list():
        if u in all_units:
            print("WARNING: First row identified as units, has been removed for value check")
            print('________________________________________________________________')
            data.drop(labels = 0,inplace = True)
            break

    for sign in to_replace_list:
        data.iloc[:,:] = data.iloc[:,:].replace(to_replace=sign, value=to_replace_value)

    # standardize column names (as it might not has happened for data yet)
    # check_columns(data,
    #               standardize = True,
    #               check_metabolites=True,
    #               verbose = False)

    # transform data to numeric values
    quantities_transformed = []
    for quantity in cols: #data.columns:
        try:
            # data_pure.loc[:,quantity] = pd.to_numeric(data_pure.loc[:,quantity])
            data[quantity] = pd.to_numeric(data[quantity])
            quantities_transformed.append(quantity)
        except ValueError:
            print("WARNING: Cound not transform '{}' to numerical values".format(quantity))
            print('________________________________________________________________')
    if verbose:
        print("Quantities with values transformed to numerical (int/float):")
        print('-----------------------------------------------------------')
        for name in quantities_transformed:
            print(name)
        print('================================================================')

    return data

def standardize(data_frame,
                reduce = True,
                store_csv = False,
                verbose=True,
                ):
    """Function providing condensed data frame with standardized names.

    Function is checking names of columns and renames columns,
    condenses data to identified column names, checks units and  names
    sof data frame.

    Function that looks at the column names and renames the columns to
    the standard names of the model.

    Args:
    -------
        data_frame: pandas.DataFrames
            dataframe with the measurements
        check_metabolites: Boolean, default False
            whether to check on metabolites' values
        reduce: Boolean, default True
            whether to reduce data to known quantities (default True),
            otherwise full dataframe with renamed columns (for those identifyable) is returned
        store_csv: Boolean, default False
            whether to save dataframe in standard format to csv-file
        verbose: Boolean, default True
            verbose statement

    Returns:
    -------
        data_numeric, units: pandas.DataFrames
            Tabular data with standardized column names, values in numerics etc
            and table with units for standardized column names

    Raises:
    -------
        None (yet).

    Example:
    -------
    Todo's:
        - complete list of potential contaminants, environmental factors
        - add name check for metabolites?
        - add key-word to specify which data to extract
            (i.e. data columns to return)

    """
    if verbose:
        print('================================================================')
        print(" Running function 'standardize()' on data")
        print('================================================================')
        print(' Function performing check of data including:')
        print('  * check of column names and standardizing them.')
        print('  * check of units and outlining which to adapt.')
        print('  * check of values, replacing empty values by nan \n    and making them numeric')

    data,cols= check_data_frame(data_frame,
                                sample_name_to_index = False,
                                inplace = False)

    # general column check & standardize column names
    check_columns(data,
                  standardize = True,
                  reduce = reduce,
                  verbose = verbose)

    # general unit check
    units = data.drop(labels = np.arange(1,data.shape[0]))
    col_check_list = check_units(units,
                                 verbose = verbose)

    # transform data to numeric values
    data_numeric = check_values(data.drop(labels = 0),
                                inplace = False,
                                verbose = verbose)

    # store standard data to file
    if store_csv:
        if len(col_check_list) != 0:
            print('________________________________________________________________')
            print("Data could not be saved because not all identified \n quantities are given in requested units.")
        else:
            try:
                data.to_csv(store_csv,index=False)
                if verbose:
                    print('________________________________________________________________')
                    print("Save standardized dataframe to file:\n", store_csv)
            except OSError:
                print("WARNING: data could not be saved. Check provided file path and name: {}".format(store_csv))
    if verbose:
        print('================================================================')

    return data_numeric, units
