import numpy as np
import random as rand

from src.rocket.Rocket import Rocket

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
        bin_mins = np.linspace(variables[v].min, variables[v].max, num_points+1)
        vals = np.zeros((num_points, 1))
        for i in range(len(vals)):
            vals[i] = rand.uniform(bin_mins[i], bin_mins[i+1])
        ind = [i for i in range(num_points)]
        rand.shuffle(ind)
        for i in ind:
            points[i, v] = vals[ind[i]]
    return points

def getConfigurationParameters(r: Rocket, num_divisions: int) -> list:
    ''' Returns the primary configuration parameters for the rocket'''
    #FIXME: LH needs to have some way of setting rocket types to 0 for rockets with less than
    # N stages. Right now you can have a rocket that has additional stages in the LH, even if that's 
    #not configured. You can also have a 5th stage, but not a 2nd stage...
    # Maybe we need to run this 5 times, one for each stage?
    stages = r.num_stages
    variables = list()
    variables.append(r.getBounds('num_boosters'))
    variables.append(r.getBounds('booster_type'))
    variables.append(r.getBounds('enginetype_S1'))
    variables.append(r.getBounds('num_engines_S1'))
    if r.num_stages >= 2:
        variables.append(r.getBounds('enginetype_S2'))
        variables.append(r.getBounds('num_engines_S2'))
    if r.num_stages >= 3:
        variables.append(r.getBounds('enginetype_S3'))
        variables.append(r.getBounds('num_engines_S3'))
    if r.num_stages >= 4:
        variables.append(r.getBounds('enginetype_S4'))
        variables.append(r.getBounds('num_engines_S4'))
    if r.num_stages >= 5:
        variables.append(r.getBounds('enginetype_S5'))
        variables.append(r.getBounds('num_engines_S5'))
    return variables

def getTimeParameters(r: Rocket, num_divisions: int) -> list:
    ''' Returns the time parameters for the rocket'''
    pass
