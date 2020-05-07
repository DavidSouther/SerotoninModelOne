import os
import sys
from absl import flags 
from absl import logging
from matplotlib.pyplot import colorbar 
from matplotlib.pyplot import figure
from matplotlib.pyplot import pcolor 
from matplotlib.pyplot import plot
from matplotlib.pyplot import savefig
from matplotlib.pyplot import subplot 
from matplotlib.pyplot import title 
from numpy import arange
from numpy import zeros

from network.TwoColumnNetwork import TwoColumnNetwork

FLAGS = flags.FLAGS

def get_default_figures_directory():
    try:
        return os.environ["FIGURES_DIRECTORY"]
    except:
        return os.path.join(os.curdir, "figures")

flags.DEFINE_string("figures_directory", get_default_figures_directory(), "Directory relative to the running directory to save figures.")
flags.DEFINE_integer("steps_between_timing_debug", 10, "Number of steps to log progress after")

class TwoColumnSimulation():
    def __init__(self, params):
        self.params = params
        self.tau = params["tau"]
        self.network = TwoColumnNetwork(self.tau, self, self.params, "Test Network1")

    def runPhase(self, phase):
        maxTime = self.params["maxTime"]
        tau = self.tau
        start = maxTime * (phase - 1)
        end = maxTime * phase
        tspan = arange(start, end, tau)
        for t in tspan:
            if t % FLAGS.steps_between_timing_debug == 0:
                logging.debug("Phase 1 step: %d" % t)
            self.network.step()

    def phase1(self):
        logging.info("Phase One, full input")
        self.runPhase(1)

    def phase2(self):
        logging.info("Phase Two, sensory deprivation")
        for inputCell in self.network.populations["InputA"].cells:
            inputCell.poissonLambda = 0
        self.runPhase(2)

    def phase3(self):
        # Third portion
        logging.info("Phase Three, Serotonin and Plasticity")
        self.weightMatrixPriorBA = zeros([self.params["popCount"], self.params["popCount"]])
        for x in range(len(self.network.populations["InputB"].cells)):
            for y in range(len(self.network.populations["pyramidalsA"].cells)):
                for source in self.network.populations["InputB"].cells[x].outputs:
                    if source.target == self.network.populations["pyramidalsA"].cells[y]:
                        self.weightMatrixPriorBA[x,y] = source.postSynapticReceptors[0].weight

        # Increase 5HT
        transmittersA = {}
        transmittersA["5HT2A"] = 30
        transmittersA["5HT1A"] = 30
        self.network.setSerotoninA(transmittersA)

        # Turn on plasticity
        for x in range(len(self.network.populations["InputB"].cells)):
            for y in range(len(self.network.populations["pyramidalsA"].cells)):
                for source in self.network.populations["InputB"].cells[x].outputs:
                    if source.target == self.network.populations["pyramidalsA"].cells[y]:
                        source.postSynapticReceptors[0].plasticity = True
                        source.postSynapticReceptors[0].c_p = 180.3

        self.runPhase(3)

        self.weightMatrixPostBA = zeros([self.params["popCount"], self.params["popCount"]])
        for x in range(len(self.network.populations["InputB"].cells)):
            for y in range(len(self.network.populations["pyramidalsA"].cells)):
                for source in self.network.populations["InputB"].cells[x].outputs:
                    if source.target == self.network.populations["pyramidalsA"].cells[y]:
                        self.weightMatrixPostBA[x,y] = source.postSynapticReceptors[0].weight

    def phase4(self):
        logging.info("Phase Four, remapped functionality.")
        # Turn off plasticity
        for x in range(len(self.network.populations["InputB"].cells)):
            for y in range(len(self.network.populations["pyramidalsA"].cells)):
                for source in self.network.populations["InputB"].cells[x].outputs:
                    if source.target == self.network.populations["pyramidalsA"].cells[y]:
                        source.postSynapticReceptors[0].plasticity = False

        transmittersA = {}
        transmittersA["5HT2A"] = 40
        transmittersA["5HT1A"] = 40
        self.network.setSerotoninA(transmittersA)
        self.runPhase(4)

    def run(self):
        self.nextFigure = 1
        self.phase1()
        self.phase2()
        self.phase3()
        self.phase4()

    def getFigureName(self, name):
        fig = self.nextFigure
        self.nextFigure += 1
        fullName = "fig_%s_%s" % (str(fig).zfill(2), name)
        return fullName

    def savefig(self, name):
        fullName = self.getFigureName(name)
        path = os.path.join(FLAGS.figures_directory, fullName)
        logging.info("Writing figure to %s" % path)
        savefig(path)
        # TODO(davidsouther):
        #     *   Generate a path name based on the run
        #     *   Upload the written file to gs://serotonin

    def prepareOutput(self):
        if not os.path.exists(FLAGS.figures_directory):
            os.makedirs(FLAGS.figures_directory)

    def plotColumns(self):
        self.prepareOutput()

        figure()
        pcolor(self.weightMatrixPriorBA)
        colorbar()
        title('Before Phase 3 Weights from Input B to Pyramidals A')
        self.savefig('weights_before_phase_3.png')

        figure()
        pcolor(self.weightMatrixPostBA)
        colorbar()
        title('After Phase 3 Weights from Input B to Pyramidals A')
        self.savefig('weights_after_phase_3.png')

        inputAVoltages = [c.vv for c in self.network.populations["InputA"].cells]
        inputBVoltages = [c.vv for c in self.network.populations["InputB"].cells]

        aPyramidalVoltages = [c.vv for c in self.network.populations["pyramidalsA"].cells]
        aFSVoltages = [c.vv for c in self.network.populations["fastSpikingsA"].cells]
        aLTSVoltages = [c.vv for c in self.network.populations["lowThresholdsA"].cells]

        bPyramidalVoltages = [c.vv for c in self.network.populations["pyramidalsB"].cells]
        bFSVoltages = [c.vv for c in self.network.populations["fastSpikingsB"].cells]
        bLTSVoltages = [c.vv for c in self.network.populations["lowThresholdsB"].cells]

        # Sliding Windowed Spike Rates
        figure()
        subplot(4, 1, 1)
        plot(self.network.populations["InputA"].rateRecord)
        title('A Input')

        subplot(4, 1, 2)
        plot(self.network.populations["pyramidalsA"].rateRecord)
        title('A Pyramidal Cells')

        subplot(4, 1, 3)
        plot(self.network.populations["fastSpikingsA"].rateRecord)
        title('A FS Cells')

        subplot(4, 1, 4)
        plot(self.network.populations["lowThresholdsA"].rateRecord)
        title('A LTS Cells')
        self.savefig('column_a_spike_rates.png')

        figure()
        subplot(4, 1, 1)
        plot(self.network.populations["InputB"].rateRecord)
        title('B Input')

        subplot(4, 1, 2)
        plot(self.network.populations["pyramidalsB"].rateRecord)
        title('B Pyramidal Cells')

        subplot(4, 1, 3)
        plot(self.network.populations["fastSpikingsB"].rateRecord)
        title('B FS Cells')

        subplot(4, 1, 4)
        plot(self.network.populations["lowThresholdsB"].rateRecord)
        title('B LTS Cells')

        self.savefig('column_b_spike_rates.png')

        figure()
        subplot(4, 1, 1)
        pcolor(inputAVoltages, vmin=-100, vmax=60)
        colorbar()
        title('A Input')

        subplot(4, 1, 2)
        pcolor(aPyramidalVoltages, vmin=-100, vmax=60)
        colorbar()
        title('A Pyramidal Cells')

        subplot(4, 1, 3)
        pcolor(aFSVoltages, vmin=-100, vmax=60)
        colorbar()
        title('A FS Cells')

        subplot(4, 1, 4)
        pcolor(aLTSVoltages, vmin=-100, vmax=60)
        colorbar()
        title('A LTS Cells')

        self.savefig('column_a_voltages.png')

        figure()
        subplot(4, 1, 1)
        pcolor(inputBVoltages, vmin=-100, vmax=60)
        colorbar()
        title('B Input')

        subplot(4, 1, 2)
        pcolor(bPyramidalVoltages, vmin=-100, vmax=60)
        colorbar()
        title('B Pyramidal Cells')

        subplot(4, 1, 3)
        pcolor(bFSVoltages, vmin=-100, vmax=60)
        colorbar()
        title('B FS Cells')

        subplot(4, 1, 4)
        pcolor(bLTSVoltages, vmin=-100, vmax=60)
        colorbar()
        title('B LTS Cells')
        self.savefig('column_b_voltages.png')

        numax = len(self.network.populations["InputB"].outboundAxons)
        timeSpan = len(self.network.populations["InputB"].rateRecord)
        baSpikeFailures = zeros((numax, timeSpan))
        axNum = 0
        for ax in self.network.populations["InputB"].outboundAxons:
            baSpikeFailures[axNum, :] = ax.spikeFailures
            axNum += 1

        figure()
        pcolor(baSpikeFailures, cmap="Greys")
        self.savefig('ba_spike_failures.png')
