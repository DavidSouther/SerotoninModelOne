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

# fastSpikingParams = {}
# params["a"]=0.02
# params["b"]=0.25
# params["c"]=-65
# params["d"]=6
# params["tau"] = tau
# params["V0"] = -65
#
# lowThresholdSpikingParams = {}
# params["a"]=0.02
# params["b"]=8
# params["c"]=-65
# params["d"]=6
# params["tau"] = tau
# params["V0"] = -56


pyramidalParams
cell1 = Neuron.Neuron(pyramidalParams)
cell2 = Neuron.Neuron(fsParams)
connection = IonotropicConnection.IonotropicConnection(tau, 0, 1500.0, cell1, cell2)

cell1.externalInput = 750.0

for t in range(len(tspan)):
    cell1.step()
    cell2.step()
    connection.step()

plot(tspan, cell1.vv)
plot(tspan, cell1.uu)
title('Pyramidal Cell')

figure()
plot(tspan, cell2.vv)
plot(tspan, cell2.uu)
title('FS Interneuron')
show()