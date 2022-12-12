import pandas as pd

class Telem:
    def __init__(self):
        self.df = self.parseFile()

    def parseFile(self):
        with open('src/sim/Telemetry.txt', 'r') as f:
            f.readline()
            vals = [[float(x) for x in line.split()] for line in f]

        cols = ['Time', 'Thrust', 'Mass', 'Altitude', 'Velocity', 
                'Acceleration', 'AtmosphericDensity', 'Pressure', 
                'Temperature', 'CD', 'Fdrag', 'g', 'DynamicPressure', 
                'MachNumber', 'OrbitalAccelerationBalance', 'dMass', 'Altitude']

        df = pd.DataFrame(vals, columns=cols, index=[i for i in range(len(vals))])
        return df

    def getAt(self, key: str, time: int=0):
        try:
            out = self.df.loc[self.df['Time'] > time][key].iloc[0]
        except:
            return None
        return out

    def getTimeAt(self, key: str, val):
        try:
            out = self.df[self.df[key] >= val]['Time'].iloc[0]
        except:
            return None
        return out


            

