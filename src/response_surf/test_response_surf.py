from src.response_surf.LatinHypercube import *
from src.rocket.Bounds import Bounds

def test_ResponseSurface():
    divisions = 2
    num_stages = 1
    vars = getParameters(num_stages)
    configs = generateLH(vars, divisions)
    rockets = makeRocketsFromVars(configs)
    for r in rockets:
        print(r.toString())

    
if __name__ == '__main__':
    test_ResponseSurface()