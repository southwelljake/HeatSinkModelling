from math import pi


class WaterPipes:
    def __init__(self,
                 no_pipes: int = 3,
                 pipe_diameter: float = 0.0127,
                 pipe_length: float = 0.5,
                 ):

        self.noPipes = no_pipes
        self.pipeDiameter = pipe_diameter
        self.pipeLength = pipe_length
        self.pipeFlowRate = 0
        self.pipeVelocity = 0
        self.inletFlowRate = 0.00036
        self.inletTemp = 30
        self.update_flow_rate()

    def update_flow_rate(self):
        self.pipeFlowRate = self.inletFlowRate / self.noPipes
        self.pipeVelocity = self.pipeFlowRate / ((pi * self.pipeDiameter ** 2) / 4)
