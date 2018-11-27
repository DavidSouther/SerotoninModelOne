from __future__ import division
'''
Created on Jan 7, 2011

M-current enabled variant on the Izhikevich quadratic integrate-and-fire neuron

@author: stefan
'''

from pylab import *
from scipy import *
from numpy import *

class FastSpikingCell:
    def __init__(self, parameters, inputs=[], outputs=[], externalInput = 0.0, debug=False):
        self.a = parameters["a"]
        self.b = parameters["b"]
        self.c = parameters["c"]
        self.d = parameters["d"]
        self.tau = parameters["tau"]
        self.V = parameters["V0"]
        self.inputs = inputs
        self.outputs = outputs
        self.time = 0

        # Init Variables
        self.u=self.b*self.V

        # Input
        self.externalInput = externalInput
        self.synapticInput = 0

        # Time
        self.tau = 0.25

        # Recording variables
        self.VV=[]
        self.uu=[]
        self.bb=[]
        self.ii=[]
        self.spikeRecord=[]


    def setInputs(self, inputs):
        self.inputs = inputs
        
    def addInput(self, input):
        self.inputs.append(input)
        
    def getInputs(self):
        return self.inputs
    
    def setOutputs(self, outputs):
        self.outputs = outputs
        
    def addOutput(self, output):
        self.outputs.append(output)
        
    def getOutputs(self):
        return self.outputs

    def addSynapticTransmission(self, current):
        self.synapticInput += current

    def step(self):
        self.time += self.tau
        I = self.externalInput + self.synapticInput
        self.V = self.V + self.tau*(0.04*self.V**2+5*self.V+140-self.u+I)
        self.u = self.u +self.tau*self.a*(self.b*self.V-self.u)
        # Uncomment this line if you want to simulate M-Currents
        # self.b = self.b + ((0.25-self.b) + (0.02 - self.b)*(max((self.V + 67),0)))/100
        if self.V > 30: # Spike
            self.spikeRecord.append([self.time,1])
            self.V = self.c
            self.u = self.u + self.d
            for axon in self.outputs:
                axon.enqueue()
        self.VV.append(self.V)
        self.bb.append(self.b)
        self.uu.append(self.u)
        self.synapticInput = 0

    def getState(self):
        vars = {}
        vars["V"] = self.V
        vars["u"] = self.u
        vars["b"] = self.b
        return vars