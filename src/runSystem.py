from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from system import System

heat_sink = HeatSink()
solar_panel = SolarPanel()
water_pipes = WaterPipes()

inlet_temp = 30
for i in range(0, 40):
    system = System(heat_sink=heat_sink,
                    solar_panel=solar_panel,
                    water_pipes=water_pipes,
                    flow_rate=0.00036,
                    flow_temp=inlet_temp)
    system.update()
    inlet_temp = system.outletTemp
    print(system.outletTemp, system.T_2)
