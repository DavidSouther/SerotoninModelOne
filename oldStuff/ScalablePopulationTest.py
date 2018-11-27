from AxonalSerotoninReceptor import *
from Neuron import *
from SomaticSerotoninReceptor import *
from oldStuff.InputIonotropicConnection import *
from oldStuff.IonotropicConnection import *

# from NetPlotter import *
# from SerotoninReceptorAxon import *

# TODO: Write utilities to manage this at the population level, like a population object that holds the neurons and the connections within population, and all the inter-population connections that originate in it?
# Then I can just create those, pass them a generator/connection pattern, hook them up to each other and inputs, and call their "SetDiffuse5htLevels" and step() methods.
# They could even manage activity summaries and plot generation of activity over time.

# TODO: Also encapsulate a run in a class, so I can define runs algorithmically and iterate through them, or define a standard test set of runs easily.

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
pyramidalParams["a"] = 0.01
pyramidalParams["b"] = 5
pyramidalParams["c"] = -60
pyramidalParams["d"] = 400
pyramidalParams["tau"] = tau
pyramidalParams["type"] = "Pyramidal"

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

popCount = 40
serotoninLevelV = 20
serotoninLevelA = 20
[inputsA1, inputsA2] = [10000, 10000]
[lambdaA1, lambdaA2] = [0.1, 0.01]
[inputsV1, inputsV2, inputsV3] = [10000, 10000, 10000]
[lambdaV1, lambdaV2, lambdaV3] = [0.1, 0.01, 0.0]

areaAVector = []
areaBVector = []

def getThetaR(population1, population2):
    pop1Sum = sum([len(neuron.spikeRecord) for neuron in population1])
    pop2Sum = sum([len(neuron.spikeRecord) for neuron in population2])
    return [(((pop2Sum - pop1Sum) / max(pop1Sum, pop2Sum)) * pi) + pi, log(max(pop1Sum, pop2Sum))]

def getAuditoryInput(theta, r):
    targetSpikeLevel = e**r
    diffSpikes = ((theta+pi) / pi) * targetSpikeLevel
    theta+pi

    if (theta-pi) >= 0:
        pop2TargetSpike = targetSpikeLevel
        pop1TargetSpike = targetSpikeLevel - diffSpikes
    else:
        pop1TargetSpike = targetSpikeLevel
        pop2TargetSpike = targetSpikeLevel + diffSpikes
    pop1Input = pop1TargetSpike * 2.3 + 250
    pop2Input = pop2TargetSpike * 2.3 + 250
    return [pop1Input, pop2Input]



pyramidalsV1 = [Neuron(pyramidalParams, tau, "PA1-" + str(i)) for i in range(popCount)]
fastSpikingsV1 = [Neuron(fsParams, tau, "FSA1-" + str(i)) for i in range(popCount)]
ltsNeuronsV1 = [Neuron(ltsParams, tau, "LTSA1-" + str(i)) for i in range(popCount)]

pyramidalsV2 = [Neuron(pyramidalParams, tau, "PA2-" + str(i)) for i in range(popCount)]
fastSpikingsV2 = [Neuron(fsParams, tau, "FSA2-" + str(i)) for i in range(popCount)]
ltsNeuronsV2 = [Neuron(ltsParams, tau, "LTSA2-" + str(i)) for i in range(popCount)]

pyramidalsV3 = [Neuron(pyramidalParams, tau, "PA3-" + str(i)) for i in range(popCount)]
fastSpikingsV3 = [Neuron(fsParams, tau, "FSA3-" + str(i)) for i in range(popCount)]
ltsNeuronsV3 = [Neuron(ltsParams, tau, "LTSA3-" + str(i)) for i in range(popCount)]

pyramidalsA1 = [Neuron(pyramidalParams, tau, "PB1-" + str(i)) for i in range(popCount)]
fastSpikingsA1 = [Neuron(fsParams, tau, "FSB1-" + str(i)) for i in range(popCount)]
ltsNeuronsA1 = [Neuron(ltsParams, tau, "LTSB1-" + str(i)) for i in range(popCount)]

