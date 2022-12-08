from subprocess import run

from src.rocket.Rocket import Rocket
from src.launch.launch import runSim

BATCH_LENGTH = 48 #Defined in Constants.h
BATCH_SIZE = 66 #Defined in Constants.h

def writeBatch(rockets: list):
    file = open("./src/sim/Batch.txt", "w")
    file.write('{}\n'.format(len(rockets)))
    for rocket in rockets:
        file.write(writeRocket(rocket))
    file.close()

def runBatch(rockets: list=None):
    if not rockets == None:
        writeBatch(rockets)
    runSim()

def writeRocket(r: Rocket) -> str:
    out =  '{}\n'.format(r.num_stages)
    out += '{}\n'.format(r.num_boosters)
    out += '{}\n'.format(r.booster_type)
    out += '{}\n'.format(r.hasS1)
    out += '{}\n'.format(r.enginetype_S1)
    out += '{}\n'.format(r.num_engines_S1)
    out += '{}\n'.format(r.hasS2)
    out += '{}\n'.format(r.enginetype_S2)
    out += '{}\n'.format(r.num_engines_S2)
    out += '{}\n'.format(r.hasS3)
    out += '{}\n'.format(r.enginetype_S3)
    out += '{}\n'.format(r.num_engines_S3)
    out += '{}\n'.format(r.hasS4)
    out += '{}\n'.format(r.enginetype_S4)
    out += '{}\n'.format(r.num_engines_S4)
    out += '{}\n'.format(r.hasS5)
    out += '{}\n'.format(r.enginetype_S5)
    out += '{}\n'.format(r.num_engines_S5)
    #Stage 1
    out += '{}\n'.format(0.0)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tD_S1)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tDC_S1)
    out += '{}\n'.format(r.lDC_S1)
    out += '{}\n'.format(r.tU_S1)
    out += '{}\n'.format(r.lDC_S1)
    out += '{}\n'.format(r.tUC_S1)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tECO_S1)
    out += '{}\n'.format(0.0)
    #Stage 2
    out += '{}\n'.format(r.tSI_S2)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tECO_S2)
    out += '{}\n'.format(0.0)
    #Stage 3
    out += '{}\n'.format(r.tSI_S3)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tECO_S3)
    out += '{}\n'.format(0.0)
    #Stage 4
    out += '{}\n'.format(r.tSI_S4)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tECO_S4)
    out += '{}\n'.format(0.0)
    #Stage 5
    out += '{}\n'.format(r.tSI_S5)
    out += '{}\n'.format(1.0)
    out += '{}\n'.format(r.tECO_S5)
    out += '{}\n'.format(0.0)
    #Size
    out += '{}\n'.format(r.dia_S1)
    out += '{}\n'.format(r.payload)
    for i in range(BATCH_SIZE - BATCH_LENGTH):
        out += '{}\n'.format('00')

    return out



