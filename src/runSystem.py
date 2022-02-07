from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from fluidProperties import FluidProperties
from system import System
import matplotlib.pyplot as plt

inlet_temp = 30
outlet_temp = []
t_0 = []
t_1 = []
t_b = []
t_inf = []
panel = []
performance = []

for i in range(0, 92):
    heat_sink = HeatSink(noFinsLength=22,
                         noFinsWidth=4,
                         finLength=0.0025,
                         finWidth=0.12125,
                         finDepth=0.035)
    solar_panel = SolarPanel()
    water_pipes = WaterPipes()
    fluid_properties = FluidProperties()
    system = System(heat_sink=heat_sink,
                    solar_panel=solar_panel,
                    water_pipes=water_pipes,
                    fluid_properties=fluid_properties,
                    flow_rate=9.3e-5,
                    flow_temp=inlet_temp)
    system.update()
    inlet_temp = system.waterPipes.outletTemp

    panel.append(i + 1)
    outlet_temp.append(system.waterPipes.outletTemp)
    t_0.append(system.T_0)
    t_1.append(system.T_1)
    t_b.append(system.T_b)
    t_inf.append(system.T_inf)
    performance.append((72-system.T_0) * 0.45)

fig, ax = plt.subplots()

ax.plot(panel, outlet_temp, label='Water Outlet Temperature')
ax.plot(panel, t_0, label='Panel Top Surface Temperature')
ax.plot(panel, t_1, label='Panel Bottom Surface Temperature')
ax.plot([0, 92], [72, 72], label='Maximum Panel Temperature without Heat Sink')
ax.plot(panel, t_inf, label='Ambient Air Temperature')
ax.set_xlabel('Number of Solar Panels')
ax.set_ylabel('Temperature (°C)')
ax.legend()

fig2, ax2 = plt.subplots()

ax2.plot(panel, performance)
ax2.set_xlabel('Number of Solar Panels')
ax2.set_ylabel('Performance Increase (%)')

plt.show()
