import csv
from math import pi, cos, sqrt, sinh, cosh, exp

# Create Panel - Assume Horizontal Orientation
panelLength = 1.98  # m
panelWidth = 0.98  # m
panelArea = panelWidth * panelLength  # m2
panelAngle = 45 * pi / 180  # rad

# Create Heat Sink
baseLength = 0.7  # m
baseWidth = 0.5  # m
baseDepth = 0.015  # m
finLength = 0.5  # m
finWidth = 0.0125  # m
finDepth = 0.015  # m
baseArea = baseLength * baseWidth
finArea = finLength * finWidth
finPerimeter = 2 * finLength + 2 * finWidth
noFins = 20

# Water Cooling
inletPipeDiameter = 0.08  # m
inletFlowRate = 0.00001  # m3/s
noPipes = 5
pipeDiameter = 0.008  # m
pipeLength = baseLength  # m
pipeFlowRate = inletFlowRate / noPipes  # m3/s
pipeVelocity = pipeFlowRate / ((pi * pipeDiameter ** 2) / 4)  # m/s

# Ambient Conditions
T_inf = 30  # Celsius

# Material Conductivity
k_Al = 205


def run_convergence():
    def get_air_properties(t_s, t_inf):
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

        properties = interpolate_air(t_s, t_inf, dry_air)

        return properties

    def interpolate_air(t_s, t_inf, dry_air):

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
            "Density": (t_film - dry_air["Temp"][index]) * (dry_air["Density"][index + 1] - dry_air["Density"][index]) /
                       (dry_air["Temp"][index + 1] - dry_air["Temp"][index]) + dry_air["Density"][index],
        }

        return properties

    def vertical_plate(properties, plate_length, plate_angle, t_s):
        gr = (properties["Density"] ** 2 * 9.81 * cos(plate_angle) * (1 / properties["Temp"]) * (t_s - T_inf) *
              panelWidth ** 3) / (properties["Mu"] ** 2)
        ra = gr * properties["Pr"]
        nu = (
                     0.825 + (0.387 * ra ** (1 / 6)) / ((1 + (0.492 / properties["Pr"]) ** (9 / 16)) ** (8 / 27))
             ) ** 2
        h = nu * properties["k"] / plate_length
        return h

    def solar_radiation(t_s, properties):
        h = vertical_plate(properties, panelWidth, panelAngle, t_s)
        return h * (t_s - T_inf)

    # Solar Radiation
    T_s = 70  # Celsius
    q_solar = solar_radiation(T_s, get_air_properties(T_s, T_inf))

    def panel_convection(t_s, properties):
        h = vertical_plate(properties, panelWidth, panelAngle, t_s)
        return h * (t_s - T_inf)

    def fin_convection(t_b, h_hs):
        def calculate_fin_constants(h_bar, p, k, a_c, t_b, t_inf):
            m = sqrt((h_bar * p) / (k * a_c))
            M = sqrt(h_bar * p * k * a_c) * (t_b - t_inf)
            return m, M

        m, M = calculate_fin_constants(h_hs, finPerimeter, k_Al, finArea, t_b, T_inf)

        return noFins * M * (sinh(m * finDepth) + (h_hs / (m * k_Al)) * cosh(m * finDepth)) / \
            (cosh(m * finDepth) + (h_hs / (m * k_Al)) * sinh(m * finDepth))

    def get_water_properties(t_s, t_m):
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

        properties = interpolate_water(t_s, t_m, water)

        return properties

    def interpolate_water(t_s, t_m, water):

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

    def water_heat_transfer(t_s, t_i, t_e, pipe_length, pipe_diameter, velocity, flow_rate):
        t_m = (t_i + t_e) / 2

        water = get_water_properties(t_s, t_m)

        re = (water["Density"] * velocity * pipe_diameter) / water["Mu_f"]

        if re < 2300:
            nu = 3.66
        else:
            nu = 0.023 * re ** (4 / 5) * water["Pr_f"] ** 0.4

        h = nu * water["k_f"] / pipe_diameter

        new_t_e = t_s - (t_s - t_i) * exp(
            (-h * pi * pipe_diameter * pipe_length) / (water["Density"] * flow_rate * water["Cp_f"]))

        return new_t_e

    def water_convection(t_s, t_i, pipe_length, pipe_diameter, velocity, flow_rate, no_pipes):
        # Guess t_e
        t_e = (t_i + t_s) / 2
        new_t_e = water_heat_transfer(t_s, t_i, t_e, pipe_length, pipe_diameter, velocity, flow_rate)

        while abs(new_t_e - t_e) > 0.01:
            t_e = new_t_e
            new_t_e = water_heat_transfer(t_s, t_i, t_e, pipe_length, pipe_diameter, velocity, flow_rate)

        water = get_water_properties(t_s, (t_i + new_t_e) / 2)

        return no_pipes * water["Density"] * flow_rate * water["Cp_f"] * (new_t_e - t_i)

    def calculate_heat_transfer(t_2, h_hs):

        # Calculate Heat Transfer Rates
        Q_solar = q_solar * panelArea
        Q_panel_conv = panel_convection(t_2, get_air_properties(t_2, T_inf)) * (panelArea - baseArea)
        Q_hs_cond = Q_solar - Q_panel_conv

        # Calculate Heat Sink Heat Flux
        q_hs_cond = Q_hs_cond / baseArea
        t_b = t_2 - q_hs_cond * baseDepth / k_Al

        # Calculate Fin Heat Transfer
        Q_fins = fin_convection(t_b, h_hs)

        # Calculate Pipe Heat Transfer
        Q_pipes = water_convection(t_b, T_inf, pipeLength, pipeDiameter, pipeVelocity, pipeFlowRate, noPipes)

        return Q_solar, Q_panel_conv, Q_hs_cond, Q_fins, Q_pipes

    def calculate_error(Q_solar, Q_panel_conv, Q_fins, Q_pipes):
        return Q_solar - (Q_panel_conv + Q_fins + Q_pipes)

    def calculate_temperatures():
        # Guess Back Panel Surface Temp
        T_2 = 48  # Celsius
        # Guess Convection Rate of Fins
        h_bar = 25  # W/m2K

        Q_solar, Q_panel_conv, Q_hs_cond, Q_fins, Q_pipes = calculate_heat_transfer(T_2, h_bar)
        error = calculate_error(Q_solar, Q_panel_conv, Q_fins, Q_pipes)

        while abs(error) > 0.5:
            if error > 0:
                T_2 += 0.01
            else:
                T_2 -= 0.01

            Q_solar, Q_panel_conv, Q_hs_cond, Q_fins, Q_pipes = calculate_heat_transfer(T_2, h_bar)
            error = calculate_error(Q_solar, Q_panel_conv, Q_fins, Q_pipes)

        return T_2

    return calculate_temperatures()


Surface_Temperature = run_convergence()
print(Surface_Temperature)


