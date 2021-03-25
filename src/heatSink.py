class HeatSink:
    def __init__(self,
                 baseLength: float = 0.7,
                 baseWidth: float = 0.5,
                 baseDepth: float = 0.02,
                 finLength: float = 0.5,
                 finWidth: float = 0.0125,
                 finDepth: float = 0.015,
                 noFins: int = 20,
                 conductivity: float = 205,
                 ):

        self.baseLength = baseLength
        self.baseWidth = baseWidth
        self.baseDepth = baseDepth
        self.finLength = finLength
        self.finWidth = finWidth
        self.finDepth = finDepth
        self.noFins = noFins
        self.conductivity = conductivity

        self.baseArea = self.baseLength * self.baseWidth
        self.finArea = self.finLength * self.finWidth
        self.finPerimeter = 2 * self.finLength + 2 * self.finWidth

        self.volume = self.baseArea * self.baseDepth + self.noFins * (self.finArea * self.finDepth)
        self.mass = self.volume * 2700
        self.cost = self.mass * 0.556
