from random import gauss
from pylab import *
from scipy import *
from numpy import *

'''
Created on Jan 7, 2011

M-current enabled variant on the Izhikevich quadratic integrate-and-fire neuron

@author: stefan
'''

class Neuron:
    def __init__(self, tau, parameters, name, inputs=None, outputs=None, diffuseTransmitters = None, externalInput = 0.0, parentPopulation=None, debug=False):

        self.name = name
        self.originalParameters = parameters

        self.a = self.originalParameters["a"]
        self.b = self.originalParameters["b"]
        self.c = self.originalParameters["c"]
        self.d = self.originalParameters["d"]
        self.v = self.originalParameters["v_r"] + gauss(0,20)
        self.v_r = self.originalParameters["v_r"]
        self.v_t = self.originalParameters["v_t"]
        self.k = self.originalParameters["k"]
        self.C = self.originalParameters["C"]
        self.v_peak = self.originalParameters["v_peak"]

        self.tau = tau

        if inputs is None:
            self.inputs = []
        else:
            self.inputs = inputs

        if outputs is None:
            self.outputs = []
        else:
            self.outputs = outputs

        self.parentPopulation = parentPopulation

        self.time = 0
        self.debug = debug
        self.type = parameters["type"]

        # Init Variables and membrane equations
        self.u = gauss(self.d, self.d/6) #self.b*self.v
        self.dvdt = lambda v, u: (self.k * (v - self.v_r) * (v - self.v_t) - u + self.I) / self.C
        self.dudt = lambda v, u: (self.a * (self.b * (v - self.v_r) - u))

        # Input
        self.externalInput = externalInput
        self.synapticInput = 0
        self.postSynapticReceptors = []
        self.diffuseReceptors = []
        if diffuseTransmitters is None:
            self.diffuseTransmitters = {}
        else:
            self.diffuseTransmitters = diffuseTransmitters
        self.diffuseCurrent = 0
        self.I = 0

        # Recording variables
        self.vv=[]
        self.uu=[]
        self.bb=[]
        self.ii=[]
        self.spikeRecord=[]

    def registerPostSynapticReceptor(self, receptor):
        self.postSynapticReceptors.append(receptor)

    def addDiffuseReceptor(self, receptor):
        self.diffuseReceptors.append(receptor)
        receptor.setTarget(self)

    def updateDiffuseTransmitters(self, diffuseTransmitters):
        self.diffuseTransmitters = diffuseTransmitters
        # Update somatic diffuse receptor levels
        for somaticReceptor in self.diffuseReceptors:
            try:
                somaticReceptor.setLevel(self.diffuseTransmitters[somaticReceptor.getTypeString()]) # Set the level to be whatever matches it in the passed dictionary
            except KeyError:
                print("WARNING: There are somatic receptors of type " + somaticReceptor.getTypeString() + " on neuron " + self.name + " in population " + self.parentPopulation.name + ", which does not currently have any transmitter levels set for that type.  Defaulting to a level of 0.0")
                somaticReceptor.setLevel(0.0)

        # Reset Diffuse Current and Neural Parameters
        self.diffuseCurrent = 0
        self.a = self.originalParameters["a"]
        self.b = self.originalParameters["b"]
        self.c = self.originalParameters["c"]
        self.d = self.originalParameters["d"]
        self.v_r = self.originalParameters["v_r"]
        self.v_t = self.originalParameters["v_t"]
        self.k = self.originalParameters["k"]
        self.C = self.originalParameters["C"]
        self.v_peak = self.originalParameters["v_peak"]

        # Run re-run all diffuse receptors
        for somaticReceptor in self.diffuseReceptors:
            somaticReceptor.doActivity()

    def setInputs(self, inputs):
        self.inputs = inputs
        
    def addInput(self, inputSynapse):
        self.inputs.append(inputSynapse)

    def setInjectedCurrent(self, current):
        if isinstance(current, (int, float)):
            self.externalInput = current
        else:
            raise ValueError("Error: setInjectedCurrent requires an int or float type, representing current in picoamperes")
        
    def getInputs(self):
        return self.inputs
    
    def setOutputs(self, outputs):
        self.outputs = outputs
        
    def addOutput(self, outputAxon):
        self.outputs.append(outputAxon)
        
    def getOutputs(self):
        return self.outputs

    def addSynapticTransmission(self, current):
        if self.debug:
            print("INCOMING SPIKE!")
        self.synapticInput += current

    def rk4OneStep(self, dvdt, dudt, v, u, h):
        k1 = h * (dvdt(v, u))
        l1 = h * (dudt(v, u))
        k2 = h * (dvdt(v + 0.5 * k1, u + 0.5 * l1))
        l2 = h * (dudt(v + 0.5 * k1, u + 0.5 * l1))
        k3 = h * (dvdt(v + 0.5 * k2, u + 0.5 * l2))
        l3 = h * (dudt(v + 0.5 * k2, u + 0.5 * l2))

        k4 = h * dvdt(v + k3, u + l3)
        l4 = h * dudt(v + k3, u + l3)

        k = (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        l = (1 / 6) * (l1 + 2 * l2 + 2 * l3 + l4)

        return ([k, l])

    def step(self):
        self.time += self.tau

        self.I = self.externalInput + self.synapticInput + self.diffuseCurrent
        self.ii.append(self.I)

        # Euler
        # self.v = self.v + self.tau*(self.k*(self.v-self.v_r)*(self.v-self.v_t)-self.u+self.I)/self.C
        # self.u = self.u + self.tau*(self.a*(self.b*(self.v-self.v_r)-self.u))
        ## Uncomment this line if you want to simulate M-Currents
        ## self.b = self.b + ((0.25-self.b) + (0.02 - self.b)*(max((self.V + 67),0)))/100

        # Runge-Kutta
        [dv, du] = self.rk4OneStep(self.dvdt, self.dudt, self.v, self.u, self.tau)
        self.v = self.v + dv
        self.u = self.u + du

        if self.v > self.v_peak: # Spike
            self.spikeRecord.append([self.time,1])
            self.v = self.c
            self.u = self.u + self.d
            if self.debug:
                print("SPIKE!")
            for axon in self.outputs:
                axon.enqueue()
        if self.u > 500:
            self.u = 500
        self.vv.append(self.v)
        self.bb.append(self.b)
        self.uu.append(self.u)
        self.synapticInput = 0
        # self.diffuseCurrent = 0

    def getState(self):
        vars = {}
        vars["V"] = self.v
        vars["u"] = self.u
        vars["b"] = self.b
        return vars