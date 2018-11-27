from TwoColumnSimulation import *
import winsound

params = {}
# Time Parameters
params["maxTime"] = 100
params["tau"] = 0.1

# Population and Connection Parameters
params["popCount"] = 40
params["pyramidalSelfExcitationWeight"] = 50000
params["pyramidalToPyramidalWeight"] = 50000
params["pyramidalToPyramidalLikelihood"] = 0.25
params["PyramidalsToFSWeight"] = 50000
params["FSToPyramidalsWeight"] = -30000
params["PyramidalsToLTSWeight"] = 80000
params["LTStoFSWeight"] = -30000
params["LTStoPyramidalsWeight"] = -5000

# Input Paramters
params["inputWeightA"] = 2400
params["inputWeightB"] = 2400
params["rateA"] = 20
params["rateB"] = 20
params["inputWeightAB"] = 1200
params["crossModalABLikelihood"] = 0.3
params["inputWeightBA"] = 800 #7500
params["crossModalBALikelihood"] = 0.3

# Diffuse Neurotransmitter Paramters
params["serotoninLevelA"] = 10
params["serotoninLevelB"] = 10
params["Somatic5HT2AWeight"] = 20
params["Somatic5HT2AWeightLTS"] = 10
params["Somatic5HT1AWeight"] = -5
params["Axonal5HT2AWeight"] = 0.2
params["Axonal5HT1AWeight"] = -0.2

sim = TwoColumnSimulation(params)
sim.run()
sim.plotColumns()
print("FINISHED!")

# winsound.Beep(440, 666)

