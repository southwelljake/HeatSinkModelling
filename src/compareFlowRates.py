from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from system import System
import matplotlib.pyplot as plt

avg_performance_D1 = []


flow_rates_D1 = [0.000271, 0.000542, 0.000813, 0.001355, 0.001626, 0.001897, 0.002168, 0.002439, 0.002710,
                 0.002981, 0.003252, 0.003523, 0.003793, 0.004064, 0.004335, 0.004606, 0.00487, 0.005148, 0.005419]

pressure_drop_D1 = [0.15, 0.60, 1.34, 3.73, 5.38, 7.32, 9.56, 12.10, 14.94, 18.08, 21.51, 25.25, 29.28, 33.61,
                    38.24, 43.17, 48.40, 53.93, 59.76]

for f in flow_rates_D1:
    panel = []
    performance = []
    heat_sink = HeatSink()
    solar_panel = SolarPanel()
    water_pipes = WaterPipes()

    inlet_temp = 30

    for i in range(0, 92):
        system = System(heat_sink=heat_sink,
                        solar_panel=solar_panel,
                        water_pipes=water_pipes,
                        ambient_temp=30,
                        flow_rate=f / 23,
                        flow_temp=inlet_temp)
        system.update()
        inlet_temp = system.outletTemp

        panel.append(i + 1)
        performance.append((70 - system.T_2) * 0.45)
    print(f)

    avg_performance_D1.append(sum(performance)/len(performance))

avg_performance_D2 = []


flow_rates_D2 = [0.000271, 0.000542, 0.000813, 0.001355, 0.001626, 0.001897, 0.002439, 0.002710,
                 0.002981, 0.003252, 0.003523, 0.003793, 0.004064, 0.004335, 0.004606, 0.00487, 0.005148, 0.005419]

pressure_drop_D2 = [0.15, 0.61, 1.38, 3.83, 5.51, 7.50, 12.41, 15.31, 18.53, 22.05, 25.88, 30.02, 34.46, 39.21,
                    44.26, 49.62, 55.29, 61.26]

for f in flow_rates_D2:
    panel = []
    performance = []
    heat_sink = HeatSink()
    solar_panel = SolarPanel()
    water_pipes = WaterPipes()

    inlet_temp = 30

    for i in range(0, 46):
        system = System(heat_sink=heat_sink,
                        solar_panel=solar_panel,
                        water_pipes=water_pipes,
                        ambient_temp=30,
                        flow_rate=f / 46,
                        flow_temp=inlet_temp)
        system.update()
        inlet_temp = system.outletTemp

        panel.append(i + 1)
        performance.append((70 - system.T_2) * 0.45)
        print(f, i)

    avg_performance_D2.append(sum(performance)/len(performance))


fig, ax = plt.subplots()

ax.plot(pressure_drop_D1, avg_performance_D1, 'o-', label='Design 1')
ax.plot(pressure_drop_D2, avg_performance_D2, 'o-', label='Design 2')
ax.set_xlabel('Pressure Drop (bar)')
ax.set_ylabel('Average performance increase (%)')
ax.legend()

fig2, ax2 = plt.subplots()

ax2.plot(flow_rates_D1, pressure_drop_D1, 'o-', label='Design 1')
ax2.plot(flow_rates_D2, pressure_drop_D2, 'o-', label='Design 2')
ax2.set_ylabel('Pressure Drop (bar)')
ax2.set_xlabel('Flow Rate (m3/s)')
ax2.legend()

plt.show()
