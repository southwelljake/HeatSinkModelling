from math import pi


class SolarPanel:
    def __init__(self,
                 panelLength: float = 1.98,
                 panelWidth: float = 0.98,
                 h_bar: float = 6,
                 irradiation: float = 500):

        self.panelLength = panelLength
        self.panelWidth = panelWidth
        self.panelArea = self.panelLength * self.panelWidth
        self.h_panel = h_bar
        self.q_solar = irradiation
        self.Q_solar = self.q_solar * self.panelArea

        # Layers
        self.glassThickness = 0.0036
        self.eva1Thickness = 0.0004
        self.solarCellsThickness = 0.0001
        self.eva2Thickness = 0.0004
        self.tedlarThickness = 0.0005

        self.glass_k = 0.98
        self.eva_k = 0.23
        self.cells_k = 200
        self.tedlar_k = 0.36

    def panel_convection(self, t_1, heat_sink_area, fluid_properties):
        return (2 * self.panelArea - heat_sink_area) * self.h_panel * (t_1 - fluid_properties.T_inf)

    def panel_conduction(self, t_1):

        resistance = (1 / self.panelArea) * (self.glassThickness / self.glass_k + self.eva1Thickness / self.eva_k +
                                             self.solarCellsThickness / self.cells_k + self.eva2Thickness / self.eva_k +
                                             self.tedlarThickness / self.tedlar_k)

        return t_1 + resistance * self.Q_solar

