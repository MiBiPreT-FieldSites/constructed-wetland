class SiteParameters:
    """All the media and flow parameters for a wetland cell."""

    def __init__(self, bulk_density, porosity, flow_rate, bulk_volume):
        """
        Parameters:
        - bulk_density: float, kg/L (mass of solids per bulk volume)
        - porosity:    float, -     (fraction of pore space in the bulk volume)
        - flow_rate:   float, m³/day (volumetric inflow to the cell)
        - bulk_volume: float, m³      (total volume of the wetland cell)
        """
        self.bulk_density = bulk_density
        self.porosity     = porosity
        self.flow_rate    = flow_rate
        self.bulk_volume  = bulk_volume

    @property
    def pore_volume(self):
        """
        Returns the total pore volume (m³) in the cell:
            Vp = porosity * bulk_volume
        """
        return self.porosity * self.bulk_volume
