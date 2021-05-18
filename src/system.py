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
                 active_cooling: bool = True,
                 flow_rate: float = 0.00006,
                 flow_temp: float = 30,
                 max_surface_temp: float = 70,
                 ):

        self.heatSink = heat_sink
        self.solarPanel = solar_panel
        self.waterPipes = water_pipes
        self.fluidProperties = fluid_properties

        self.active = active_cooling
        self.T_inf = self.fluidProperties.T_inf

        self.inletFlowRate = flow_rate
        self.inletTemp = flow_temp
        self.waterPipes.inletTemp = self.inletTemp
        self.waterPipes.inletFlowRate = self.inletFlowRate
        self.waterPipes.update_flow_rate()
        self.outletTemp = 0

        self.max_T_s = max_surface_temp

        self.T_1 = 0  # Panel front surface temperature
        self.T_2 = 45  # Panel back surface temperature
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
        self.q_solar = self.solar_radiation(self.max_T_s, self.T_inf, self.fluidProperties.get_air_properties(
            self.max_T_s))
        self.Q_solar = self.q_solar * self.solarPanel.panelArea

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

    def vertical_plate(self, properties, plate_length, plate_angle, t_s, t_inf):
        gr = (properties["Density"] ** 2 * 9.81 * cos(plate_angle) * (1 / properties["Temp"]) * (t_s - t_inf) *
              plate_length ** 3) / (properties["Mu"] ** 2)
        ra = gr * properties["Pr"]
        nu = (
                     0.825 + (0.387 * ra ** (1 / 6)) / ((1 + (0.492 / properties["Pr"]) ** (9 / 16)) ** (8 / 27))
             ) ** 2
        h = nu * properties["k"] / plate_length
        if t_s < t_inf:
            return 0
        else:
            return h

    def solar_radiation(self, t_s, t_inf, properties):
        h = self.vertical_plate(properties, self.solarPanel.panelWidth, self.solarPanel.panelAngle, t_s, t_inf)
        return h * (t_s - self.T_inf)

    def panel_convection(self, t_s, properties):
        h = self.vertical_plate(properties, self.solarPanel.panelWidth, self.solarPanel.panelAngle, t_s, self.T_inf)
        return h * (t_s - self.T_inf)

    def calculate_heat_transfer(self, t_2):
        # Calculate Heat Transfer Rates
        self.Q_panel_conv = self.panel_convection(t_2, self.fluidProperties.get_air_properties(t_2)) * \
            (self.solarPanel.panelArea - self.heatSink.baseArea)

        # Calculate Heat Sink Heat Flux
        t_b = self.heatSink.base_temperature(t_2, self.Q_solar - self.Q_panel_conv)

        # Calculate Fin Heat Transfer
        self.Q_fins = self.heatSink.fin_convection(t_b, self.fluidProperties)

        # Calculate Pipe Heat Transfer
        self.Q_pipes = self.waterPipes.water_convection(t_b, self.fluidProperties)
        self.outletTemp = self.waterPipes.outletTemp

        return self.Q_panel_conv + self.Q_fins + self.Q_pipes

