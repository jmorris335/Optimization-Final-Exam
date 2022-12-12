from src.rocket.Rocket import Rocket
from src.rocket.Telem import Telem
from src.rocket.Engines import Engines
from src.rocket.Bounds import Bounds
from src.launch.limits import *

e = Engines()
b = Bounds()

#Initial Values
DURATION_0 = 5
RAMP_DOWN = 2
MAX_BURN_TIME = 300

def adjustPayload(r:Rocket, adjust: float):
    if r.payload + adjust >= b.get('payload')[1]: 
        r.payload = b.get('payload')[1]
        return False
    else: r.payload += adjust
    if r.payload <= MIN_PAYLOAD: 
        r.payload = MIN_PAYLOAD
        return False
    return True

def addStage(r, burn_time: int=100) -> bool:
    if r.num_stages == 5: return False
    r.num_stages += 1
    if r.num_stages == 2:
        r.hasS2 = 1
        updateS2time(r, burn_time)
    if r.num_stages == 3:
        r.hasS3 = 1 
        updateS3time(r, burn_time)
    if r.num_stages == 4:
        r.hasS4 = 1 
        updateS4time(r, burn_time)
    if r.num_stages == 5:
        r.hasS5 = 1 
        updateS5time(r, burn_time)
    return True

def getNumEngines(r: Rocket, stage: int):
    ''' Returns the number of engines at given stage'''
    match stage:
        case 0: return r.num_boosters
        case 1: return r.num_engines_S1
        case 2: return r.num_engines_S2
        case 3: return r.num_engines_S3
        case 4: return r.num_engines_S4
        case 5: return r.num_engines_S5

def getTypeEngine(r: Rocket, stage: int):
    ''' Returns type of engine used at given stage'''
    match stage:
        case 0: return r.booster_type
        case 1: return r.enginetype_S1
        case 2: return r.enginetype_S2
        case 3: return r.enginetype_S3
        case 4: return r.enginetype_S4
        case 5: return r.enginetype_S5
    
def addEngine(r: Rocket, stage: int=2, engine_id: int=None, amount: int=1):
    ''' Adds an engine to the rocket'''
    match stage:
        case 0:
            if not engine_id is None: r.booster_type = engine_id
            if r.num_boosters >= 2: return False
            else: r.num_boosters += amount
        case 1:
            if not engine_id is None: r.enginetype_S1 = engine_id
            if r.num_engines_S1 >= maxRockets(r.enginetype_S1): return False
            else: r.num_engines_S1 += amount
        case 2:
            if not engine_id is None: r.enginetype_S2 = engine_id
            if r.num_engines_S2 >= maxRockets(r.enginetype_S2): return False
            else: r.num_engines_S2 += amount
        case 3:
            if not engine_id is None: r.enginetype_S3 = engine_id
            if r.num_engines_S3 >= maxRockets(r.enginetype_S3): return False
            else: r.num_engines_S3 += amount
        case 4:
            if not engine_id is None: r.enginetype_S4 = engine_id
            if r.num_engines_S4 >= maxRockets(r.enginetype_S4): return False
            else: r.num_engines_S4 += amount
        case 5:
            if not engine_id is None: r.enginetype_S5 = engine_id
            if r.num_engines_S5 >= maxRockets(r.enginetype_S5): return False
            else: r.num_engines_S5 += amount
    return True

