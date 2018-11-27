from pylab import *

from oldStuff import IonotropicConnection, Pyramidal

# Time
tau = 0.25
tspan = arange(0,300, tau)
T1=len(tspan)/5

#Parameters
params = {}
params["a"]=0.02
params["b"]=0.25
params["c"]=-65
params["d"]=6;
params["tau"] = tau
params["V0"] = -65

populationA = [Pyramidal.PyramidalCell(params) for i in range(10)]
populationB = [Pyramidal.PyramidalCell(params) for i in range(10)]
populationIlA =
populationIgA =
populationIlB =
populationIgB =

inputConnections =

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