pyramidalsA2 = [Neuron(pyramidalParams, tau, "PB2-" + str(i)) for i in range(popCount)]
fastSpikingsA2 = [Neuron(fsParams, tau, "FSB2-" + str(i)) for i in range(popCount)]
ltsNeuronsA2 = [Neuron(ltsParams, tau, "LTSB2-" + str(i)) for i in range(popCount)]

connections = []
inputConnections = []

# [inputsA1, inputsA2] = getAuditoryInput(-pi/2, 1)


print("Visual Inputs: ", inputsV1, ",", inputsV2, ",", inputsV3)
print("Auditory Inputs: ", inputsA1, ",",  inputsA2)

# Set up external inputs
for i in range(popCount):
    for pyramidalV1 in pyramidalsV1:
        inputConnection = InputIonotropicConnection(tau, gauss(inputsV1/popCount, (inputsV1/10)/popCount), pyramidalV1, lambdaV1)
        inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelV))
        inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalV2 in pyramidalsV2:
        inputConnection = InputIonotropicConnection(tau, gauss(inputsV2/popCount, (inputsV2/10)/popCount), pyramidalV2, lambdaV2)
        inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelV))
        inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalV3 in pyramidalsV3:
        inputConnection = InputIonotropicConnection(tau, gauss(inputsV3/popCount, (inputsV3/10)/popCount), pyramidalV3, lambdaV3)
        inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelV))
        inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalA1 in pyramidalsA1:
        inputConnection = InputIonotropicConnection(tau, gauss(inputsA1/popCount, (inputsA1/10)/popCount), pyramidalA1, lambdaA1)
        inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelA))
        inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalA2 in pyramidalsA2:
        inputConnection = InputIonotropicConnection(tau, gauss(inputsA2/popCount, (inputsA2/10)/popCount), pyramidalA2, lambdaA2)
        inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelA))
        inputConnections.append(inputConnection)

# Set up cross-modal external inputs
for i in range(popCount):
    for pyramidalV1 in pyramidalsV1:
        if random() < 0.5:
            inputConnection = InputIonotropicConnection(tau, gauss(inputsA1/popCount, (inputsA1/10)/popCount), pyramidalV1, lambdaA1)
            inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelV))
            inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalV3 in pyramidalsV3:
        if random() < 0.5:
            inputConnection = InputIonotropicConnection(tau, gauss(inputsA2/popCount, (inputsA2/10)/popCount), pyramidalV3, lambdaA2)
            inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelV))
            inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalA1 in pyramidalsA1:
        if random() < 0.5:
            inputConnection = InputIonotropicConnection(tau, gauss(inputsV1 / popCount, (inputsV1 / 10) / popCount), pyramidalA1, lambdaV1)
            inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelA))
            inputConnections.append(inputConnection)

for i in range(popCount):
    for pyramidalA2 in pyramidalsA2:
        if random() < 0.5:
            inputConnection = InputIonotropicConnection(tau, gauss(inputsV3 / popCount, (inputsV3 / 10) / popCount), pyramidalA2, lambdaV3)
            inputConnection.addAxonReceptor(AxonalSerotoninReceptor(inputConnection, "5ht2A Axonal", 0.01, serotoninLevelA))
            inputConnections.append(inputConnection)

# Set up connections in Visual Area
for pyramidalV1 in pyramidalsV1:
    # pyramidalV1.externalInput = gauss(inputsV1, inputsV1/10)
    # if random() < 0.3:
    #     pyramidalV1.externalInput += gauss(inputsA1/10, inputsA1/100)
    connections.append(IonotropicConnection(tau, 0, gauss(9000/popCount, 1000/popCount), pyramidalV1, pyramidalV1))
    for fastSpikingV1 in fastSpikingsV1:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 4000/popCount), pyramidalV1, fastSpikingV1))
        connections.append(IonotropicConnection(tau, 0, gauss(-20000/popCount, 4000/popCount), fastSpikingV1, pyramidalV1))

