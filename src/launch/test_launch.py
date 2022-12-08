from src.rocket.Rocket import Rocket
from src.launch.run_batch import writeBatch
from src.launch.launch import *

def test_BatchLaunch():
    rockets = [Rocket(), Rocket(), Rocket(), Rocket()]
    writeBatch(rockets)
    runSim()