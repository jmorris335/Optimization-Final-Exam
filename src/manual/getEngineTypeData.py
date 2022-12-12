from src.launch.run_batch import runBatch
from src.rocket.Rocket import Rocket
from src.rocket.Engines import Engines
from src.rocket.Telem import Telem
from src.launch.get_results import readSimSummData
from launch.parse_results import parseFlownRockets

def getMasses(type: str=144, stage: int=1):
    f = open('src/manual/{} Results.txt'.format(type), 'w')

    for i in range(1, 51):
        if stage == 1:
            type_S1 = type
            num_S1 = i
        else:
            type_S1 = 144
            num_S1 = 1
        
        if stage >= 2:
            type_S2 = type
            num_S2 = i
        else:
            type_S2 = 0
            num_S1 = 0

        if stage >= 3:
            type_S3 = type
            num_S3 = i
        else:
            type_S3 = 0
            num_S3 = 0

        if stage >= 4:
            type_S4 = type
            num_S4 = i
        else:
            type_S4 = 0
            num_S4 = 0

        if stage >= 5:
            type_S5 = type
            num_S5 = i
        else:
            type_S5 = 0
            num_S5 = 0
            
        r = Rocket(num_stages=stage, num_boosters=1, booster_type=13, dia_S1=3, payload=10000,
            enginetype_S1=type_S1, num_engines_S1=num_S1,
            enginetype_S2=type_S2, num_engines_S2=num_S2,
            enginetype_S3=type_S3, num_engines_S3=num_S3,
            enginetype_S4=type_S4, num_engines_S4=num_S4,
            enginetype_S5=type_S5, num_engines_S5=num_S5,
            tD_S1 = 40, tDC_S1=50, lDC_S1=0.5, tU_S1=90, tUC_S1=100,
            tECO_S1=311, tSI_S2=312, tECO_S2=600, tSI_S3=601, tECO_S3=700)
        runBatch([r])
        readSimSummData([r])
        parseFlownRockets([r])
        print(r.toString())
        tel = Telem()
        mass = tel.df['Mass'][0]
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(i, mass, r.orbital_velocity[0],
                r.orbital_altitude[0], r.injection_velocity[0], r.max_acceleration[0], 
                r.max_pressure[0]))

    f.close()


    
