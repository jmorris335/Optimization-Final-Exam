from src.rocket.Rocket import Rocket
from src.launch.run_batch import runBatch
from src.launch.get_results import readSimSummData

def test_BatchLaunch():
    rockets = [Rocket(), Rocket(), Rocket()]
    runBatch(rockets)
    print(readSimSummData())
