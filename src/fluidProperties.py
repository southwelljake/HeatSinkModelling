import csv


class FluidProperties:
    def __init__(self,
                 ambient_temp: float = 30):

        self.T_inf = ambient_temp

    def get_air_properties(self, t_s):
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

        properties = self.interpolate_air(t_s, dry_air)

        return properties

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

    def interpolate_air(self, t_s, dry_air):

        t_film = ((t_s + self.T_inf) / 2) + 273
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