from src.response_surf.LatinHypercube import *
from src.response_surf.get_rs import *
from src.launch.parse_results import parseFlownRockets
from src.analysis.analysis import *

def test_ResponseSurface():
    divisions = 2
    num_stages = 1
    vars = getParameters(num_stages)
    configs = generateLH(vars, divisions)
    rockets = makeRocketsFromVars(configs)
    for r in rockets:
        print(r.toString())

def test_getRS():
    rockets = findResponseSurface(100, 2)
    scores = parseFlownRockets(rockets)
    br = rockets[scores.index(min(scores))]
    print(br.toString())

if __name__ == '__main__':
    test_ResponseSurface()