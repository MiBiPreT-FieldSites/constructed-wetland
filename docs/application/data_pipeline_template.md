
In the following you could read all the steps to create data pipeline for your project: 

## 1. Data Ingestion (Collection of Raw Data)
This is the first stage, where raw data is gathered from various sources and ingested into the pipeline. It can be structured as per our case (databases, CSV files, APIs, Excels).

#### Examples:
- Batch Data: importing a CSV file of site data regularly like once a day.
- API Data: Pulling real-time data streams from the API.
- Database Extraction: Replicating data from a MySQL database to our own database.


## 2. Data Preprocessing (Cleaning and Standardization)
Before analysis, raw data is often messy and inconsistent. This step ensures data quality, removes duplicates, corrects errors, and formats it for the next processes. This step can be done manually or automated by code.

### Tasks in this stage:
- Check format like the headings and units per column
- Handling missing values (e.g., filling gaps with averages)
- Data deduplication (removing repeated records)
- Converting different formats (e.g., date formats across multiple sources, unit conversion)
- Encoding Data: Create identifiers for the samples name based on their location and country
- Normalization (converting text values to lowercase, trimming spaces, etc.)

#### Examples:
- Standardizing dates from different sources (e.g., converting MM-DD-YYYY to YYYY-MM-DD)
- Convert units to SI units(e.g., pound to Kg, ft to m)
- Removing duplicate sample records from different sources
- Filtering out irrelevant data (e.g., the columns that we don't need)
- Sample name identifier example: NL_GRI_W_1

## 3. Data Transformation (Processing and Enrichment)
In this step, data is converted into a useful format, enriched with additional information, or aggregated for reporting. This step also can be done manually or automated by code.

### Common tasks in this stage:
- Joining Data: Merging datasets from multiple sources
- Data Enrichment: Calculating new values from initial data

#### Examples:
- Merging site measurments data with lab analyized data in one csv file
- Calculating isotop ratio according to Raleigh equation

## 4. Data Storage (Centralized Data Repository)
Once data is transformed, it is stored in an appropriate system depending on the use case.

### Types of Storage:
- Databases like UU YODA, MySQL
- GitHub repository

### Examples:
- Storing processed data in YODA

## 5. Data Validation & Monitoring for Each Data Analysis Module  (Quality Control)
This stage ensures that processed data is accurate, complete, and meets requirements to run different analysis.

### Common Checks:
- Schema validation (ensuring expected columns, required input data or calculated parameters exists)
- Anomaly detection (flagging unexpected values)
- Data freshness checks (ensuring updates occur within expected timeframes)

#### Examples:
- Checking if any contaminant are missing calculated isotope ratios baed on Raliegh equation exist for isoptoppe analysis. 
  - Validating all the concentration values are positive numbers.  
- Monitoring real-time streaming data for sudden spikes in API errors (if we want to recive redox data of Grift park constructed wetlan from online server)

## 6. Data Analytics & Delivery (Insights & Output)
At this stage, we extract insights from processed data, either through graphs or reports.

### Examples:
- Graph: Visualize na_analysis data as traffic lights plotted for each sample
- Graph: creat Rayleigh plots
- Reports: prepare TAUW report
- APIs that serve the processed data to other services or researchers


## End-to-End Example of the Data Pipeline
1. **Ingestion:**
```python
from mibipret.data.load_data import load_csv
from mibipret.data.load_data import load_excel

# load data from csv file
file_path = 'path/to/data/data.csv'
data_raw,units = load_csv(file_path,verbose=False)

# load data from excel file per sheet 
file_path = 'path/to/data/data.xlsx'
environment_raw,units = load_excel(file_path, sheet_name = 'environment', verbose = verbose)
```
    
2. **Preprocessing:(Cleaning and Standardization)**

```Python
from mibipret.data.check_data import standardize

# Runs all checks on data, i.e. column names (check_columns()), data format (check_data_frame()), units (check_units()), names (standard_names()) and values (check_values()) in one go and returns transformed data with standard column names and valueas in numerical type where possible. Data is reduced to those columns containing known quantities if reduce=true.
data, units = standardize(data_raw, reduce = True, verbose=False)
```

3. **Transformation:(processing and enrichment)**
```python
 # For NA screening, stochiometric equations are used to analyze electron balance, here is how to perform NA screening step by step:
 import mibipret.analysis.sample.screening_NA as na
 #Calculation of number of electrons for reduction
 #Returns pandas-Series with total amount of electron reductors per well in [mmol e-/l]:
    tot_reduct = na.reductors(data,verbose = True,ea_group = 'ONSFe')                               


#Calculation of number of electrons needed for oxidation
#Returns pandas-Series with total amount of oxidators per well in [mmol e-/l]:
    tot_oxi = na.oxidators(data,verbose = True, contaminant_group='BTEXIIN')                              


#Calculation of number of electron balance
#Returns pandas-Series with ratio of reductors to oxidators. If value below 1, available electrons for reduction are not sufficient for reaction and thus NA is potentially not taking place:
    e_bal = na.electron_balance(data,verbose = True)                               

# Evaluation of intervention threshold exceedance
#Calculation of total concentration of contaminants/specified group of contaminants
#Returns pandas-Series with total concentrations of contaminants per well in [ug/l]:
    tot_cont = na.total_contaminant_concentration(data,verbose = True,contaminant_group='BTEXIIN')                             
 
 # If you want to perform complete NA screening and evaluation of intervention threshold exceedance in one go:
 data_na = na.screening_NA(data,verbose = True)

 # It is also possible to run full NA screening with results added to data using argument (inplace = True):
 na.screening_NA(data,inplace = True,verbose = False)
```
4. **Storage:**
`Not available`

5. **Validation & Monitoring for Each Data Analysis Module**
This is intended task to do but not implemented yet.

```python
# we use the `options` function to check what types of analyses/modeling/visualization/reports we can do on the dataset
# if func argument is provided, it will check whether this function is possible and if not what else is needed
mibipret.decision_support.options(st_sample_data, func=mibipret.visualize.traffic3d)

# To perform mibipret.visualize.traffic3d you need to run mibipret.analysis.na_screening
# the workflow requires the following columns: [x,y, depth]
# Row 4-19 and 28-39 have these columns defined, you can apply the function on these rows.
```

6. **Analytics:** 
```python
# Calculation of "traffic light" based on electron balance
# Returns pandas-Series with traffic light (red/yellow/green) if NA is taking place based on electron balance. Red corresponds to a electron balance below 1 where available electrons for reduction are not sufficient and thus NA is potentially not taking place:
na_traffic = na.NA_traffic(data,verbose = True)

# Calculation of "traffic light" for threshold exceedance
# Returns pandas-DataFrame (similar to input data, including well specification) with intervention threshold exceedance analysis:
# traffic light if well requires intervention (red/yellow/green)
# number of contaminants exceeding the intervention value
# list of contaminants above the threshold of intervention
na_intervention = na.thresholds_for_intervention(data,verbose = True,contaminant_group='BTEXIIN')
display(na_intervention)

# Activity plot
from mibipret.visualize.activity import activity
# Create activity plot linking contaminant concentration to metabolite occurence based on NA screening
fig, ax = activity(data)
```
