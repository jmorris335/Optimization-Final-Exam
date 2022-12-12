from src.rocket.Rocket import Rocket
from src.launch.run_batch import runBatch
from src.launch.get_results import readSimSummData
from src.launch.launch import runSim

def test_BatchLaunch():
    rockets = [Rocket(),Rocket(),Rocket(),Rocket(),Rocket()]
    runBatch(rockets)
    print(readSimSummData())

def test_SingleLaunch():
    r = Rocket(num_stages=2, num_boosters=0, booster_type=0, dia_S1=3, payload=1700,
    enginetype_S1=145, num_engines_S1=9, enginetype_S2=238, num_engines_S2=1,
    tD_S1 = 60, tDC_S1=70, lDC_S1=0.8, tU_S1=90, tUC_S1=100,
    tECO_S1=240, tSI_S2=245)
    runBatch([r])
    print(r.toString())
