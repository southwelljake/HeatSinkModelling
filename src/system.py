from heatSink import HeatSink
from solarPanel import SolarPanel
from waterPipes import WaterPipes
import csv
from math import cos, sqrt, sinh, cosh, exp, pi


class System:
    def __init__(self,
                 heat_sink: HeatSink,
                 solar_panel: SolarPanel,
                 water_pipes: WaterPipes,
                 active_cooling: bool = True,
                 ambient_temp: float = 30,
                 flow_rate: float = 0.00006,
                 flow_temp: float = 30,
                 max_surface_temp: float = 70,
                 ):

        self.heatSink = heat_sink
        self.solarPanel = solar_panel
        self.waterPipes = water_pipes

        self.active = active_cooling
        self.T_inf = ambient_temp

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
        self.q_solar = self.solar_radiation(self.max_T_s, self.T_inf, self.get_air_properties(self.max_T_s, self.T_inf))
        self.Q_solar = self.q_solar * self.solarPanel.panelArea

        # Guess Convection Rate of Fins
        h_bar = 16.8  # W/m2K

        # Shooting Method
        a = [self.T_inf + 5, self.T_inf + 20]
        x = [self.calculate_heat_transfer(a[0], h_bar),
             self.calculate_heat_transfer(a[1], h_bar)]
        e = [x[0] - self.Q_solar, x[1] - self.Q_solar]

        n = 1
        while abs(e[n]) > 0.1 and n < 1000:
            a.append(a[n] - e[n] * (a[n] - a[n-1])/(e[n] - e[n-1]))
            x.append(self.calculate_heat_transfer(a[n+1], h_bar))
            e.append(x[-1] - self.Q_solar)
            n += 1

        self.T_2 = a[-1]
        self.T_1 = self.T_2 + self.Q_solar * self.heatSink.timThickness / \
            (self.heatSink.contactConductivity * self.heatSink.baseArea)

    def get_air_properties(self, t_s, t_inf):
        dry_air = {
            "Temp": [],
            "Mu": [],
            "k": [],
            "Pr": [],
            "Density": [],
        }

        with open('dryAir.csv', newline='') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=',')
            for row in file_reader:
                dry_air["Temp"].append(float(row[0]))
                dry_air["Mu"].append(float(row[4]) * 10 ** -5)
                dry_air["k"].append(float(row[5]) * 10 ** -2)
                dry_air["Pr"].append(float(row[6]))
                dry_air["Density"].append(float(row[7]))

        properties = self.interpolate_air(t_s, t_inf, dry_air)

        return properties

    def interpolate_air(self, t_s, t_inf, dry_air):

        t_film = ((t_s + t_inf) / 2) + 273
        index = 0
        for i in range(0, len(dry_air["Temp"]) - 1):
            if dry_air["Temp"][i] < t_film < dry_air["Temp"][i + 1]:
                index = i
            elif t_film == dry_air["Temp"][i]:
                index = i

        properties = {
            "Temp": t_film,
            "Mu": (t_film - dry_air["Temp"][index]) * (dry_air["Mu"][index + 1] - dry_air["Mu"][index]) /
                  (dry_air["Temp"][index + 1] - dry_air["Temp"][index]) + dry_air["Mu"][index],
            "k": (t_film - dry_air["Temp"][index]) * (dry_air["k"][index + 1] - dry_air["k"][index]) /
                 (dry_air["Temp"][index + 1] - dry_air["Temp"][index]) + dry_air["k"][index],
            "Pr": (t_film - dry_air["Temp"][index]) * (dry_air["Pr"][index + 1] - dry_air["Pr"][index]) /
                  (dry_air["Temp"][index + 1] - dry_air["Temp"][index]) + dry_air["Pr"][index],
            "Density": (t_film - dry_air["Temp"][index]) * (
                        dry_air["Density"][index + 1] - dry_air["Density"][index]) /
                       (dry_air["Temp"][index + 1] - dry_air["Temp"][index]) + dry_air["Density"][index],
        }

        return properties

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

    def fin_convection(self, t_b, h_hs):
        def calculate_fin_constants(h_bar, p, k, a_c, t_b, t_inf):
            m = sqrt((h_bar * p) / (k * a_c))
            M = sqrt(h_bar * p * k * a_c) * (t_b - t_inf)
            return m, M

        m, M = calculate_fin_constants(h_hs, self.heatSink.finPerimeter, self.heatSink.conductivity,
                                       self.heatSink.finArea, t_b, self.T_inf)

        finTipHeatTransfer = self.heatSink.noFins * M * (sinh(m * self.heatSink.finDepth) +
                                                         (h_hs / (m * self.heatSink.conductivity))
                                                         * cosh(m * self.heatSink.finDepth)) / \
                                                        (cosh(m * self.heatSink.finDepth) +
                                                             (h_hs / (m * self.heatSink.conductivity)) *
                                                         sinh(m * self.heatSink.finDepth))
        finHeatTransfer = finTipHeatTransfer + self.heatSink.noFins * h_hs * self.heatSink.finPerimeter * \
            self.heatSink.finDepth * (t_b - self.T_inf)

        return finHeatTransfer

    def get_water_properties(self, t_s, t_m):
        water = {
            "Temp": [],
            "Density": [],
            "Cp_f": [],
            "Mu_f": [],
            "k_f": [],
            "Pr_f": [],
        }

        with open('waterProperties.csv', newline='') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=',')
            for row in file_reader:
                water["Temp"].append(float(row[0]))
                water["Density"].append(1 / (float(row[2]) * 10 ** -2))
                water["Cp_f"].append(float(row[3]) * 10 ** 3)
                water["Mu_f"].append(float(row[5]) * 10 ** -6)
                water["k_f"].append(float(row[7]) * 10 ** -3)
                water["Pr_f"].append(float(row[9]))

        properties = self.interpolate_water(t_s, t_m, water)

        return properties

    def interpolate_water(self, t_s, t_m, water):

        t_film = (t_s + t_m) / 2
        index = 0
        for i in range(0, len(water["Temp"]) - 1):
            if water["Temp"][i] < t_film < water["Temp"][i + 1]:
                index = i
            elif t_film == water["Temp"][i]:
                index = i

        properties = {
            "Temp": t_film,
            "Density": (t_film - water["Temp"][index]) * (water["Density"][index + 1] - water["Density"][index]) /
                       (water["Temp"][index + 1] - water["Temp"][index]) + water["Density"][index],
            "Cp_f": (t_film - water["Temp"][index]) * (water["Cp_f"][index + 1] - water["Cp_f"][index]) /
                    (water["Temp"][index + 1] - water["Temp"][index]) + water["Cp_f"][index],
            "Mu_f": (t_film - water["Temp"][index]) * (water["Mu_f"][index + 1] - water["Mu_f"][index]) /
                    (water["Temp"][index + 1] - water["Temp"][index]) + water["Mu_f"][index],
            "k_f": (t_film - water["Temp"][index]) * (water["k_f"][index + 1] - water["k_f"][index]) /
                   (water["Temp"][index + 1] - water["Temp"][index]) + water["k_f"][index],
            "Pr_f": (t_film - water["Temp"][index]) * (water["Pr_f"][index + 1] - water["Pr_f"][index]) /
                    (water["Temp"][index + 1] - water["Temp"][index]) + water["Pr_f"][index],
        }

        return properties

    def water_heat_transfer(self, t_s, t_i, t_e, pipe_length, pipe_diameter, velocity, flow_rate):
        t_m = (t_i + t_e) / 2

        water = self.get_water_properties(t_s, t_m)

        re = (water["Density"] * velocity * pipe_diameter) / water["Mu_f"]

        if re < 2300:
            nu = 3.66
        else:
            nu = 0.023 * re ** (4 / 5) * water["Pr_f"] ** 0.4

        h = nu * water["k_f"] / pipe_diameter

        new_t_e = t_s - (t_s - t_i) * exp(
            (-h * pi * pipe_diameter * pipe_length) / (water["Density"] * flow_rate * water["Cp_f"]))

        return new_t_e

    def water_convection(self, t_s, t_i, pipe_length, pipe_diameter, velocity, flow_rate, no_pipes):
        # Shooting Method
        a = [t_i + 5, t_i + 10]
        x = [self.water_heat_transfer(t_s, t_i, a[0], pipe_length, pipe_diameter, velocity, flow_rate),
             self.water_heat_transfer(t_s, t_i, a[1], pipe_length, pipe_diameter, velocity, flow_rate)]
        e = [x[0] - a[0], x[1] - a[1]]

        n = 1
        while abs(e[n]) > 0.1:
            a.append(a[n] - e[n] * (a[n] - a[n - 1]) / (e[n] - e[n - 1]))
            x.append(self.water_heat_transfer(t_s, t_i, a[n + 1], pipe_length, pipe_diameter, velocity, flow_rate))
            e.append(x[n+1] - a[n+1])
            n += 1

        water = self.get_water_properties(t_s, (t_i + a[-1] / 2))
        self.outletTemp = a[-1]

        return no_pipes * water["Density"] * flow_rate * water["Cp_f"] * (a[-1] - t_i)

    def calculate_heat_transfer(self, t_2, h_hs):
        # Calculate Heat Transfer Rates
        self.Q_panel_conv = self.panel_convection(t_2, self.get_air_properties(t_2, self.T_inf)) * \
            (self.solarPanel.panelArea - self.heatSink.baseArea)
        self.Q_hs_cond = self.Q_solar - self.Q_panel_conv

        # Calculate Heat Sink Heat Flux
        self.q_hs_cond = self.Q_hs_cond / self.heatSink.baseArea
        t_b = t_2 - self.q_hs_cond * self.heatSink.baseDepth / self.heatSink.conductivity

        # Calculate Fin Heat Transfer
        self.Q_fins = self.fin_convection(t_b, h_hs)

        # Calculate Pipe Heat Transfer
        self.Q_pipes = self.water_convection(t_b, self.waterPipes.inletTemp, self.waterPipes.pipeLength,
                                             self.waterPipes.pipeDiameter,
                                             self.waterPipes.pipeVelocity, self.waterPipes.pipeFlowRate,
                                             self.waterPipes.noPipes)

        return self.Q_panel_conv + self.Q_fins + self.Q_pipes

