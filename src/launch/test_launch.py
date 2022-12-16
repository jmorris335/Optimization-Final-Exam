from src.rocket.Rocket import Rocket
from src.launch.run_batch import runBatch
from src.launch.get_results import readSimSummData
from src.launch.launch import runSim
from src.launch.parse_results import parseFlownRockets

def test_BatchLaunch():
    rockets = [Rocket(),Rocket(),Rocket(),Rocket(),Rocket()]
    runBatch(rockets)
    print(readSimSummData())

def test_SingleLaunch():
    S1_burntime = 150
    S2_burntime = 397 + S1_burntime
    S3_burntime = 200 + S2_burntime
    S4_burntime = 200 + S3_burntime
    S5_burntime = 200 + S4_burntime

    gap12 = 1
    gap23 = 1 + gap12
    gap34 = 1 + gap23
    gap45 = 1 + gap34

    r = Rocket(num_stages=2, 
    payload=25000,
    num_boosters=0, booster_type=11, 
    enginetype_S1=144, num_engines_S1=9, 
    enginetype_S2=238, num_engines_S2=1,
    enginetype_S3=213, num_engines_S3=0,
    enginetype_S4=213, num_engines_S4=0,
    enginetype_S5=238, num_engines_S5=0,
    tD_S1 = 60, tDC_S1=63.7, lDC_S1=1.0, 
    tU_S1=63.7, tUC_S1=65.7,
    tECO_S1=S1_burntime, 
    tSI_S2=S1_burntime+gap12, tECO_S2=S2_burntime+1,
    tSI_S3=S2_burntime+gap23, tECO_S3=S3_burntime+2,
    tSI_S4=S3_burntime+gap34, tECO_S4=S4_burntime+3,
    tSI_S5=S4_burntime+gap45, tECO_S5=S5_burntime+4)
    runBatch([r])
    parseFlownRockets([r])
    readSimSummData([r])
    print(r.toString())
