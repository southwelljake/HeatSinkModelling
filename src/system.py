from heatSink import HeatSink
from solarPanel import SolarPanel
from waterPipes import WaterPipes
from fluidProperties import FluidProperties
import csv
from math import cos, sqrt, sinh, cosh, exp, pi


class System:
    def __init__(self,
                 heat_sink: HeatSink,
                 solar_panel: SolarPanel,
                 water_pipes: WaterPipes,
                 fluid_properties: FluidProperties,
                 flow_rate: float = 0.00006,
                 flow_temp: float = 30,
                 ):

        self.heatSink = heat_sink
        self.solarPanel = solar_panel
        self.waterPipes = water_pipes
        self.fluidProperties = fluid_properties

        self.T_inf = self.fluidProperties.T_inf

        self.waterPipes.inletTemp = flow_temp
        self.waterPipes.inletFlowRate = flow_rate
        self.waterPipes.update_flow_rate()

        self.T_0 = 0  # Panel front surface temperature
        self.T_1 = 0  # Panel back surface temperature
        self.T_2 = 45  # Heat Sink bottom temperature
        self.T_b = 0  # Heat Sink base temperature

        self.Q_solar = 0
        self.Q_panel_conv = 0
        self.Q_hs_cond = 0
        self.Q_fins = 0
        self.Q_pipes = 0

        self.q_solar = 0
        self.q_panel_conv = 0
        self.q_hs_cond = 0
        self.q_fins = 0
        self.q_pipes = 0

    def update(self):
        self.Q_solar = self.solarPanel.Q_solar

        # Shooting Method
        a = [self.T_inf + 5, self.T_inf + 20]
        x = [self.calculate_heat_transfer(a[0]),
             self.calculate_heat_transfer(a[1])]
        e = [x[0] - self.Q_solar, x[1] - self.Q_solar]

        n = 1
        while abs(e[n]) > 0.1 and n < 1000:
            a.append(a[n] - e[n] * (a[n] - a[n-1])/(e[n] - e[n-1]))
            x.append(self.calculate_heat_transfer(a[n+1]))
            e.append(x[-1] - self.Q_solar)
            n += 1

        self.T_2 = a[-1]
        self.T_1 = self.heatSink.tim_temperature(self.T_2, self.Q_solar)
        self.T_0 = self.solarPanel.panel_conduction(self.T_1)

    def calculate_heat_transfer(self, t_2):
        # Calculate Heat Transfer Rates
        t_1 = self.heatSink.tim_temperature(t_2, self.Q_solar)
        self.Q_panel_conv = self.solarPanel.panel_convection(t_1, self.heatSink.baseArea, self.fluidProperties)

        # Calculate Heat Sink Heat Flux
        t_b = self.heatSink.base_temperature(t_2, self.Q_solar - self.Q_panel_conv)

        # Calculate Fin Heat Transfer
        self.Q_fins = self.heatSink.fin_convection(t_b, self.fluidProperties)

        # Calculate Pipe Heat Transfer
        self.Q_pipes = self.waterPipes.water_convection(t_b, self.fluidProperties)

        return self.Q_panel_conv + self.Q_fins + self.Q_pipes

