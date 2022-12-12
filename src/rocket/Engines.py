import pandas as pd

class Engines:
    def __init__(self):
        self.df = self.parseFile()

    def parseFile(self) -> pd.DataFrame:
        #Get probability of failure
        with open('src/sim/EngineFailureProb.txt', 'r') as f2:
            failures = [float(x) for x in f2]

        # Get rest of data
        with open('src/sim/RocketData.txt', 'r') as f:
            lines = [[x for x in line.split()] for line in f]
        
        engines = list()
        int_i = [0, 1, 2, 5, 10]
        float_i = [3, 4, 6, 7, 8, 9]
        for l in range(len(lines)):
            e = list()
            for i in range(len(lines[l])):
                if i in int_i: e.append(int(lines[l][i]))
                else: e.append(float(lines[l][i]))
            e.append(failures[l])
            engines.append(e)

        ids =  [int(l[0]) for l in lines]       
        cols = ['ID', 'Stage', 'Unknown', 'Ox/Fuel', 'ISP', 'Thrust', 'Dry_Mass', 'Diameter', 
                'Fuel_Consumption', 'Burn_Time', 'Gross_Mass', 'Type', 'Prob_Failure']
        return pd.DataFrame(engines, index=ids, columns=cols)

    def get(self, key: str, engine_id: int=144):
        return self.df[key].loc[engine_id]