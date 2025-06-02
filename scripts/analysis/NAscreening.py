
import mibiscreen.analysis.sample.screening_NA as na
from mibiscreen.data.check_data import standardize
from mibiscreen.data.load_data import load_csv
from IPython.display import display

time_point = "4"
file_path = f"../../data/preprocessed/na_screening/cw_T{time_point}_preprocessed.csv"

data_raw,units = load_csv(file_path, verbose = True)

data,units = standardize(data_raw,reduce = True, verbose = True)

tot_redct = na.reductors(data, verbose = True, ea_group = "ONS")

tot_oxi = na.oxidators(data, verbose = True, contaminant_group="BTEX")

e_bal = na.electron_balance(data, verbose=True)

na_traffic = na.NA_traffic(data,verbose = True)

tot_cont = na.total_contaminant_concentration(data, verbose = True, contaminant_group="BTEX")

na_interventation = na.thresholds_for_intervention(data, verbose=True, contaminant_group="BTEX")

data_na = na.screening_NA(data)
#display(data_na)

data_na.to_excel(f"../../results/na_screening_result_T{time_point}.xlsx", index=False)