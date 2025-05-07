# config.py — Configuration for the wetland modeling system

# Paths to cleaned Excel files and their sampling dates
FILE_PATHS = [
    ("../../../data/cleaned/cw_T0_cleaned.xlsx", "2024-08-14"),
    ("../../../data/cleaned/cw_T1_cleaned.xlsx", "2024-10-23"),
    ("../../../data/cleaned/cw_T2_cleaned.xlsx", "2025-01-7"),
    ("../../../data/cleaned/cw_T3_cleaned.xlsx", "2025-02-18"),
]

# Site parameters
BULK_DENSITY = 1.43   # kg/L (estimated from media layers)
POROSITY     = 0.4   # dimensionless
FLOW_RATE    = 1   # m³/day
BULK_VOLUME  = 4.0    # m³
FOC          = 0.004   # fraction of organic carbon (e.g., 0.4%)
PORE_VOLUME  = 20 # m³

# Compound definitions: log_Kow, decay_rate (1/day), molecular_weight (g/mol)
COMPOUND_INFO = {
    "benzene":        {"log_Kow": 2.13, "decay_rate": 0.05,  "molecular_weight": 78.11},
    "toluene":        {"log_Kow": 2.73, "decay_rate": 0.03,  "molecular_weight": 92.14},
    "ethylbenzene":   {"log_Kow": 3.15, "decay_rate": 0.02,  "molecular_weight": 106.17},
    "o-xylene":       {"log_Kow": 3.12, "decay_rate": 0.02,  "molecular_weight": 106.17},
    "(m+p)-xylene":   {"log_Kow": 3.18, "decay_rate": 0.02,  "molecular_weight": 106.17},
    "naphthalene":    {"log_Kow": 3.30, "decay_rate": 0.01,  "molecular_weight": 128.17},
    "acenaphthylene": {"log_Kow": 3.94, "decay_rate": 0.005, "molecular_weight": 152.17},
    "acenaphtene":    {"log_Kow": 3.92, "decay_rate": 0.005, "molecular_weight": 154.20},
    "fluorene":       {"log_Kow": 4.18, "decay_rate": 0.003, "molecular_weight": 166.22},
    "phenanthrene":   {"log_Kow": 4.46, "decay_rate": 0.002, "molecular_weight": 178.23},
    "anthracene":     {"log_Kow": 4.45, "decay_rate": 0.001, "molecular_weight": 178.23},
}
