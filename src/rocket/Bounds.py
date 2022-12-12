class Bounds:
    ''' Provides the hard constants for the upper and lower bounds on the Rocket'''
    def __init__(self):
        self.bounds = {
            'num_stages' : (0, 5),
            'num_boosters' : (0, 2),
            'booster_type' : (1, 32),
            'hasS1' : (0, 1),
            'enginetype_S1' : (101, 146),
            'num_engines_S1' : (2, 50),
            'enginetype_S2' : (201, 240),
            'num_engines_S2' : (1, 50),
            'enginetype_S3' : (201, 240),
            'num_engines_S3' : (1, 50),
            'enginetype_S4' : (201, 240),
            'num_engines_S4' : (1, 50),
            'enginetype_S5' : (201, 240),
            'num_engines_S5' : (1, 2),
            'dia_S1' : (1, 50),
            'payload' : (25000, 50000),
            'lDC_S1' : [0.2, 1.0],
 
            #Time Gaps
            'g_until_throttle_down' : (1, 60),
            'g_ramp_throttle_down' : (3, 3),
            'g_until_throttle_up' : (1, 20),
            'g_ramp_throttle_up' : (3, 3),
            'g_until_end_S1' : (100, 200),
            'g_between_S1_S2' : (3, 3),
            'g_until_end_S2' : (100, 200),
            'g_between_S2_S3' : (3, 3),
            'g_until_end_S3' : (60, 100),
            'g_between_S3_S4' : (3, 3),
            'g_until_end_S4' : (30, 100),
            'g_between_S4_S5' : (3, 3),
            'g_until_end_S5' : (30, 100),
        }

    def addBounds(self, more: dict):
        self.bounds.update(more)

    # Access
    def lowerBound(self, var: str):
        ''' Returns the lower bound of the variable with the name var'''
        return self.get(var)[0]

    def upperBound(self, var: str):
        ''' Returns the upper bound of the variable with the name var'''
        return self.get(var)[1]

    def get(self, var: str) -> list:
        ''' Returns a list of the bounds of the variable with the name var -> [lb, ub]'''
        return self.bounds[var]