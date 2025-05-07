class CompoundProperties:
    """Contaminant-specific properties; Kd is computed from log Kow and site foc."""

    def __init__(self, log_Kow, decay_rate, molecular_weight):
        """
        Parameters:
        - log_Kow: log₁₀ of octanol-water partition coefficient
        - decay_rate: first-order decay rate (day⁻¹)
        - molecular_weight: g/mol
        """
        self.log_Kow = log_Kow
        self.decay_rate = decay_rate
        self.molecular_weight = molecular_weight

    def compute_Kd(self, site):
        """Estimate Kd = foc * Koc, where log Koc = log Kow - 0.211"""
        Koc = 10 ** (self.log_Kow - 0.211)
        return site.foc * Koc

    def retardation(self, site):
        """
        Compute retardation factor:
            R = 1 + (ρ_b / n) * Kd
        using site bulk density, porosity, and Kd
        """
        Kd = self.compute_Kd(site)
        return 1 + (site.bulk_density / site.porosity) * Kd

