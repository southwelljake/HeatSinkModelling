from math import pi


class SolarPanel:
    def __init__(self,
                 panelLength: float = 1.98,
                 panelWidth: float = 0.98,
                 panelAngle: float = 45,
                 conductivity: float = 205,):

        self.panelLength = panelLength
        self.panelWidth = panelWidth
        self.panelArea = self.panelLength * self.panelWidth
        self.panelAngle = panelAngle * pi / 180
        self.conductivity = conductivity
