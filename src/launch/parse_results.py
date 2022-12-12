from src.rocket import Rocket
from src.launch.limits import *

def parseFlownRockets(rockets: list):
    scores = [obj_func(r) for r in rockets]
    mean = sum(scores) / len(scores)
    
    return scores

def obj_func(r: Rocket):
    ''' Lower scores are better. Normalized so that 0 is best, 1 is worst.
    Scores higher than 1 indicate failure.
    '''
    score = 0
    num_factors = 7
    
    [didFail, mesg] = rocketFailed(r, True)
    r.addMessage(mesg)
    if didFail: score += num_factors

    # Obtained minimum orbital velocity (0 to 1)
    factor = max((0, (MIN_ORBITAL_VEL - r.orbital_velocity[0]) / MIN_ORBITAL_VEL))
    score += factor * WEIGHT_ORBITAL_VEL

    # Obtained minimum orbital altitude (0 to 1)
    factor = max((0, (MIN_ALTITUDE - r.orbital_altitude[0]) / MIN_ALTITUDE))
    score += factor * WEIGHT_ALTITUDE

    # Obtained target injection velocity (0 to 1)
    tol = abs(r.injection_velocity[0] - GOAL_INJECTION_VEL)
    if tol > MAX_TOLERANCE_INJ_VEL: factor = 1
    else: factor = tol / MAX_TOLERANCE_INJ_VEL
    score += factor * WEIGHT_INJECTION_VEL
    
    # Under maximum acceleration (0 to 1)
    acc_limit = MAX_ACCEL - ACCEL_SAFTEY_GAP
    factor = max(0, min(1, (r.max_acceleration[0] - acc_limit) / acc_limit))
    score += factor * WEIGHT_ACCEL

    # Under max pressure (0 to 1)
    p_limit = MAX_PRESSURE - PRESSURE_SAFETY_GAP
    factor = max(0, min(1, (r.max_pressure[0] - p_limit) / p_limit))
    score += factor * WEIGHT_PRESSURE

    # Carried large enough payload (0 to 1)
    factor = max(0, (MIN_PAYLOAD - r.payload) / MIN_PAYLOAD)
    score += factor * WEIGHT_PAYLOAD

    # Liklihood of success (0 to 1)
    factor = 1 - r.success_rate
    score += factor * WEIGHT_FAILURE

    # Normalize and return
    score = score / num_factors
    r.addScore(score)
    return score

def rocketFailed(r: Rocket, getMesg: bool=False):
    mesg = None
    if r.orbital_velocity[0] < MIN_ORBITAL_VEL: 
        mesg = 'Orbital velocity is too slow ({:.2f} vs. {:.2f})'.format(r.orbital_velocity[0], MIN_ORBITAL_VEL)
    elif r.orbital_altitude[0] < MIN_ALTITUDE:
        mesg = 'Orbital altitude is too low ({:.2f} vs. {:.2f})'.format(r.orbital_altitude[0], MIN_ALTITUDE)
    elif r.payload < MIN_PAYLOAD:
        mesg = 'Payload is too light ({:.2f} vs. {:.2f})'.format(r.payload, MIN_PAYLOAD)
    elif r.injection_velocity[0] < GOAL_INJECTION_VEL - TOLERANCE_INJECTION_VEL:
        mesg = 'Injection velocity was too slow ({:.2f} vs. {:.2f})'.format(r.injection_velocity[0], GOAL_INJECTION_VEL)
    elif r.injection_velocity[0] > GOAL_INJECTION_VEL + TOLERANCE_INJECTION_VEL:
        mesg = 'Injection velocity was too fast ({:.2f} vs. {:.2f})'.format(r.injection_velocity[0], GOAL_INJECTION_VEL)
    elif r.max_pressure[0] > MAX_PRESSURE:
        mesg = 'Dynamic pressure was too great ({:.2f} vs. {:.2f})'.format(r.max_pressure[0], MAX_PRESSURE)
    elif r.max_acceleration[0] > MAX_ACCEL:
        mesg = 'Max acceleration was too great ({:.2f} vs. {:.2f})'.format(r.max_accleration[0] / 9.81, MAX_ACCEL / 9.81)
    
    if mesg is None:
        if getMesg:
            return False, 'Successfully completed mission'
        else: return False
    else:
        if getMesg: 
            return True, mesg
        else: return True

