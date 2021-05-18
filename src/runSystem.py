from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from fluidProperties import FluidProperties
from system import System
import matplotlib.pyplot as plt

inlet_temp = 30
outlet_temp = []
panel_temp = []
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
                    flow_rate=0.002138/23,
                    flow_temp=inlet_temp)
    system.update()
    inlet_temp = system.outletTemp

    panel.append(i + 1)
    outlet_temp.append(system.outletTemp)
    panel_temp.append(system.T_1)
    performance.append((70-system.T_1) * 0.45)

plt.plot(panel, outlet_temp, label='Water Outlet Temperature')
plt.plot(panel, panel_temp, label='Panel Surface Temperature')
plt.legend()
plt.show()