for ltsNeuronV1 in ltsNeuronsV1:
    for pyramidalV1 in pyramidalsV1:
        connections.append(IonotropicConnection(tau, 0, gauss(50000/popCount, 10000/popCount), pyramidalV1, ltsNeuronV1))
    for fastSpikingV1 in fastSpikingsV1:
        connections.append(IonotropicConnection(tau, 0, gauss(-50000/popCount, 10000/popCount), fastSpikingV1, ltsNeuronV1))

for pyramidal in pyramidalsV2:
    # pyramidal.externalInput = gauss(inputsV2, inputsV2/10)
    connections.append(IonotropicConnection(tau, 0, gauss(9000 / popCount, 1000 / popCount), pyramidal, pyramidal))
    for fastSpiking in fastSpikingsV2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(20000 / popCount, 4000 / popCount), pyramidal, fastSpiking))
        connections.append(
            IonotropicConnection(tau, 0, gauss(-20000 / popCount, 4000 / popCount), fastSpiking, pyramidal))

for ltsNeuron in ltsNeuronsV2:
    for pyramidal in pyramidalsV2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(50000 / popCount, 10000 / popCount), pyramidal, ltsNeuron))
    for fastSpiking in fastSpikingsV2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(-50000 / popCount, 10000 / popCount), fastSpiking, ltsNeuron))

for pyramidal in pyramidalsV3:
    # pyramidal.externalInput = gauss(inputsV3, inputsV3 / 10)
    # if random() < 0.3:
    #     pyramidal.externalInput += gauss(inputsA2/10, inputsA2/100)
    connections.append(IonotropicConnection(tau, 0, gauss(9000 / popCount, 1000 / popCount), pyramidal, pyramidal))
    for fastSpiking in fastSpikingsV3:
        connections.append(
            IonotropicConnection(tau, 0, gauss(20000 / popCount, 4000 / popCount), pyramidal, fastSpiking))
        connections.append(
            IonotropicConnection(tau, 0, gauss(-20000 / popCount, 4000 / popCount), fastSpiking, pyramidal))

for ltsNeuron in ltsNeuronsV3:
    for pyramidal in pyramidalsV3:
        connections.append(
            IonotropicConnection(tau, 0, gauss(50000 / popCount, 10000 / popCount), pyramidal, ltsNeuron))
    for fastSpiking in fastSpikingsV2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(-50000 / popCount, 10000 / popCount), fastSpiking, ltsNeuron))

# Set up connections in Auditory Area
for pyramidal in pyramidalsA1:
    # pyramidal.externalInput = gauss(inputsA1, inputsA1/10)
    # if random() < 0.3:
    #     pyramidal.externalInput += gauss(inputsV1/10, inputsV1/100)
    connections.append(IonotropicConnection(tau, 0, gauss(9000/popCount, 1000/popCount), pyramidal, pyramidal))
    for fastSpiking in fastSpikingsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 4000/popCount), pyramidal, fastSpiking))
        connections.append(IonotropicConnection(tau, 0, gauss(-20000/popCount, 4000/popCount), fastSpiking, pyramidal))

for ltsNeuron in ltsNeuronsA1:
    for pyramidal in pyramidalsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(50000/popCount, 10000/popCount), pyramidal, ltsNeuron))
    for fastSpiking in fastSpikingsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(-50000/popCount, 10000/popCount), fastSpiking, ltsNeuron))

for pyramidal in pyramidalsA2:
    # pyramidal.externalInput = gauss(inputsA2, inputsA2/10)
    # if random() < 0.3:
    #     pyramidal.externalInput += gauss(inputsV3/10, inputsV3/100)
    connections.append(IonotropicConnection(tau, 0, gauss(9000 / popCount, 1000 / popCount), pyramidal, pyramidal))
    for fastSpiking in fastSpikingsA2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(20000 / popCount, 4000 / popCount), pyramidal, fastSpiking))
        connections.append(
            IonotropicConnection(tau, 0, gauss(-20000 / popCount, 4000 / popCount), fastSpiking, pyramidal))

for ltsNeuronA2 in ltsNeuronsA2:
    for pyramidalA2 in pyramidalsA2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(50000 / popCount, 10000 / popCount), pyramidalA2, ltsNeuronA2))
    for fastSpikingA2 in fastSpikingsA2:
        connections.append(
            IonotropicConnection(tau, 0, gauss(-50000 / popCount, 10000 / popCount), fastSpikingA2, ltsNeuronA2))

