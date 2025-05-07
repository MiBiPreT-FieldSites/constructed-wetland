import numpy as np
from scipy.special import erfc

class ADESolution:
    """
    Compute the analytical solution to the 1D ADE with linear adsorption only (no decay).
    Uses the erfc breakthrough curve solution.
    """

    def __init__(self, dispersion_length, velocity, transport_distance):
        """
        Parameters:
        - dispersion_length (α): dispersivity [m]
        - velocity (v): average linear velocity [m/day]
        - transport_distance (L): transport path length [m]
        """
        self.alpha = dispersion_length
        self.v = velocity
        self.L = transport_distance

    def erfc_solution(self, R, t):
        """
        Compute the relative concentration C/C₀ at time t for a given retardation factor R.
        Returns 0 if t = 0 to avoid divide-by-zero error.
        """
        if t <= 0:
            return 0.0
        D = self.alpha * self.v
        term = (self.L - self.v * t / R) / (2 * np.sqrt(D * t / R))
        return 0.5 * erfc(term)

    def add_to_dataframe(self, df, time_column="days", R_column="R", result_column="ADE_adsorption_only"):
        """
        Adds a new column to the DataFrame with predicted values using erfc solution.

        Parameters:
        - df: DataFrame with time and R values
        - time_column: column name for elapsed time
        - R_column: column name for retardation factor
        - result_column: name of the new output column to add
        """
        df[result_column] = df.apply(
            lambda row: self.erfc_solution(row[R_column], row[time_column]),
            axis=1
        )
        return df


