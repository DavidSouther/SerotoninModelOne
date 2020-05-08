import os

from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer("maxTime", 100, "Number of miliseconds per phase.")
flags.DEFINE_float("tau", 0.1, "Milisecond subdivision resolution.")
flags.DEFINE_integer("popCount", 20, "Number of neurons per population")

flags.DEFINE_float("pyramidalSelfExcitationWeight", 25, "pyramidalSelfExcitationWeight")
flags.DEFINE_float("pyramidalToPyramidalWeight", 50, "pyramidalToPyramidalWeight")
flags.DEFINE_float("pyramidalToPyramidalLikelihood", 0.3, "pyramidalToPyramidalLikelihood")
flags.DEFINE_float("PyramidalsToFSWeight", 35, "PyramidalsToFSWeight")
flags.DEFINE_float("FSToPyramidalsWeight", -100, "FSToPyramidalsWeight")
flags.DEFINE_float("PyramidalsToLTSWeight", 20, "PyramidalsToLTSWeight")
flags.DEFINE_float("LTStoFSWeight", -50, "LTStoFSWeight")
flags.DEFINE_float("LTStoPyramidalsWeight", -50, "LTStoPyramidalsWeight")

flags.DEFINE_float("inputWeightA", 50, "inputWeightA")
flags.DEFINE_float("inputWeightB", 50, "inputWeightB")
flags.DEFINE_float("rateA", 1, "rateA")
flags.DEFINE_float("rateB", 1, "rateB")
flags.DEFINE_float("inputWeightAB", 25, "inputWeightAB")
flags.DEFINE_float("crossModalABLikelihood", 0.5, "crossModalABLikelihood")
flags.DEFINE_float("inputWeightBA", 25, "inputWeightBA")
flags.DEFINE_float("crossModalBALikelihood", 0.5, "crossModalBALikelihood")

flags.DEFINE_float("serotoninLevelA", 10, "serotoninLevelA")
flags.DEFINE_float("serotoninLevelB", 10, "serotoninLevelB")
flags.DEFINE_float("Somatic5HT2AWeight", 85, "Somatic5HT2AWeight")
flags.DEFINE_float("Somatic5HT2AWeightLTS", 81, "Somatic5HT2AWeightLTS")
flags.DEFINE_float("Somatic5HT1AWeight", -80, "Somatic5HT1AWeight")
flags.DEFINE_float("Axonal5HT2AWeight", 0.4, "Axonal5HT2AWeight")
flags.DEFINE_float("Axonal5HT1AWeight", -0.4, "Axonal5HT1AWeight")
    
def loadParams():
    params = {}
    # Time Parameters
    params["maxTime"] = FLAGS.maxTime
    params["tau"] = FLAGS.tau

    # Population and Connection Parameters
    params["popCount"] = FLAGS.popCount

    params["pyramidalSelfExcitationWeight"] = FLAGS.pyramidalSelfExcitationWeight
    params["pyramidalToPyramidalWeight"] = FLAGS.pyramidalToPyramidalWeight
    params["pyramidalToPyramidalLikelihood"] = FLAGS.pyramidalToPyramidalLikelihood
    params["PyramidalsToFSWeight"] = FLAGS.PyramidalsToFSWeight
    params["FSToPyramidalsWeight"] = FLAGS.FSToPyramidalsWeight
    params["PyramidalsToLTSWeight"] = FLAGS.PyramidalsToLTSWeight
    params["LTStoFSWeight"] = FLAGS.LTStoFSWeight
    params["LTStoPyramidalsWeight"] = FLAGS.LTStoPyramidalsWeight

    ## Regular
    # Input Paramters
    params["inputWeightA"] = FLAGS.inputWeightA
    params["inputWeightB"] = FLAGS.inputWeightB
    params["rateA"] = FLAGS.rateA
    params["rateB"] = FLAGS.rateB
    params["inputWeightAB"] = FLAGS.inputWeightAB
    params["crossModalABLikelihood"] = FLAGS.crossModalABLikelihood
    params["inputWeightBA"] = FLAGS.inputWeightBA
    params["crossModalBALikelihood"] = FLAGS.crossModalBALikelihood

    # Diffuse Neurotransmitter Paramters
    params["serotoninLevelA"] = FLAGS.serotoninLevelA
    params["serotoninLevelB"] = FLAGS.serotoninLevelB
    params["Somatic5HT2AWeight"] = FLAGS.Somatic5HT2AWeight
    params["Somatic5HT2AWeightLTS"] = FLAGS.Somatic5HT2AWeightLTS
    params["Somatic5HT1AWeight"] = FLAGS.Somatic5HT1AWeight
    params["Axonal5HT2AWeight"] = FLAGS.Axonal5HT2AWeight
    params["Axonal5HT1AWeight"] = FLAGS.Axonal5HT1AWeight

    return params