# Set up long-range connections
#Visual to Auditory
for ltsNeuronV1 in ltsNeuronsV1:
    for fastSpikingA1 in fastSpikingsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronV1, fastSpikingA1))
    for pyramidalA1 in pyramidalsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronV1, pyramidalA1))
    for fastSpikingA2 in fastSpikingsA2:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronV1, fastSpikingA2))
    for pyramidalA2 in pyramidalsA2:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronV1, pyramidalA2))
for ltsNeuronV2 in ltsNeuronsV2:
    for fastSpikingA1 in fastSpikingsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronV2, fastSpikingA1))
    for pyramidalA1 in pyramidalsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronV2, pyramidalA1))
    for fastSpikingA2 in fastSpikingsA2:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronV2, fastSpikingA2))
    for pyramidalA2 in pyramidalsA2:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronV2, pyramidalA2))
for ltsNeuronV3 in ltsNeuronsV3:
    for fastSpikingA1 in fastSpikingsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronV3, fastSpikingA1))
    for pyramidalA1 in pyramidalsA1:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronV3, pyramidalA1))
    for fastSpikingA2 in fastSpikingsA2:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronV3, fastSpikingA2))
    for pyramidalA2 in pyramidalsA2:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronV3, pyramidalA2))

# Auditory to Visual
for ltsNeuronA1 in ltsNeuronsA1:
    for fastSpikingV1 in fastSpikingsV1:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronA1, fastSpikingV1))
    for pyramidalV1 in pyramidalsV1:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronA1, pyramidalV1))
    for fastSpikingV2 in fastSpikingsV2:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronA1, fastSpikingV2))
    for pyramidalV2 in pyramidalsV2:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronA1, pyramidalV2))
    for fastSpikingV3 in fastSpikingsV3:
        connections.append(IonotropicConnection(tau, 0, gauss(-40000/popCount, 4000/popCount), ltsNeuronA1, fastSpikingV3))
    for pyramidalV3 in pyramidalsV3:
        connections.append(IonotropicConnection(tau, 0, gauss(20000/popCount, 2000/popCount), ltsNeuronA1, pyramidalV3))

# Scatter 5ht Receptors About
for pyramidalV1 in pyramidalsV1:
    pyramidalV1.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalV1, "5ht2A Somatic", 10, serotoninLevelV))
    pyramidalV1.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalV1, "5ht1A Somatic", -3, serotoninLevelV))

for pyramidalV2 in pyramidalsV2:
    pyramidalV2.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalV2, "5ht2A Somatic", 10, serotoninLevelV))
    pyramidalV2.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalV2, "5ht1A Somatic", -3, serotoninLevelV))

for pyramidalV3 in pyramidalsV3:
    pyramidalV3.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalV3, "5ht2A Somatic", 10, serotoninLevelV))
    pyramidalV3.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalV3, "5ht1A Somatic", -3, serotoninLevelV))

for pyramidalA1 in pyramidalsA1:
    pyramidalA1.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalA1, "5ht2A Somatic", 10, serotoninLevelA))
    pyramidalA1.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalA1, "5ht1A Somatic", -3, serotoninLevelA))

for pyramidalA2 in pyramidalsA2:
    pyramidalA2.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalA2, "5ht2A Somatic", 10, serotoninLevelA))
    pyramidalA2.addDiffuseReceptor(SomaticSerotoninReceptor(pyramidalA2, "5ht2A Somatic", -3, serotoninLevelA))

for ltsNeuronV1 in ltsNeuronsV1:
    ltsNeuronV1.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronV1, "5ht2A Somatic", 10, serotoninLevelV))
    ltsNeuronV1.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronV1, "5ht1A Somatic", -3, serotoninLevelV))

for ltsNeuronV2 in ltsNeuronsV2:
    ltsNeuronV2.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronV2, "5ht2A Somatic", 10, serotoninLevelV))
    ltsNeuronV2.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronV2, "5ht1A Somatic", -3, serotoninLevelV))

