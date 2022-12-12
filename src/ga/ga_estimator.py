from random import randint, sample
from copy import deepcopy
from datetime import datetime

from src.predict.estimate import *
from src.rocket.Rocket import Rocket
from src.response_surf.get_rs import findResponseSurface
from src.launch.parse_results import parseFlownRockets
from src.launch.run_batch import runBatch

logfile = 'results/ga_results.txt'

def callerGA():
    writeTime()
    best_r = runGA(N=400, max_gen=1000, stall_gen=10, max_size=440, breeding_size=64,
                   death_age=8)
    print(best_r.toString())

def runGA(N: int=200, max_gen: int=1000, stall_gen: int=50,
          death_age: int=100, breeding_size: int=10, max_size: int=220) -> Rocket:
    rockets = seed(N)
    parseFlownRockets(rockets)
    
    # Set Initial Conditions
    scores = [r.score for r in rockets]
    ages = [0] * len(rockets)
    best_r = deepcopy(rockets[scores.index(min(scores))])
    gen = 1
    stalled_gen = 0

    # Begin Loop
    while gen < max_gen:
        # Take intelligent step
        for r in rockets: adjust(r)
        fly(rockets)

        # Make children
        makeChildren(rockets, scores, ages, breeding_size)

        # Mutate
        for r in rockets: mutate(r, .10)
        
        # Check convergence
        scores = [r.score for r in rockets]
        if min(scores) < best_r.score:
            stalled_gen = 0
            best_r = deepcopy(rockets[scores.index(min(scores))])
            log(best_r.toString())
            print(best_r.toString())

        output = getOutput(gen, scores, best_r)
        print(output)
        log(output)

        # Age and kill
        ages = [i + 1 for i in ages]
        for i in range(len(ages)):
            if ages[-i] > 100: 
                del rockets[-i]
                del ages[-i]
        rockets, ages = trim(rockets, scores, ages, max_size)

        # Check stopping criteria
        if gen >= max_gen:
            print(best_r.toString())
            print('NUMBER OF GENERATIONS EXCEEDED THRESHOLD: {}'.format(max_gen))
            return best_r
        else: gen += 1

        if stalled_gen > stall_gen:
            print(best_r.toString())
            print('POPULATION EXCEEDED STALL THRESHOLD: {}'.format(stall_gen))
            return best_r
        else:
            stalled_gen += 1
    
    return best_r

def seed(N: int=200):
    rs = findResponseSurface(10, 5)
    return sample(rs, N)

def mutate(r: Rocket, chance_of_mutation: float=0.04):
    if random() < chance_of_mutation:
        mutation = randint(0, 9)
        match mutation:
            case 0: r.booster_type = randint(b.get('booster_type')[0], b.get('booster_type')[1])
            case 1: r.enginetype_S1 = randint(b.get('enginetype_S1')[0], b.get('enginetype_S1')[1])
            case 2: r.enginetype_S2 = randint(b.get('enginetype_S2')[0], b.get('enginetype_S2')[1])
            case 3: r.enginetype_S3 = randint(b.get('enginetype_S3')[0], b.get('enginetype_S3')[1])
            case 4: r.enginetype_S4 = randint(b.get('enginetype_S4')[0], b.get('enginetype_S4')[1])
            case 5: r.enginetype_S5 = randint(b.get('enginetype_S5')[0], b.get('enginetype_S5')[1])
            case 6: addEngine(r, stage=randint(0, r.num_stages+1))
            case 7: removeEngine(r, stage=randint(0, r.num_stages))
            case 8: adjustPayload(r, float(randint(-10000, 10000)))
            case 9: adjustTime(r, randint(0, r.num_stages+1), randint(-60, 60))
        fly([r])

def makeChildren(rockets: list, scores: list, ages: list, breeders_size: int=10):
    if not breeders_size % 2 == 0: breeders_size -= 1
    # Get top rockets to breed
    breeders = getNbest(rockets, scores, breeders_size)
    left = sample(breeders, len(breeders) // 2)
    right = [i for i in breeders if i not in left]
    for i in range(len(left)):
        child = crossover(left[i], right[i])
        rockets.append(child)
        fly([child])
        scores.append(child.score)
        ages.append(0)

def crossover(left: Rocket, right: Rocket, degree: int=None):
    num_genes = 18
    if degree is None: degree = randint(1, num_genes)
    genes = sample(range(num_genes), degree)
    child = deepcopy(left)
    for gene in genes:
        match gene:
            case 0: child.booster_type = right.booster_type
            case 1: child.enginetype_S1 = right.enginetype_S1
            case 2: child.enginetype_S2 = right.enginetype_S2
            case 3: child.enginetype_S3 = right.enginetype_S3
            case 4: child.enginetype_S4 = right.enginetype_S4
            case 5: child.enginetype_S5 = right.enginetype_S5
            case 6: child.num_boosters = right.num_boosters
            case 7: child.num_engines_S1 = right.num_engines_S1
            case 8: child.num_engines_S2 = right.num_engines_S2
            case 9: child.num_engines_S3 = right.num_engines_S3
            case 10: child.num_engines_S4 = right.num_engines_S4
            case 11: child.num_engines_S5 = right.num_engines_S5
            case 12: child.payload = right.payload
            case 13: adjustTime(child, 1, right.tECO_S1)
            case 14: adjustTime(child, 2, right.tECO_S2 - right.tECO_S1)
            case 15: adjustTime(child, 3, right.tECO_S3 - right.tECO_S2)
            case 16: adjustTime(child, 4, right.tECO_S4 - right.tECO_S3)
            case 17: adjustTime(child, 5, right.tECO_S5 - right.tECO_S4)
            case 18: child.num_stages = right.num_stages
    child.refresh()
    return child

def getNbest(rockets: list, scores: list, N: int):
    ''' Returns the top N rockets based on scores. Use -N for worst'''
    if N < 0:
        N = max(-len(rockets)+1, N)
        return [rockets[i] for i in sorted(range(len(rockets)), key=lambda i: scores[i])][N:]
    N = min(len(rockets), N)
    return [rockets[i] for i in sorted(range(len(rockets)), key=lambda i: scores[i])][:N]

def trim(rockets: list, scores: list, ages: list, max_size: int=220) -> list:
    ''' Removes the worst rockets so that the size is below max_size'''
    keep = getNbest(rockets, scores, max_size)
    ages = [ages[i] for i in range(len(rockets)) if rockets[i] in keep]
    return keep, ages

def fly(rockets: list):
    runBatch(rockets)
    parseFlownRockets(rockets)

def writeTime():
    f = open(logfile, 'w')
    now = datetime.now()
    f.write('***Genetic Algorithm Results\t')
    f.write(now.strftime("%d/%m/%Y %H:%M:%S"))
    f.write('\n')

def log(out: str):
    f = open(logfile, 'a')
    f.write(out)
    f.write('\n')
    f.close()

def getOutput(gen: int, scores: list, best_r: Rocket):
    mean = sum(scores) / len(scores)
    return 'Generation: {}\tMean value: {:4.3f}\tBest value: {:4.3f}'.format(gen, mean, best_r.score)

if __name__ == '__main__':
    callerGA()
