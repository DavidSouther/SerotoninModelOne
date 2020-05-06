from absl import app
from absl import flags
import sys

from network import TestTwoColumnNetwork 


sys.setrecursionlimit(10000)

FLAGS = flags.FLAGS

flags.DEFINE_string("mode", "PLOT", "Mode to execute. PLOT to run and plot an output, wihout saving an intermediate simulation. RUN for running the simulation & saving a pickled output, WRITE to read a pickled output and generate figures.")
flags.DEFINE_string("picklejar", "two_column_simulation.pickle", "Filename to write simulation to or read simulation from.")

def main(argv):
    if FLAGS.mode == "PLOT":
        sim = TestTwoColumnNetwork.runSim()
        TestTwoColumnNetwork.plotSim(sim)
    if FLAGS.mode == "RUN":
        sim = TestTwoColumnNetwork.runSim()
        TestTwoColumnNetwork.writeSim(sim)
    if FLAGS.mode == "WRITE":
        sim = TestTwoColumnNetwork.readSim()
        TestTwoColumnNetwork.plotSim(sim)

if __name__ == '__main__':
    app.run(main)