for ltsNeuronV3 in ltsNeuronsV3:
    ltsNeuronV3.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronV3, "5ht2A Somatic", 10, serotoninLevelV))
    ltsNeuronV3.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronV3, "5ht1A Somatic", -3, serotoninLevelV))

for ltsNeuronA1 in ltsNeuronsA1:
    ltsNeuronA1.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronA1, "5ht2A Somatic", 10, serotoninLevelA))
    ltsNeuronA1.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronA1, "5ht1A Somatic", -3, serotoninLevelA))

for ltsNeuronA2 in ltsNeuronsA2:
    ltsNeuronA2.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronA2, "5ht2A Somatic", 10, serotoninLevelA))
    ltsNeuronA2.addDiffuseReceptor(SomaticSerotoninReceptor(ltsNeuronA2, "5ht1A Somatic", -3, serotoninLevelA))

for t in range(len(tspan)):
    if t%100 == 0:
        print("TimeStep", t)
    # V1
    for pyramidalV1 in pyramidalsV1:
        pyramidalV1.step()
    for fastSpikingV1 in fastSpikingsV1:
        fastSpikingV1.step()
    for ltsV1 in ltsNeuronsV1:
        ltsV1.step()

    #V2
    for pyramidalV2 in pyramidalsV2:
        pyramidalV2.step()
    for fastSpikingV2 in fastSpikingsV2:
        fastSpikingV2.step()
    for ltsV2 in ltsNeuronsV2:
        ltsV2.step()

    #V3
    for pyramidalV3 in pyramidalsV3:
        pyramidalV3.step()
    for fastSpikingV3 in fastSpikingsV3:
        fastSpikingV3.step()
    for ltsV3 in ltsNeuronsV3:
        ltsV3.step()

    #A1
    for pyramidalA1 in pyramidalsA1:
        pyramidalA1.step()
    for fastSpikingA1 in fastSpikingsA1:
        fastSpikingA1.step()
    for ltsA1 in ltsNeuronsA1:
        ltsA1.step()

    #A2
    for pyramidalA2 in pyramidalsA2:
        pyramidalA2.step()
    for fastSpikingA2 in fastSpikingsA2:
        fastSpikingA2.step()
    for ltsA2 in ltsNeuronsA2:
        ltsA2.step()

    # Inputs
    for connection in inputConnections:
        connection.step()

sumV1P = sum([len(neuron.spikeRecord) for neuron in pyramidalsV1])
sumV1FS = sum([len(neuron.spikeRecord) for neuron in fastSpikingsV1])
sumV1LTS = sum([len(neuron.spikeRecord) for neuron in ltsNeuronsV1])
sumV2P = sum([len(neuron.spikeRecord) for neuron in pyramidalsV2])
sumV2FS = sum([len(neuron.spikeRecord) for neuron in fastSpikingsV2])
sumV2LTS = sum([len(neuron.spikeRecord) for neuron in ltsNeuronsV2])
sumV3P = sum([len(neuron.spikeRecord) for neuron in pyramidalsV3])
sumV3FS = sum([len(neuron.spikeRecord) for neuron in fastSpikingsV3])
sumV3LTS = sum([len(neuron.spikeRecord) for neuron in ltsNeuronsV3])
sumA1P = sum([len(neuron.spikeRecord) for neuron in pyramidalsA1])
sumA1FS = sum([len(neuron.spikeRecord) for neuron in fastSpikingsA1])
sumA1LTS = sum([len(neuron.spikeRecord) for neuron in ltsNeuronsA1])
sumA2P = sum([len(neuron.spikeRecord) for neuron in pyramidalsA2])
sumA2FS = sum([len(neuron.spikeRecord) for neuron in fastSpikingsA2])
sumA2LTS = sum([len(neuron.spikeRecord) for neuron in ltsNeuronsA2])



print("Visual Inputs: ", inputsV1, ",", inputsV2, ",", inputsV3)
print("Auditory Inputs: ", inputsA1, ",",  inputsA2)

print("\nRESULTS")

