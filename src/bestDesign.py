from heatSink import HeatSink
from waterPipes import WaterPipes
from solarPanel import SolarPanel
from fluidProperties import FluidProperties
from system import System
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set default parameters
noFinsWidth = 1
finLength = 0.0025
finWidth = 0.5


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
        fluid_properties = FluidProperties()
        system = System(heat_sink=heat_sink,
                        solar_panel=solar_panel,
                        water_pipes=water_pipes,
                        fluid_properties=fluid_properties,
                        flow_rate=9.3e-5,
                        flow_temp=inlet_temp)
        system.update()

        inlet_temp = system.waterPipes.outletTemp

        panel_temp.append(system.T_0)
        cost = system.heatSink.cost

    performance = (72 - sum(panel_temp) / 92) * 0.45

    return performance, cost


# Varying parameter lists
varyNoFinsLength = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
varyFinDepth = [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]

materialCost = []
performance = []

for d in varyFinDepth:
    perf = []
    cost = []
    for n in varyNoFinsLength:
        p, c = run(n, noFinsWidth, finLength, finWidth, d)

        perf.append(p)
        cost.append(c)

    materialCost.append(cost)
    performance.append(perf)

fig1, ax1 = plt.subplots()

for i in range(0, len(varyFinDepth)):
    ax1.plot(varyNoFinsLength, performance[i], label="Fin Depth " + str(varyFinDepth[i]))

# ax1.plot([57, 63, 69, 77, 86, 98], [17.027, 17.045, 17.049, 17.059, 17.059, 17.064], 'k')
ax1.set_xlabel("Number of Fins Length-ways")
ax1.set_ylabel("Performance Increase (%)")
ax1.legend()

fig2, ax2 = plt.subplots()

for i in range(0, len(varyFinDepth)):
    ax2.plot(varyNoFinsLength, materialCost[i], label="Fin Depth " + str(varyFinDepth[i]))

#ax2.plot([20, 80], [17.5, 17.5], 'r')
#ax2.plot([20, 80], [15, 15], 'r')
ax2.set_xlabel("Number of Fins Length-ways")
ax2.set_ylabel("Cost ($)")
ax2.legend()

fig3 = plt.figure()
ax3 = Axes3D(fig3)

for i in range(0, len(varyFinDepth)):
    ax3.scatter(varyNoFinsLength, performance[i], materialCost[i], label="Fin Depth " + str(varyFinDepth[i]))

ax3.set_xlabel("Number of Fins Length-ways")
ax3.set_ylabel("Performance Increase (%)")
ax3.set_zlabel("Cost ($)")
ax3.legend()

plt.show()
