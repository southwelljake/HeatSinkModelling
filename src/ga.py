from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from system import System
import matplotlib.pyplot as plt
import numpy as np
from geneticalgorithm import geneticalgorithm as ga

# Set default parameters
noFinsWidth = 1
finLength = 0.0025
finWidth = 0.5


def f(X):
    inlet_temp = 30
    avg_performance = 0
    final_cost = 0
    temp = []

    #for i in range(0, 92):
    heat_sink = HeatSink(noFinsLength=X[0],
                             noFinsWidth=noFinsWidth,
                             finLength=finLength,
                             finWidth=finWidth,
                             finDepth=X[1])
    solar_panel = SolarPanel()
    water_pipes = WaterPipes()
    system = System(heat_sink=heat_sink,
                        solar_panel=solar_panel,
                        water_pipes=water_pipes,
                        ambient_temp=30,
                        flow_rate=0.002138 / 23,
                        flow_temp=inlet_temp)
    system.update()
    inlet_temp = system.outletTemp
    temp.append(system.T_1)

    avg_performance = (70 - sum(temp) / 92) * 0.45
    final_cost = system.heatSink.cost

    penalty = 0
    if final_cost > 17.5:
        penalty += 1000
    #if avg_performance < 17:
    #    penalty += 1000

    return (1000/avg_performance) + penalty


varbound = np.array([[56, 91],
                     [0.035, 0.06]])

algorithm_param = {'max_num_iteration': 100,
                   'population_size': 50,
                   'mutation_probability': 0.1,
                   'elit_ratio': 0.01,
                   'crossover_probability': 0.5,
                   'parents_portion': 0.3,
                   'crossover_type': 'uniform',
                   'max_iteration_without_improv': None}

model = ga(function=f,
           dimension=2,
           variable_type='real',
           variable_boundaries=varbound,
           algorithm_parameters=algorithm_param)

model.run()
