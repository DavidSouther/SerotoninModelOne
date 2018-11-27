from Neuron import *
from pylab import *
from random import gauss

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
pyramidalParams["a"] = 0.01
pyramidalParams["b"] = 5
pyramidalParams["c"] = -60
pyramidalParams["d"] = 400
pyramidalParams["tau"] = tau
pyramidalParams["type"] = "Pyramidal"

popCount = 40


spikeRates = []
for inputLevel in range(0, 2000, 50):
    pyramidals = [Neuron(pyramidalParams, "P-" + str(i)) for i in range(popCount)]
    for pyramidal in pyramidals:
        pyramidal.externalInput = gauss(inputLevel, 0.0)
    for t in range(len(tspan)):
        for pyramidal in pyramidals:
            pyramidal.step()
    spikeRates.append(sum([len(neuron.spikeRecord) for neuron in pyramidals]))
    print("Input ", inputLevel, ":", sum([len(neuron.spikeRecord) for neuron in pyramidals]))

figure()
plot(range(0, 2000, 50), spikeRates)
title('Pyr. Rate by Input, Population:' + str(popCount))
show()