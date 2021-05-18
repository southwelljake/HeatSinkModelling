from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from system import System
import matplotlib.pyplot as plt

flow_rates = [0.00025, 0.0005, 0.001, 0.002, 0.003, 0.005]
panel_temp = []
no_pipes = []

inlet_temp = 30

for f in flow_rates:
    temps = []
    pipes = []
    for p in [1, 2, 3, 4, 5]:
        heat_sink = HeatSink()
        solar_panel = SolarPanel()
        water_pipes = WaterPipes(no_pipes=p)
        final_temp = 0
        for i in range(0, 40):
            system = System(heat_sink=heat_sink,
                            solar_panel=solar_panel,
                            water_pipes=water_pipes,
                            ambient_temp=30,
                            flow_rate=f,
                            flow_temp=inlet_temp)
            system.update()
            inlet_temp = system.outletTemp
            final_temp = system.T_2

        temps.append(final_temp)
        pipes.append(p)

    panel_temp.append(temps)
    no_pipes.append(pipes)

for i in range(0, len(flow_rates)):
    plt.plot(no_pipes[i], panel_temp[i], 'o-', label='Flow rate: ' + str(flow_rates[i]) + ' m3/s')

plt.legend()
plt.xlabel('Number of Pipes')
plt.ylabel('Panel Surface Temperature (°C)')
plt.show()
