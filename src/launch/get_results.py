from src.rocket.Rocket import Rocket

LENGTH_ROCKET_SUM = 5 #Number of lines per rocket in file
OFFSET = 1 #Space between rockets in file

def readSimSummData(rockets: list=None):
    ''' Reads the rocket sim data from the file and either writes to the rockets list 
    or returns a list with all the results
    '''

    with open("src/sim/SimulationSummaryData.txt") as f:
        lines = [line.strip() for line in f]
    
    out = list()
    for i in range(len(lines) // (LENGTH_ROCKET_SUM + OFFSET)):
        results = list()
        for j in range(LENGTH_ROCKET_SUM):
            vals = lines[i*LENGTH_ROCKET_SUM + j + i*OFFSET]
            tup = tuple([float(k) for k in vals.split()])
            results.append(tup)
        if (not rockets is None) and (len(rockets) >= i):
            rockets[i].addResults(results)
        else: out.append(results)
    
    f.close()
    if (rockets is None):
        return out