print("\nV1: ", sumV1P, ",", sumV1FS, ",", sumV1LTS)
print("V2: ", sumV2P, ",", sumV2FS, ",", sumV2LTS)
print("V3: ", sumV3P, ",", sumV3FS, ",", sumV3LTS)

print("\nA1: ", sumA1P, ",", sumA1FS, ",", sumA1LTS)
print("A2: ", sumA2P, ",", sumA2FS, ",", sumA2LTS)

print("Auditory Direction (Polar Coordinates): ", getThetaR(pyramidalsA1, pyramidalsA2))



#
#
# pyramidalVoltages = [pyramidalsV1[i].vv for i in range(len(pyramidalsV1))]
# pyramidalUU = [pyramidalsV1[i].uu for i in range(len(pyramidalsV1))]
# pyramidalII = [pyramidalsV1[i].ii for i in range(len(pyramidalsV1))]
# fastSpikingVoltages = [fastSpikingsV1[i].vv for i in range(len(fastSpikingsV1))]
# fastSpikingUU = [fastSpikingsV1[i].uu for i in range(len(fastSpikingsV1))]
# fastSpikingII = [fastSpikingsV1[i].ii for i in range(len(fastSpikingsV1))]
# ltsVoltages = [ltsNeuronsV1[i].vv for i in range(len(ltsNeuronsV1))]
# ltsUU = [ltsNeuronsV1[i].uu for i in range(len(ltsNeuronsV1))]
# ltsII = [ltsNeuronsV1[i].ii for i in range(len(ltsNeuronsV1))]
# pyramidalVoltages2 = [pyramidalsA1[i].vv for i in range(len(pyramidalsA1))]
# pyramidalUU2 = [pyramidalsA1[i].uu for i in range(len(pyramidalsA1))]
# pyramidalII2 = [pyramidalsA1[i].ii for i in range(len(pyramidalsA1))]
# fastSpikingVoltages2 = [fastSpikingsA1[i].vv for i in range(len(fastSpikingsA1))]
# ltsVoltages2 = [ltsNeuronsA1[i].vv for i in range(len(ltsNeuronsA1))]
#
# # plot(tspan, pyramidals[0].vv)
# # # plot(tspan, cell1.uu)
# # title('Pyramidal Cell 0')
# #
# figure()
# pcolor(pyramidalVoltages, vmin=-100, vmax=60)
# colorbar()
# title('Pyramidal Cells')
# #
# # figure()
# # pcolor(pyramidalUU)
# # colorbar()
# # title('Pyramidal UU')
# #
# # figure()
# # pcolor(pyramidalII)
# # colorbar()
# # title('Pyramidal II')
# #
# figure()
# pcolor(pyramidalVoltages2, vmin=-100, vmax=60)
# colorbar()
# title('Pyramidal Cells 2')
# #
# # figure()
# # pcolor(pyramidalUU2)
# # colorbar()
# # title('Pyramidal UU 2')
# #
# # figure()
# # pcolor(pyramidalII2)
# # colorbar()
# # title('Pyramidal II 2')
# #
# figure()
# pcolor(fastSpikingVoltages, vmin=-100, vmax=60)
# colorbar()
# title('FS Interneurons')
# #
# # figure()
# # pcolor(fastSpikingUU)
# # colorbar()
# # title('FS UU')
# #
# # figure()
# # pcolor(fastSpikingII)
# # colorbar()
# # title('FS II')
# #
# figure()
# pcolor(fastSpikingVoltages2, vmin=-100, vmax=60)
# colorbar()
# title('FS Interneurons 2')
#
# figure()
# plot(tspan, fastSpikingsV1[0].vv)
# title('FS Interneuron 0')
#
# figure()
# pcolor(ltsVoltages, vmin=-100, vmax=60)
# colorbar()
# title('LTS Interneurons')
# #
# # figure()
# # pcolor(ltsUU)
# # colorbar()
# # title('LTS UU')
# #
# # figure()
# # pcolor(ltsII)
# # colorbar()
# # title('LTS II')
# #
# figure()
# pcolor(ltsVoltages2, vmin=-100, vmax=60)
# colorbar()
# title('LTS Interneurons 2')
#
# # np = NetPlotter(connections)
# # np.plot()
#
# show()
#
