import csv

# Create Panel
panelLength = 1.98
panelWidth = 0.98
panelArea = panelWidth * panelLength

# Create Heat Sink
baseLength = 0.7
baseWidth = 0.5
baseDepth = 0.015
finLength = 0.7
finWidth = 0.01
finDepth = 0.015
baseArea = baseLength * baseWidth
finArea = finLength * finWidth
noFins = 20

# Ambient Conditions
T_inf = 30  # Celsius


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

    return dry_air


def interpolate(t_s, t_inf):

    return


values = get_air_properties(30, 40)

# Solar Radiation - *Improve Calculation*


# Guess Temps
T_b = 40  # Celsius
T_2 = 50  # Celsius
