import os

from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_integer("max_time", 100, "Number of miliseconds per phase.")
flags.DEFINE_float("tau", 0.1, "Milisecond subdivision resolution.")
flags.DEFINE_integer("population_count", 20, "Number of neurons per population")

# Because this will often run in Docker, we can either set parameters using the environment, or using flags.
# Because of the number of parameter flags, it's expected that a --flagfile would be used. This can be
# generated programmatically across a number of criteria.

def get_max_time():
    try:
        return os.environ["MAX_TIME"]
    except:
        return FLAGS.max_time

def get_tau():
    try:
        return os.environ["TAU"]
    except:
        return FLAGS.tau

def get_pop_count():
    try:
        return os.environ["POPULATION_COUNT"]
    except:
        return FLAGS.population_count

def loadParams():
    params = {}
    # Time Parameters
    params["maxTime"] = get_max_time()
    params["tau"] = get_tau()

    # Population and Connection Parameters
    params["popCount"] = get_pop_count()

    params["pyramidalSelfExcitationWeight"] = 25
    params["pyramidalToPyramidalWeight"] = 50
    params["pyramidalToPyramidalLikelihood"] = 0.3
    params["PyramidalsToFSWeight"] = 35
    params["FSToPyramidalsWeight"] = -100
    params["PyramidalsToLTSWeight"] = 20 #500
    params["LTStoFSWeight"] = -50
    params["LTStoPyramidalsWeight"] = -50

    ## Regular
    # Input Paramters
    params["inputWeightA"] = 50
    params["inputWeightB"] = 50
    params["rateA"] = 1
    params["rateB"] = 1
    params["inputWeightAB"] = 25
    params["crossModalABLikelihood"] = 0.5
    params["inputWeightBA"] = 25 #7500
    params["crossModalBALikelihood"] = 0.5

    # Diffuse Neurotransmitter Paramters
    params["serotoninLevelA"] = 10
    params["serotoninLevelB"] = 10
    params["Somatic5HT2AWeight"] = 85
    params["Somatic5HT2AWeightLTS"] = 81
    params["Somatic5HT1AWeight"] = -80
    params["Axonal5HT2AWeight"] = 0.4
    params["Axonal5HT1AWeight"] = -0.4

    return params