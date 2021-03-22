import csv
from math import pi, cos, sqrt, sinh, cosh

# Create Panel - Assume Horizontal Orientation
panelLength = 1.98
panelWidth = 0.98
panelArea = panelWidth * panelLength
panelAngle = 45 * pi / 180

# Create Heat Sink
baseLength = 0.7
baseWidth = 0.5
baseDepth = 0.015
finLength = 0.5
finWidth = 0.0125
finDepth = 0.015
baseArea = baseLength * baseWidth
finArea = finLength * finWidth
finPerimeter = 2 * finLength + 2 * finWidth
noFins = 20

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

        properties = interpolate(t_s, t_inf, dry_air)

        return properties

    def interpolate(t_s, t_inf, dry_air):

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

        return Q_solar, Q_panel_conv, Q_hs_cond, Q_fins

    def calculate_error(Q_solar, Q_panel_conv, Q_fins):
        return Q_solar - (Q_panel_conv + Q_fins)

    def calculate_temperatures():
        # Guess Back Panel Surface Temp
        T_2 = 48  # Celsius
        # Guess Convection Rate of Fins
        h_bar = 25  # W/m2K

        Q_solar, Q_panel_conv, Q_hs_cond, Q_fins = calculate_heat_transfer(T_2, h_bar)
        error = calculate_error(Q_solar, Q_panel_conv, Q_fins)

        while abs(error) > 0.5:
            if error > 0:
                T_2 += 0.01
            else:
                T_2 -= 0.01

            Q_solar, Q_panel_conv, Q_hs_cond, Q_fins = calculate_heat_transfer(T_2, h_bar)
            error = calculate_error(Q_solar, Q_panel_conv, Q_fins)

        return T_2

    return calculate_temperatures()


Surface_Temperature = run_convergence()
print(Surface_Temperature)


