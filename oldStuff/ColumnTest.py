from random import gauss

from pylab import *

import Neuron
from oldStuff import IonotropicConnection

# Time
tau = 0.1
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
pyramidalParams["type"] = "Pyramidal"
#

fsParams = {}
fsParams["C"]= 100 #20
fsParams["k"] = 1
fsParams["v_r"] = -55
fsParams["v_t"] = -40
fsParams["v_peak"] = 25
fsParams["a"] = 0.15
fsParams["b"] = 8
fsParams["c"] = -55
fsParams["d"] = 200
fsParams["tau"] = tau
fsParams["type"] = "FS"

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
ltsParams["type"] = "LTS"

connections = []
pyramidals = []
# for i in range(40):
#     pyramidalParams["type"] = "Pyramidal", i
#     pyramidals.append(Neuron.Neuron(pyramidalParams))
pyramidals = [Neuron.Neuron(pyramidalParams) for i in range(20)]
fsNeurons = [Neuron.Neuron(fsParams) for i in range(20)]
ltsNeurons = [Neuron.Neuron(ltsParams) for i in range(20)]
for pyramidal in pyramidals:
    pyramidal.debug = False
    pyramidal.externalInput = gauss(500.0, 50.0)
    for fsNeuron in fsNeurons:
        connections.append(IonotropicConnection.IonotropicConnection(tau, 0, gauss(600.0, 1.0), pyramidal, fsNeuron, debug=False))
    for ltsNeuron in ltsNeurons:
        connections.append(IonotropicConnection.IonotropicConnection(tau, 0, gauss(600.0, 1.0), pyramidal, ltsNeuron, debug=False))

print(len(connections))

for t in range(len(tspan)):
    if t%10 == 0:
        print(t)
        # print(fsNeurons[1].synapticInput, ",", fsNeurons[1].v)
    for pyramidal in pyramidals:
        pyramidal.step()
    for ltsNeuron in ltsNeurons:
        ltsNeuron.step()
    for fsNeuron in fsNeurons:
        fsNeuron.step()
    # for connection in connections:
    #     connection.step()

pyramidalVoltages = [pyramidals[i].vv for i in range(len(pyramidals))]
fsVoltages = [fsNeurons[i].vv for i in range(len(fsNeurons))]
ltsVoltages = [ltsNeurons[i].vv for i in range(len(ltsNeurons))]

figure()
pcolor(pyramidalVoltages, vmin=-100, vmax=60)
colorbar()
title('Pyramidal Cells')

figure()
pcolor(fsVoltages, vmin=-100, vmax=60)
colorbar()
title('FS Interneurons')

figure()
pcolor(ltsVoltages, vmin=-100, vmax=60)
colorbar()
title('LTS Interneurons')

figure()
plot(tspan, fsNeuron.vv)
title('FSNeuron')

# plot(tspan, cell1.vv)
# plot(tspan, cell1.uu)
# title('Pyramidal Cell')
#
# figure()
# plot(tspan, cell2.vv)
# plot(tspan, cell2.uu)
# title('FS Interneuron')
show()