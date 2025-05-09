# Data Standardization and Manual Cleaning for Constructed Wetland Monitoring

*Documented standardization steps for raw field measurement data in Constructed Wetland (CW) monitoring rounds T0–T3.*

**Function location**: [data_standardization.py](..\..\scripts\data\data_standardization.py)

## Table of Contents

1. [Overview](#overview)  
2. [Prerequisites](#prerequisites)  
3. [Function Reference](#function-reference)  
4. [Manual Cleaning of Raw Data](#manual-cleaning-of-raw-data)  
   - [Round T0](#round-t0)  
     - [First sheet (Analyseresultaten)](#first-sheet-analyseresultaten)  
     - [Second sheet (Watermonstergegevens)](#second-sheet-watermonstergegevens)  
   - [Rounds T1, T2, T3](#rounds-t1-t2-t3)  
5. [Standardization Steps](#standardization-steps)  
6. [Example Workflow](#example-workflow)  

---

## Overview

This file describes how the `cleanup_compound` function in **standardization.py** takes raw Excel sheets from CW field measurements and transforms them into a consistent, analysis-ready format. It covers both manual corrections needed in specific monitoring rounds and the general sequence of standardization actions.

## Prerequisites

- Python 3.x  
- pandas library  


## Function Reference

- **Function name:** `cleanup_compound`  
- **Location:** [data_standardization.py](..\..\scripts\data\data_standardization.py)  
- **Purpose:** Load raw data, apply translations and filters, map sample codes, reorder and clean values, then output a final transposed DataFrame.

## Manual Cleaning of Raw Data

### Round T0

#### First sheet (Analyseresultaten)
- Add a new parameter `sulfid vrij`.  
- Rename `nitriet` → **nitriet-N** (unit [mgN/l]).  
- Rename `nitraat` → **nitraat-N** (unit [mgN/l]).  
- Remove `CW2_EFF-1-2` (only two measurements exist).

#### Second sheet (Watermonstergegevens)
- Correct typo: `CW2MF05-1-1` → **CW2MF05-1-2**.  
- Remove `CW2_EFF-1-2`.

### Rounds T1, T2, T3

#### First sheet (Analyseresultaten)
- Rename `nitriet` → **nitriet-N** (unit [mgN/l]).  
- Rename `nitraat` → **nitraat-N** (unit [mgN/l]).  
- Clean well names in the `Monsteromschrijving` row by keeping only the identifier inside parentheses.

## Standardization Steps

1. **Load and parse** raw Excel file (skip first header row, interpret comma decimals, set first column as identifiers).  
2. **Extract column names** from the sample description row.  
3. **Translate parameter names** from Dutch to English.  
4. **Remove non-measurement rows** (metadata and empty lines).  
5. **Map sample codes** using metadata sheet to standard CW location identifiers.  
6. **Reorder columns** for consistent sequence across datasets.  
7. **Append oxygen data** from metadata as an additional row.  
8. **Handle below-detection values** by replacing `<value` entries with zero.  
9. **Convert to numeric** and strip whitespace.  
10. **Fill missing values** with `0.0`.  
11. **Finalize units** (set placeholder for sample description).  
12. **Transpose** table for analysis-ready layout.

## Example Workflow

1. Apply manual corrections in the raw Excel files for each round.  
2. Run `cleanup_compound` in **standardization.py**.  
3. Use the resulting output for visualization or further analysis.