def removeEngine(r: Rocket, stage: int=2, engine_id: int=None, amount: int=1):
    match stage:
        case 0:
            if not engine_id is None: r.booster_type = engine_id
            if r.num_boosters < amount: 
                r.num_boosters = 0
                return False
            else: r.num_boosters -= amount
        case 1:
            if not engine_id is None: r.enginetype_S1 = engine_id
            if r.num_engines_S1 <= amount: 
                r.num_engines_S1 = 0
                return False
            else: r.num_engines_S1 -= amount
        case 2:
            if not engine_id is None: r.enginetype_S2 = engine_id
            if r.num_engines_S2 <= amount:
                r.num_engines_S2 = 0
                return False
            else: r.num_engines_S2 -= amount
        case 3:
            if not engine_id is None: r.enginetype_S3 = engine_id
            if r.num_engines_S3 <= amount:
                r.num_engines_S3 = 0
                return False            
            else: r.num_engines_S3 -= amount
        case 4:
            if not engine_id is None: r.enginetype_S4 = engine_id
            if r.num_engines_S4 <= amount:
                r.num_engines_S4 = 0
                return False
            else: r.num_engines_S4 -= amount
        case 5:
            if not engine_id is None: r.enginetype_S5 = engine_id
            if r.num_engines_S5 <= amount:
                r.num_engines_S5 = 0
                return False
            else: r.num_engines_S5 -= amount
    return True

def setThrottle(r: Rocket, centered_time: int, duration: int=10, level: float=None, ramp_down: int=2):
    ''' Sets the throttle times for to center around the inputted time for the
    given duration'''
    r.tD_S1 = centered_time - duration / 2 - ramp_down
    r.tDC_S1 = r.tD_S1 + ramp_down
    r.tU_S1 = r.tDC_S1 + duration / 2
    r.tUC_S1 = r.tUC_S1 = r.tU_S1 + ramp_down
    r.tSI_S2 = r.tECO_S1 + 1
    if not level is None:
        if not (level < 0 or level > 1):
            r.lDC_S1 = level

def adjustTime(r: Rocket, stage: int, adjustment: int):
    match stage:
        case 1: 
            burn_time = r.tECO_S1 + adjustment
            if burn_time > MAX_BURN_TIME or burn_time < 0: return False
            updateS1time(r, burn_time)
        case 2: 
            burn_time = r.tECO_S2 + adjustment - r.tSI_S2
            if burn_time > MAX_BURN_TIME or burn_time < 0: return False
            updateS2time(r, burn_time)
        case 3: 
            burn_time = r.tECO_S3 + adjustment - r.tSI_S3
            if burn_time > MAX_BURN_TIME or burn_time < 0: return False
            updateS3time(r, burn_time)
        case 4: 
            burn_time = r.tECO_S4 + adjustment - r.tSI_S4
            if burn_time > MAX_BURN_TIME or burn_time < 0: return False
            updateS4time(r, burn_time)
        case 5: 
            burn_time = r.tECO_S5 + adjustment - r.tSI_S5
            if burn_time > MAX_BURN_TIME or burn_time < 0: return False
            updateS5time(r, burn_time)
    return True

def updateS1time(r: Rocket, burn_time: int=100):
    r.tECO_S1 = burn_time
    updateS2time(r, burn_time)

def updateS2time(r: Rocket, burn_time: int=100):
    r.tSI_S2 = r.tECO_S1 + 1
    r.tECO_S2 = r.tSI_S2 + burn_time
    updateS3time(r, burn_time)

def updateS3time(r: Rocket, burn_time: int=100):
    r.tSI_S3 = r.tECO_S2 + 1
    r.tECO_S3 = r.tSI_S3 + burn_time
    updateS4time(r, burn_time)

def updateS4time(r: Rocket, burn_time: int=100):
    r.tSI_S4 = r.tECO_S3 + 1
    r.tECO_S4 = r.tSI_S4 + burn_time
    updateS5time(r, burn_time)

def updateS5time(r: Rocket, burn_time: int=100):
    r.tSI_S5 = r.tECO_S4 + 1
    r.tECO_S5 = r.tSI_S5 + burn_time

def maxRockets(engine_id: int=144, failure_threshold: float=0.95):
    ''' Returns the maximum number of engines possible before failure'''
    p_fail = e.get('Prob_Failure', engine_id)
    p_succeed = 1.0
    count = 0
    while p_succeed >= failure_threshold:
        count += 1
        p_succeed = p_succeed * (1 - p_fail)
    return min(count, 50)