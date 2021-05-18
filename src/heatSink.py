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
