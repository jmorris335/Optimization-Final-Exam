from random import random, randint

from src.rocket.Telem import Telem
from src.rocket.Rocket import Rocket
from src.rocket.access_rocket import *
from src.launch.limits import *
from src.launch.run_batch import runBatch
from src.launch.parse_results import parseFlownRockets

def adjust(r: Rocket):
    runRocket(r)
    checkAltitude(r)
    checkAcceleration(r)
    checkPressure(r)
    checkOrbitalVelocity(r)
    checkInjectionVelocity(r)
    checkFailureRatio(r)

def checkAltitude(r: Rocket) -> bool:
    if r.orbital_altitude[0] < MIN_ALTITUDE:
        adjustPayload(r, -1500)
        addEngine(r, 0)
        for i in range(2, r.num_stages+1):
            removeEngine(r, i, amount=2)

def checkAcceleration(r: Rocket):
    if r.max_acceleration[0] < MAX_ACCEL * 0.5:
        adjustTime(r, 1, -20)
    if r.max_acceleration[0] > MAX_ACCEL:
        adjustPayload(r, r.payload * .1) 
        removeEngine(r, findMaxAccelerationStage(r))

def findMaxAccelerationStage(r: Rocket):
    ''' Returns stage where max acceleration occured'''
    tel = Telem()
    t_max_a = tel.getTimeAt('Acceleration', r.max_acceleration[0])
    if t_max_a <= r.tECO_S1: return 1
    if t_max_a <= r.tECO_S2: return 2
    if t_max_a <= r.tECO_S3: return 3
    if t_max_a <= r.tECO_S4: return 4
    else: return 5

def checkPressure(r: Rocket):
    duration = r.tU_S1 - r.tDC_S1
    level = r.lDC_S1
    ramp_down = 2
    if r.max_pressure[0] > MAX_PRESSURE:
        duration += 2
        level = level - 0.1
    tel = Telem()
    t_p_max = tel.df['Time'].iloc[tel.df['DynamicPressure'].idxmax()]
    setThrottle(r, t_p_max, duration, level, ramp_down)

def checkOrbitalVelocity(r: Rocket):
    if r.orbital_velocity[0] < MIN_ORBITAL_VEL:
        adjustTime(r, 1, 20)
        adjustTime(r, max(r.num_stages-1, 1), 20)
        addEngine(r, max(r.num_stages-1,1))
        if r.num_engines_S2 >= 10: r.num_boosters += 1 if r.num_boosters < 2 else 0
        if getNumEngines(r, max(r.num_stages-1,1)) >= maxRockets(getTypeEngine(r, max(r.num_stages-1,1))):
            addStage(r)

def checkInjectionVelocity(r: Rocket):
    if (r.injection_velocity[0] - GOAL_INJECTION_VEL) < -MAX_TOLERANCE_INJ_VEL:
        # Too slow
        if not  addEngine(r, stage=r.num_stages):
            if not addStage(r):
                r.tECO_S5 += r.tECO_S5 * 0.1
    elif (r.injection_velocity[0] - GOAL_INJECTION_VEL) > MAX_TOLERANCE_INJ_VEL:
        # Too fast
        if not removeEngine(r, r.num_stages):
            adjustTime(r, r.num_stages, -20)

def checkFailureRatio(r: Rocket):
    if (r.success_rate < MIN_SUCCESS_RATE):
        worst_stage = [1., 0]
        for stage in range(r.num_stages + 1):
            if getStageSuccessRate(r, stage) < worst_stage[0]:
                worst_stage[1] = stage
        removeEngine(r, worst_stage[1])
        adjustPayload(r, -5000)

def getInitalRocket(engine_id_S1: int=144, engine_id_S2plus: int=213, booster_type: int=22, 
                    num_stages: int=3) -> Rocket:
    r = Rocket(num_stages=num_stages, payload=25000,
               num_boosters=0, booster_type=booster_type,
               enginetype_S1=engine_id_S1, num_engines_S1=maxRockets(engine_id_S1, 0.98),
               enginetype_S2=engine_id_S2plus, num_engines_S2=maxRockets(engine_id_S2plus, 0.98),
               enginetype_S3=engine_id_S2plus, num_engines_S3=maxRockets(engine_id_S2plus, 0.98),
               enginetype_S4=engine_id_S2plus, num_engines_S4=maxRockets(engine_id_S2plus, 0.98),
               enginetype_S5=engine_id_S2plus, num_engines_S5=maxRockets(engine_id_S2plus, 0.98), 
               )
    updateS1time(r, MAX_BURN_TIME)
    setThrottle(r, 40, DURATION_0, 1.0)
    return r

def runRocket(r: Rocket):
    runBatch([r])
    parseFlownRockets([r])
