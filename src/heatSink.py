from math import  sqrt, sinh, cosh


class HeatSink:
    def __init__(self,
                 baseLength: float = 0.865,
                 baseWidth: float = 0.5,
                 baseDepth: float = 0.003,
                 noFinsLength: float = 45,
                 noFinsWidth: float = 15,
                 finWidth: float = 0.03,
                 finLength: float = 0.005,
                 finDepth: float = 0.02,
                 conductivity: float = 205,
                 pipeWeight: float = 1.4135,
                 contactConductivity: float = 3,
                 timThickness: float = 0.001,
                 h_bar: float = 16.8,
                 ):

        self.noFinsLength = round(noFinsLength)
        self.noFinsWidth = round(noFinsWidth)

        self.baseLength = baseLength
        self.baseWidth = baseWidth
        self.baseDepth = baseDepth

        self.noFinsLength = noFinsLength
        self.noFinsWidth = noFinsWidth
        self.finWidth = finWidth
        self.finLength = finLength
        self.finDepth = finDepth

        self.spacingLength = (self.baseLength - (self.noFinsLength * self.finLength)) / (self.noFinsLength + 1)
        while self.spacingLength < 0:
            self.noFinsLength -= 1
            self.spacingLength = (self.baseLength - (self.noFinsLength * self.finLength)) / (self.noFinsLength + 1)

        self.spacingWidth = (self.baseWidth - (self.noFinsWidth * self.finWidth)) / (self.noFinsWidth + 1)
        while self.spacingWidth < 0:
            self.noFinsWidth -= 1
            self.spacingWidth = (self.baseWidth - (self.noFinsWidth * self.finWidth)) / (self.noFinsWidth + 1)

        self.noFins = self.noFinsLength * self.noFinsWidth

        self.conductivity = conductivity

        self.baseArea = self.baseLength * self.baseWidth
        self.finArea = self.finLength * self.finWidth
        self.finPerimeter = 2 * self.finLength + 2 * self.finWidth

        self.volume = self.baseArea * self.baseDepth + self.noFins * (self.finArea * self.finDepth)
        self.mass = self.volume * 2700 + pipeWeight
        self.cost = self.mass * 2

        self.contactConductivity = contactConductivity
        self.timThickness = timThickness
        self.h_hs = h_bar

    def base_temperature(self, t_2, Q_hs_cond):
        return t_2 - Q_hs_cond / self.baseArea * self.baseDepth / self.conductivity

    def tim_temperature(self, t_2, Q_solar):
        return t_2 + Q_solar * self.timThickness / (self.contactConductivity * self.baseArea)

    def fin_convection(self, t_b, fluid_properties):
        def calculate_fin_constants(h_bar, p, k, a_c, t_b, t_inf):
           m = sqrt((h_bar * p) / (k * a_c))
           M = sqrt(h_bar * p * k * a_c) * (t_b - t_inf)
           return m, M

        m, M = calculate_fin_constants(self.h_hs, self.finPerimeter, self.conductivity,
                                        self.finArea, t_b, fluid_properties.T_inf)

        finTipHeatTransfer = self.noFins * M * (sinh(m * self.finDepth) +
                                                            (self.h_hs / (m * self.conductivity))
                                                         * cosh(m * self.finDepth)) / \
                                 (cosh(m * self.finDepth) +
                                  (self.h_hs / (m * self.conductivity)) *
                                  sinh(m * self.finDepth))
        finHeatTransfer = finTipHeatTransfer + self.noFins * self.h_hs * self.finPerimeter * \
                              self.finDepth * (t_b - fluid_properties.T_inf)

        return finHeatTransfer