# Preprocessing for NA-Screening Analysis

*This document outlines the steps performed by the `extract_contaminants` function in **data_preprocessing_na.py** to prepare standardized CW data for NA-screening analysis.*

**Function location:** [data_preprocessing_na.py](..\..\scripts\data\data_preprocessing_na.py)

## Table of Contents

1. [Overview](#overview)  
2. [Prerequisites](#prerequisites)  
3. [Function Reference](#function-reference)  
4. [Data Extraction Steps](#data-extraction-steps)  
5. [Manual Post-Processing](#manual-post-processing)  
6. [Example Workflow](#example-workflow)  

---

## Overview

The `extract_contaminants` function takes a cleaned, standardized Excel file and produces a tailored DataFrame for NA-screening by selecting only relevant contaminant columns, inserting a unique coding column, and optionally converting measurement values to integers.

## Prerequisites

- Python 3.x  
- pandas library  

Ensure you have **preprocessing.py** in your project; update the link above if necessary.

## Function Reference

- **Function name:** `extract_contaminants`  
- **Location:** [data_preprocessing_na.py](..\..\scripts\data\data_preprocessing_na.py)  
- **Purpose:** Load a standardized dataset, filter for contaminants of interest, add a coding column, and convert measurement data to the required format for NA-screening.

## Data Extraction Steps

1. **Load standardized data:** Read the Excel file where the first row contains column headers (parameter names) and the second row indicates units.  
2. **Select contaminants:** Keep only the “Well name” column plus those columns matching a predefined list of contaminants of interest.  
3. **Insert Coding column:**  
   - Row 0 (unit row): Coding = “unit”, Well name = “-”  
   - Subsequent rows: Generate codes of the form `NL_CW_W_##` (round T0) or `NL_CW_W_T#_##` for other rounds.  
4. **Convert to integers:** Optionally cast selected numeric columns (excluding the unit row) to integer type.

## Manual Post-Processing

After running `extract_contaminants`, additional renaming is applied to align with the standard NA-screening template. These steps can be removed once the analysis code accepts these variants natively:

- **Change units:**
  - `µg/l` → `ug/l`
- **Rename columns:**  
  - `Coding` → `sample_nr`  
  - `Well name` → `obs_well`  
  - Remove the `Sample description` column entirely  
  - Rename contaminant parameters to valid NA-screening names:  
    - `(m+p)xylene` → `pm_xylene`  
    - `o-xylene` → `o_xylene`  
    - `iron(2+)` → `iron2`  
    - `manganese (II)` → `manganese`
    - `sulphate` → `sulfate`

## Example Workflow

1. Ensure raw data has been standardized via `cleanup_compound` in **standardization.py**.  
2. Run `extract_contaminants` in **preprocessing.py** with the appropriate file path, time point, and contaminant list.  
3. Apply manual post-processing renames if necessary, and save the final DataFrame for NA-screening analysis.