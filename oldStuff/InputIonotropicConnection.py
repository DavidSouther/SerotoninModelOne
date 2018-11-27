from __future__ import division
from scipy.stats import poisson
from random import random


'''
Created on September 12, 2018

A class which handles a transmission queue, weight, and STDP if needed.

@author: Stefan Berteau
'''

class InputIonotropicConnection:
    def __init__(self, timeStep, weight, target, inputLambda, width=0.1, myelin=0.1, debug = False):
        self.weight = weight
        self.spikes = [] # Spikes currently traveling down the axon

        self.distribution = poisson(inputLambda)

        self.target = target

        self.failureRate = 0.1

        self.diffuseReceptors = []

        # self.target.addInput(self)

        self.time = 0
        self.timeStep = timeStep
        self.width = width
        self.myelin = myelin
        self.speed = (self.width ** (2 - self.myelin)) * 1000 # determine conduction velocity
        self.debug = debug

        if self.debug:
            print(self.source.type, "connected to ", self.target.type)

    def addAxonReceptor(self, receptor):
        self.diffuseReceptors.append(receptor)

    def enqueue(self):
        if random() > self.failureRate:
            if self.debug:
                print(self.source.type, "spiked!  Transmitting ", self.weight, "to ", self.target.type)
            self.target.addSynapticTransmission(self.weight)
        # self.spikes.append(0)

    def step(self):
        self.time += self.timeStep
        if self.distribution.rvs((1,))[0] > 0:
            self.enqueue()

    #     self.speed = (self.width ** (2 - self.myelin)) * 1000
    #     self.spikes = [self.spikes[i] + (self.timeStep / self.speed) for i in range(len(self.spikes))]
    #     while len(self.spikes) > 0 and max(self.spikes) > self.length:
    #         # print('SYNAPTIC TRANSMISSION!')
    #         self.spikes.remove(max(self.spikes))
    #         self.target.addSynapticTransmission(self.weight)

        # TODO: Add Voltage dependent stdp here.