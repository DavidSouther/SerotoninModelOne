from random import gauss

from pylab import *

import Neuron
from oldStuff import IonotropicConnection

# Time
tau = 0.25
tspan = arange(0,500, tau)
T1=len(tspan)/5

#Parameters
pyramidalParams = {}
pyramidalParams["C"]= 100
pyramidalParams["k"] = 3
pyramidalParams["v_r"] = -60
pyramidalParams["v_t"] = -50
pyramidalParams["v_peak"] = 50
# pyramidalParams["g_up"] = 3.0
# pyramidalParams["g_down"] = 5.0
pyramidalParams["a"] = 0.01
pyramidalParams["b"] = 5
pyramidalParams["c"] = -60
pyramidalParams["d"] = 400
pyramidalParams["tau"] = tau
#

fsParams = {}
fsParams["C"]= 20
fsParams["k"] = 1
fsParams["v_r"] = -55
fsParams["v_t"] = -40
fsParams["v_peak"] = 25
fsParams["a"] = 0.15
fsParams["b"] = 8
fsParams["c"] = -55
fsParams["d"] = 200
fsParams["tau"] = tau

ltsParams = {}
ltsParams["C"]= 100
ltsParams["k"] = 1
ltsParams["v_r"] = -56
ltsParams["v_t"] = -42
ltsParams["v_peak"] = 40
ltsParams["a"] = 0.03
ltsParams["b"] = 8
ltsParams["c"] = -50
ltsParams["d"] = 200
ltsParams["tau"] = tau

connections = []
pyramidals = [Neuron.Neuron(pyramidalParams) for i in range(20)]
fsNeurons = [Neuron.Neuron(fsParams) for i in range(20)]
ltsNeurons = [Neuron.Neuron(ltsParams) for i in range(20)]
for pyramidal in pyramidals:
    pyramidal.externalInput = gauss(500.0, 50.0)
    for fsNeuron in fsNeurons:
        connections.append(IonotropicConnection.IonotropicConnection(tau, 0, gauss(75.0, 25.0), pyramidal, fsNeuron))
    for ltsNeuron in ltsNeurons:
        connections.append(IonotropicConnection.IonotropicConnection(tau, 0, gauss(75.0, 25.0), pyramidal, ltsNeuron))
# connection = IonotropicConnection.IonotropicConnection(tau, 0, 2500.0, cell1, cell2)

for t in range(len(tspan)):
    if t%10 == 0:
        print(t)
    for pyramidal in pyramidals:
        pyramidal.step()
    for ltsNeuron in ltsNeurons:
        ltsNeuron.step()
    for connection in connections:
        connection.step()

pyramidalVoltages = [pyramidals[i].vv for i in range(len(pyramidals))]
ltsVoltages = [ltsNeurons[i].vv for i in range(len(ltsNeurons))]

figure()
pcolor(pyramidalVoltages, vmin=-100, vmax=60)
colorbar()
title('Pyramidal Cells')

figure()
pcolor(fastSpikingVoltages, vmin=-100, vmax=60)
colorbar()
title('FS Interneurons')

figure()
pcolor(ltsVoltages)
colorbar()
title('LTS Interneurons')

# plot(tspan, cell1.vv)
# plot(tspan, cell1.uu)
# title('Pyramidal Cell')
#
# figure()
# plot(tspan, cell2.vv)
# plot(tspan, cell2.uu)
# title('FS Interneuron')
show()