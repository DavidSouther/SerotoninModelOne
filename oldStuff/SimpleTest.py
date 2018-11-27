from pylab import *

from oldStuff import IonotropicConnection, Pyramidal

# Time
tau = 0.25
tspan = arange(0,300, tau)
T1=len(tspan)/5

#Parameters
pyramidalParams = {}
pyramidalParams["C"]= 100
pyramidalParams["k"] = 3
pyramidalParams["v_r"] = -60
pyramidalParams["v_t"] = -50
pyramidalParams["v_peak"] = 50
pyramidalParams["g_up"] = 3.0
pyramidalParams["g_down"] = 5.0
pyramidalParams["a"] = 0.01
pyramidalParams["b"] = 5
pyramidalParams["c"] = -60
pyramidalParams["d"] = 400



# pyramidalParams["a"]=0.02
# pyramidalParams["b"]=0.25
# pyramidalParams["c"]=-65
# pyramidalParams["d"]=6
# pyramidalParams["tau"] = tau
# pyramidalParams["V0"] = -65

fastSpikingParams = {}
params["a"]=0.02
params["b"]=0.25
params["c"]=-65
params["d"]=6
params["tau"] = tau
params["V0"] = -65

lowThresholdSpikingParams = {}
params["a"]=0.02
params["b"]=8
params["c"]=-65
params["d"]=6
params["tau"] = tau
params["V0"] = -56



cell1 = Pyramidal.PyramidalCell(params)
cell2 = Pyramidal.PyramidalCell(params)
connection = IonotropicConnection.IonotropicConnection(tau, 0, 30.0, cell1, cell2)



cell1.externalInput = 10.0

for t in range(len(tspan)):
    cell1.step()
    cell2.step()
    connection.step()

plot(tspan, cell1.VV)
plot(tspan, cell2.VV)
title('Coupled Cells')
show()