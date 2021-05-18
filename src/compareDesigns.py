from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from system import System
import matplotlib.pyplot as plt

inlet_temp1 = 30
inlet_temp2 = 30
inlet_temp3 = 30
inlet_temp4 = 30
inlet_temp5 = 30
panel = []
d1_perf = []
d2_perf = []
d3_perf = []
d4_perf = []
d5_perf = []

for i in range(0, 92):
    heat_sink1 = HeatSink(noFinsLength=45,
                          noFinsWidth=1,
                          finLength=0.0025,
                          finWidth=0.5,
                          finDepth=0.03)
    heat_sink2 = HeatSink(noFinsLength=45,
                          noFinsWidth=2,
                          finLength=0.0025,
                          finWidth=0.24875,
                          finDepth=0.03)
    heat_sink3 = HeatSink(noFinsLength=45,
                          noFinsWidth=4,
                          finLength=0.0025,
                          finWidth=0.123125,
                          finDepth=0.03)
    heat_sink4 = HeatSink(noFinsLength=45,
                          noFinsWidth=8,
                          finLength=0.0025,
                          finWidth=0.0603125,
                          finDepth=0.03)
    heat_sink5 = HeatSink(noFinsLength=45,
                          noFinsWidth=16,
                          finLength=0.0025,
                          finWidth=0.02890625,
                          finDepth=0.03)
    solar_panel = SolarPanel()
    water_pipes = WaterPipes()
    system1 = System(heat_sink=heat_sink1,
                     solar_panel=solar_panel,
                     water_pipes=water_pipes,
                     ambient_temp=30,
                     flow_rate=0.002138/23,
                     flow_temp=inlet_temp1)
    system2 = System(heat_sink=heat_sink2,
                     solar_panel=solar_panel,
                     water_pipes=water_pipes,
                     ambient_temp=30,
                     flow_rate=0.002138/23,
                     flow_temp=inlet_temp2)
    system3 = System(heat_sink=heat_sink3,
                     solar_panel=solar_panel,
                     water_pipes=water_pipes,
                     ambient_temp=30,
                     flow_rate=0.002138/23,
                     flow_temp=inlet_temp3)
    system4 = System(heat_sink=heat_sink3,
                     solar_panel=solar_panel,
                     water_pipes=water_pipes,
                     ambient_temp=30,
                     flow_rate=0.002138/23,
                     flow_temp=inlet_temp4)
    system5 = System(heat_sink=heat_sink3,
                     solar_panel=solar_panel,
                     water_pipes=water_pipes,
                     ambient_temp=30,
                     flow_rate=0.002138/23,
                     flow_temp=inlet_temp5)
    system1.update()
    system2.update()
    system3.update()
    system4.update()
    system5.update()
    inlet_temp1 = system1.outletTemp
    inlet_temp2 = system2.outletTemp
    inlet_temp3 = system3.outletTemp
    inlet_temp4 = system4.outletTemp
    inlet_temp5 = system5.outletTemp

    panel.append(i + 1)
    d1_perf.append((70-system1.T_1) * 0.45)
    d2_perf.append((70-system2.T_1) * 0.45)
    d3_perf.append((70-system3.T_1) * 0.45)
    d4_perf.append((70-system4.T_1) * 0.45)
    d5_perf.append((70-system5.T_1) * 0.45)


plt.plot(panel, d1_perf, label='Design 1')
plt.plot(panel, d2_perf, label='Design 2')
plt.plot(panel, d3_perf, label='Design 3')
plt.plot(panel, d4_perf, label='Design 4')
plt.plot(panel, d5_perf, label='Design 5')

plt.xlabel("Panel")
plt.ylabel("Performance Increase (%)")
plt.legend()
plt.show()
