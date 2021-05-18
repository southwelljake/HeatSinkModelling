from math import pi, exp


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
        self.outletTemp = 0

    def update_flow_rate(self):
        self.pipeFlowRate = self.inletFlowRate / self.noPipes
        self.pipeVelocity = self.pipeFlowRate / ((pi * self.pipeDiameter ** 2) / 4)

    def water_heat_transfer(self, t_s, t_e, fluid_properties):
        t_m = (self.inletTemp + t_e) / 2

        water = fluid_properties.get_water_properties(t_s, t_m)

        re = (water["Density"] * self.pipeVelocity * self.pipeDiameter) / water["Mu_f"]

        if re < 2300:
            nu = 3.66
        else:
            nu = 0.023 * re ** (4 / 5) * water["Pr_f"] ** 0.4

        h = nu * water["k_f"] / self.pipeDiameter

        new_t_e = t_s - (t_s - self.inletTemp) * exp(
            (-h * pi * self.pipeDiameter * self.pipeLength) / (water["Density"] * self.pipeFlowRate * water["Cp_f"]))

        return new_t_e

    def water_convection(self, t_s, fluid_properties):
        # Shooting Method
        a = [self.inletTemp + 5, self.inletTemp + 10]
        x = [self.water_heat_transfer(t_s, a[0], fluid_properties),
             self.water_heat_transfer(t_s, a[1], fluid_properties)]
        e = [x[0] - a[0], x[1] - a[1]]

        n = 1
        while abs(e[n]) > 0.1:
            a.append(a[n] - e[n] * (a[n] - a[n - 1]) / (e[n] - e[n - 1]))
            x.append(self.water_heat_transfer(t_s, a[n + 1], fluid_properties))
            e.append(x[n+1] - a[n+1])
            n += 1

        water = fluid_properties.get_water_properties(t_s, (self.inletTemp + a[-1] / 2))
        self.outletTemp = a[-1]

        return self.noPipes * water["Density"] * self.pipeFlowRate * water["Cp_f"] * (a[-1] - self.inletTemp)