class Rocket:
    def __init__(self, num_stages=2, num_boosters=0, booster_type=0, 
                 enginetype_S1=0, num_engines_S1=0, enginetype_S2=0, num_engines_S2=0,
                 enginetype_S3=0, num_engines_S3=0, enginetype_S4=0, num_engines_S4=0, enginetype_S5=0, num_engines_S5=0, 
                 tD_S1=60, tDC_S1=70, lDC_S1=0.8, tU_S1=90, tUC_S1=100, tECO_S1=240, 
                 tSI_S2=245, tECO_S2=485, tSI_S3=0, tECO_S3=0, tSI_S4=0, tECO_S4=0, 
                 tSI_S5=0, tECO_S5=0, dia_S1=5, payload=1000):
        self.num_stages = num_stages
        self.num_boosters = num_boosters
        self.booster_type = booster_type
        self.hasS1 = 1 if num_stages >= 1 else 0
        self.enginetype_S1 = enginetype_S1
        self.num_engines_S1 = num_engines_S1
        self.hasS2 = 1 if num_stages >= 2 else 0
        self.enginetype_S2 = enginetype_S2
        self.num_engines_S2 = num_engines_S2
        self.hasS3 = 1 if num_stages >= 3 else 0
        self.enginetype_S3 = enginetype_S3
        self.num_engines_S3 = num_engines_S3
        self.hasS4 = 1 if num_stages >= 4 else 0
        self.enginetype_S4 = enginetype_S4
        self.num_engines_S4 = num_engines_S4
        self.hasS5 = 5 if num_stages >= 5 else 0
        self.enginetype_S5 = enginetype_S5
        self.num_engines_S5 = num_engines_S5
        self.tD_S1 = tD_S1      #Time to start throttle down
        self.tDC_S1 = tDC_S1    #Time to complete throttle down
        self.lDC_S1 = lDC_S1    #Level to throttle down to
        self.tU_S1 = tU_S1      # Time to start throttle Up
        self.tUC_S1 =tUC_S1     #Time to complete throttle up
        self.tECO_S1 =tECO_S1   #Time for main engine cut off
        self.tSI_S2 = tSI_S2    #Time for 2nd stage ignition
        self.tECO_S2 = tECO_S2  #Time for 2nd stage engine cut off
        self.tSI_S3 = tSI_S3    #Time for 3nd stage ignition
        self.tECO_S3 = tECO_S3  #Time for 3nd stage engine cut off
        self.tSI_S4 = tSI_S4    #Time for 4nd stage ignition
        self.tECO_S4 = tECO_S4  #Time for 4nd stage engine cut off
        self.tSI_S5 = tSI_S5    #Time for 5nd stage ignition
        self.tECO_S5 = tECO_S5  #Time for 5nd stage engine cut off
        self.dia_S1 = dia_S1    #Diameter for main stage
        self.payload = payload

        self.bounds = None

    def defineBounds(self):
        ''' Defines lower (0) and upper (1) bounds for each variable in Rocket'''
        if not self.bounds is None:
            return

        self.bounds = {
            'num_stages' : [0, 5],
            'num_boosters' : [0, 2],
            'booster_type' : [1, 32],
            'hasS1' : [0, 1],
            'enginetype_S1' : [101, 146],
            'num_engines_S1' : [0, 50],
            'enginetype_S2' : [201, 240],
            'num_engines_S2' : [0, 50],
            'enginetype_S3' : [201, 240],
            'num_engines_S3' : [0, 50],
            'enginetype_S4' : [201, 240],
            'num_engines_S4' : [0, 50],
            'enginetype_S5' : [201, 240],
            'num_engines_S5' : [0, 50],
            'tD_S1' : [0, 100],
            'tDC_S1' : [self.tD_S1 + 1, self.tD_S1 + 50],
            'lDC_S1' : [0.2, 1.0],
            'tU_S1' : [self.tDC_S1 + 1, self.tDC_S1 + 50],
            'tUC_S1' : [self.tU_S1 + 1, self.tU_S1 + 50],
            'tECO_S1' : [self.tUC_S1 + 1, self.tUC_S1 + 200],
            'tSI_S2' : [self.tECO_S1 + 1, self.tECO_S1 + 50],
            'tECO_S2' : [self.tSI_S2 + 1, self.tSI_S2 + 300],
            'tSI_S3' : [self.tECO_S2 + 1, self.tECO_S2 + 50],
            'tECO_S3' : [self.tSI_S3 + 1, self.tSI_S3 + 300],
            'tSI_S4' : [self.tECO_S3 + 1, self.tECO_S3 + 50],
            'tECO_S4' : [self.tSI_S4 + 1, self.tSI_S4 + 300],
            'tSI_S5' : [self.tECO_S4 + 1, self.tECO_S4 + 50],
            'tECO_S' : [self.tSI_S5 + 1, self.tSI_S5 + 300],
            'dia_S1' : [1, 50],
            'payload' : [1000, 50000]
        }

    # Access
    def lowerBound(self, var: str):
        ''' Returns the lower bound of the variable with the name var'''
        self.defineBounds()
        return self.getBounds(var)[0]

    def upperBound(self, var: str):
        ''' Returns the upper bound of the variable with the name var'''
        self.defineBounds()
        return self.getBounds(var)[1]

    def getBounds(self, var: str) -> list:
        ''' Returns a list of the bounds of the variable with the name var -> [lb, ub]'''
        self.defineBounds()
        return self.bounds[var]



    
