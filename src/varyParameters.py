from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from system import System
import matplotlib.pyplot as plt

# Set defaults of parameters to vary
noFinsLength = 45
noFinsWidth = 15
finLength = 0.005
finWidth = 0.03
finDepth = 0.02


def run(no_fins_length, no_fins_width, fin_length, fin_width, fin_depth):
    panel_temp = []

    inlet_temp = 30
    cost = 0

    for i in range(0, 92):
        heat_sink = HeatSink(noFinsLength=no_fins_length,
                             noFinsWidth=no_fins_width,
                             finLength=fin_length,
                             finWidth=fin_width,
                             finDepth=fin_depth)
        solar_panel = SolarPanel()
        water_pipes = WaterPipes()
        system = System(heat_sink=heat_sink,
                        solar_panel=solar_panel,
                        water_pipes=water_pipes,
                        ambient_temp=30,
                        flow_rate=0.002138/23,
                        flow_temp=inlet_temp)
        system.update()

        inlet_temp = system.outletTemp

        panel_temp.append(system.T_1)
        cost = system.heatSink.cost

    performance = (70 - sum(panel_temp) / 92) * 0.45

    return performance, cost


# Varying parameter lists
varyNoFinsLength = [5, 10, 15, 20, 25, 30, 35, 40, 45]
varyNoFinsWidth = [1, 2, 5, 8, 10, 12, 15]
varyFinLength = [0.0025, 0.004, 0.005, 0.0075, 0.01, 0.0125, 0.015]
varyFinWidth = [0.0025, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02, 0.03]
varyFinDepth = [0.005, 0.010, 0.0125, 0.015, 0.02, 0.025, 0.03, 0.04]

costNoFinsLength = []
costNoFinsWidth = []
costFinLength = []
costFinWidth = []
costFinDepth = []

perfNoFinsLength = []
perfNoFinsWidth = []
perfFinLength = []
perfFinWidth = []
perfFinDepth = []

# Vary No Fins Length
for value in varyNoFinsLength:
    p, c = run(value, noFinsWidth, finLength, finWidth, finDepth)
    perfNoFinsLength.append(p)
    costNoFinsLength.append(c)

fig1, ax1 = plt.subplots()

ax1.plot(varyNoFinsLength, perfNoFinsLength, 'b')
ax1.set_xlabel("Number of Fins Length-ways")
ax1.set_ylabel("Performance Increase (%)")

ax2 = ax1.twinx()
ax2.plot(varyNoFinsLength, costNoFinsLength, 'r')
ax2.set_ylabel("Cost ($)")

# Vary No Fins Width
for value in varyNoFinsWidth:
    p, c = run(noFinsLength, value, finLength, finWidth, finDepth)
    perfNoFinsWidth.append(p)
    costNoFinsWidth.append(c)

fig3, ax3 = plt.subplots()

ax3.plot(varyNoFinsWidth, perfNoFinsWidth, 'b')
ax3.set_xlabel("Number of Fins Width-ways")
ax3.set_ylabel("Performance Increase (%)")

ax4 = ax3.twinx()
ax4.plot(varyNoFinsWidth, costNoFinsWidth, 'r')
ax4.set_ylabel("Cost ($)")

# Vary Fin Length
for value in varyFinLength:
    p, c = run(noFinsLength, noFinsWidth, value, finWidth, finDepth)
    perfFinLength.append(p)
    costFinLength.append(c)

fig5, ax5 = plt.subplots()

ax5.plot(varyFinLength, perfFinLength, 'b')
ax5.set_xlabel("Fin Length (m)")
ax5.set_ylabel("Performance Increase (%)")

ax6 = ax5.twinx()
ax6.plot(varyFinLength, costFinLength, 'r')
ax6.set_ylabel("Cost ($)")

# Vary Fin Width
for value in varyFinWidth:
    p, c = run(noFinsLength, noFinsWidth, finLength, value, finDepth)
    perfFinWidth.append(p)
    costFinWidth.append(c)

fig7, ax7 = plt.subplots()

ax7.plot(varyFinWidth, perfFinWidth, 'b')
ax7.set_xlabel("Fin Width (m)")
ax7.set_ylabel("Performance Increase (%)")

ax8 = ax7.twinx()
ax8.plot(varyFinWidth, costFinWidth, 'r')
ax8.set_ylabel("Cost ($)")

# Vary Fin Depth
for value in varyFinDepth:
    p, c = run(noFinsLength, noFinsWidth, finLength, finWidth, value)
    perfFinDepth.append(p)
    costFinDepth.append(c)

fig9, ax9 = plt.subplots()

ax9.plot(varyFinDepth, perfFinDepth, 'b')
ax9.set_xlabel("Fin Depth (m)")
ax9.set_ylabel("Performance Increase (%)")

ax10 = ax9.twinx()
ax10.plot(varyFinDepth, costFinDepth, 'r')
ax10.set_ylabel("Cost ($)")

plt.show()
