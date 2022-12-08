from src.response_surf.LatinHypercube import *
from src.rocket.Rocket import Rocket
from src.rocket.Bounds import Bounds
from src.launch.run_batch import runBatch
from src.launch.get_results import readSimSummData

def findResponseSurface(divisions: int=2):
    rockets = list()
    for stage in range(5+1):
        vars = getParameters(stage)
        configs = generateLH(vars, divisions)
        these_rockets = makeRocketsFromVars(configs)
        runBatch(these_rockets)
        readSimSummData(these_rockets)
        rockets.extend(these_rockets)
    return rockets

def parseFlownRockets(rockets: list):
    pass
