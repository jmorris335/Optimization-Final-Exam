import numpy as np
import random as rand

from src.rocket.Rocket import Rocket
from src.rocket.Bounds import Bounds

def generateLH(variables: list, divisions: int) -> np.array:
    ''' Returns a Latin Hypercube sampling across the variables. For N variables, the 
    functions returns divisions*(N-1) points. The output is a divisions*(N-1) x N array 
    where each row represents a coordinate point, and each column is the coordinate of 
    each variable corresponding to the point. 
    
    See https://en.wikipedia.org/wiki/Latin_hypercube_sampling for more information on
    Latin Hypercube sampling.
    '''
    N = len(variables)
    num_points = divisions * (N-1)
    if N == 1: num_points = 1
    points = np.zeros((num_points, N))
    
    for v in range(len(variables)):
        bin_mins = np.linspace(min(variables[v]), max(variables[v]), num_points+1)
        vals = np.zeros((num_points, 1))
        for i in range(len(vals)):
            vals[i] = rand.uniform(bin_mins[i], bin_mins[i+1])
        ind = [i for i in range(num_points)]
        rand.shuffle(ind)
        for i in ind:
            points[i, v] = vals[ind[i]]
    return points

def getParameters(num_stages: int=2) -> list:
    ''' Returns all the contant variables defining a rocket'''
    b = Bounds()
    variables = list()
    # Mandatory configuration variables
    variables.append(b.get('num_boosters'))
    variables.append(b.get('booster_type'))
    variables.append(b.get('enginetype_S1'))
    variables.append(b.get('num_engines_S1'))
    variables.append(b.get('lDC_S1'))
    variables.append(b.get('payload'))

    # Mandatory Timing variables
    variables.append(b.get('g_until_throttle_down'))
    variables.append(b.get('g_ramp_throttle_down'))
    variables.append(b.get('g_until_throttle_up'))
    variables.append(b.get('g_ramp_throttle_up'))
    variables.append(b.get('g_until_end_S1'))

    # Stage 2
    if num_stages >= 2:
        variables.append(b.get('enginetype_S2'))
        variables.append(b.get('num_engines_S2'))
        variables.append(b.get('g_between_S1_S2'))
        variables.append(b.get('g_until_end_S2'))

    # Stage 3
    if num_stages >= 3:
        variables.append(b.get('enginetype_S3'))
        variables.append(b.get('num_engines_S3'))
        variables.append(b.get('g_between_S2_S3'))
        variables.append(b.get('g_until_end_S3'))

    # Stage 4
    if num_stages >= 4:
        variables.append(b.get('enginetype_S4'))
        variables.append(b.get('num_engines_S4'))
        variables.append(b.get('g_between_S3_S4'))
        variables.append(b.get('g_until_end_S4'))

    # Stage 5
    if num_stages >= 5:
        variables.append(b.get('enginetype_S5'))
        variables.append(b.get('num_engines_S5'))
        variables.append(b.get('enginetype_S5'))
        variables.append(b.get('num_engines_S5'))
    
    return variables

def getConfigurationParameters(b: Bounds, num_stages: int=2) -> list:
    ''' Returns the primary configuration parameters for the rocket'''
    #FIXME: LH needs to have some way of setting rocket types to 0 for rockets with less than
    # N stages. Right now you can have a rocket that has additional stages in the LH, even if that's 
    #not configured. You can also have a 5th stage, but not a 2nd stage...
    # Maybe we need to run this 5 times, one for each stage?
    variables = list()
    variables.append(b.get('num_boosters'))
    variables.append(b.get('booster_type'))
    variables.append(b.get('enginetype_S1'))
    variables.append(b.get('num_engines_S1'))
    variables.append(b.get('lDC_S1'))
    variables.append(b.get('payload'))
    if num_stages >= 2:
        variables.append(b.get('enginetype_S2'))
        variables.append(b.get('num_engines_S2'))
    if num_stages >= 3:
        variables.append(b.get('enginetype_S3'))
        variables.append(b.get('num_engines_S3'))
    if num_stages >= 4:
        variables.append(b.get('enginetype_S4'))
        variables.append(b.get('num_engines_S4'))
    if num_stages >= 5:
        variables.append(b.get('enginetype_S5'))
        variables.append(b.get('num_engines_S5'))
    return variables

def getTimeGaps(b: Bounds, num_stages: int=2) -> list:
    ''' Returns the lower and upper bounds permissible for each gap between times'''
    variables = list()
    variables.append(b.get('g_until_throttle_down'))
    variables.append(b.get('g_ramp_throttle_down'))
    variables.append(b.get('g_until_throttle_up'))
    variables.append(b.get('g_ramp_throttle_up'))
    variables.append(b.get('g_until_end_S1'))
    if num_stages >= 2:
        variables.append(b.get('g_between_S1_S2'))
        variables.append(b.get('g_until_end_S2'))
    if num_stages >= 3:
        variables.append(b.get('g_between_S2_S3'))
        variables.append(b.get('g_until_end_S3'))
    if num_stages >= 4:
        variables.append(b.get('g_between_S3_S4'))
        variables.append(b.get('g_until_end_S4'))
    if num_stages >= 5:
        variables.append(b.get('g_between_S4_S5'))
        variables.append(b.get('g_until_end_S5'))
    return variables

def makeRocketsFromVars(all_vars: list):
    ''' Takes the lists and returns the corresponding rockets'''
    rockets = list()
    for v in all_vars:
        rockets.append(Rocket(v))
    return rockets
