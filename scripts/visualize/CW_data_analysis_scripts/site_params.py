class SiteParameters:
    """All the media and flow parameters for a wetland cell, including foc."""
    def __init__(self, bulk_density, porosity, flow_rate, bulk_volume, foc):
        """
        Parameters:
        - bulk_density: kg/L
        - porosity: fraction (0-1)
        - flow_rate: m³/day
        - bulk_volume: m³
        - foc: fraction of organic carbon in the medium
        """
        self.bulk_density = bulk_density
        self.porosity     = porosity
        self.flow_rate    = flow_rate
        self.bulk_volume  = bulk_volume
        self.foc          = foc

    @property
    def pore_volume(self):
        """Compute pore volume Vp = n × Vbulk (m³)."""
        return self.porosity * self.bulk_volume
