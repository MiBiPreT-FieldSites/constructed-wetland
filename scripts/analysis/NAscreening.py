import mibiscreen as mbs
from IPython.display import display

file_path = "../../data/preprocessed/na_screening/cw_T4_preprocessed.csv"
data_raw,units = mbs.load_csv(file_path, verbose = True)

data,units = mbs.standardize(data_raw,reduce = True, verbose = True)

tot_redct = mbs.reductors(data, verbose = True, ea_group = "ONS")

tot_oxi = mbs.oxidators(data, verbose = True, contaminant_group="BTEX")

e_bal = mbs.electron_balance(data, verbose=True)

na_traffic = mbs.sample_NA_traffic(data,verbose = True)

tot_cont = mbs.total_contaminant_concentration(data, verbose = True, contaminant_group="BTEX")

na_interventation = mbs.thresholds_for_intervention(data, verbose=True, contaminant_group="BTEX")

data_na = mbs.sample_NA_screening(data)
display(data_na)