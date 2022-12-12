from src.rocket.Bounds import Bounds
from src.rocket.Engines import Engines
from src.rocket.diameter import getRocketDiameter

class Rocket:
    def __init__(self, l: list=None, score: float=None, status_mesg: str=None, num_stages=2, num_boosters=0, booster_type=0, 
                 enginetype_S1=0, num_engines_S1=0, enginetype_S2=0, num_engines_S2=0,
                 enginetype_S3=0, num_engines_S3=0, enginetype_S4=0, num_engines_S4=0, enginetype_S5=0, num_engines_S5=0, 
                 tD_S1=60, tDC_S1=70, lDC_S1=0.8, tU_S1=90, tUC_S1=100, tECO_S1=240, 
                 tSI_S2=245, tECO_S2=485, tSI_S3=486, tECO_S3=487, tSI_S4=488, tECO_S4=489, 
                 tSI_S5=490, tECO_S5=491, dia_S1=5, payload=1000):
        self.e = Engines()
        self.score = score
        self.status_mesg = status_mesg
        if not l is None:
            self.defineFromList(l)
        else:
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
            self.hasS5 = 1 if num_stages >= 5 else 0
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
            self.dia_S1 = self.calcDiameter()    #Diameter for main stage
            self.payload = payload

        # self.bounds = None
        self.bounds = Bounds()
        self.defineTimeBounds()
        self.setSuccessRate()

    def defineFromList(self, l: list):
        # Mandatory Configuration Param
        self.num_stages = 1
        self.num_boosters = int(l[0])
        self.booster_type = int(l[1])
        self.enginetype_S1 = int(l[2])
        self.num_engines_S1 = int(l[3])
        self.lDC_S1 = l[4]
        self.payload = l[5]
        self.dia_S1 = self.calcDiameter()

        # Mandatory Time Param
        self.tD_S1 = l[6]                 #Time to start throttle down
        self.tDC_S1 = self.tD_S1 + l[7]        #Time to complete throttle down
        self.tU_S1 = self.tDC_S1 + l[8]        # Time to start throttle Up
        self.tUC_S1 = self.tU_S1 + l[9]        #Time to complete throttle up
        self.tECO_S1 = self.tUC_S1 + l[10]     #Time for main engine cut off

        # Stage 2
        if len(l) > 11:
            self.num_stages = 2
            self.enginetype_S2 = int(l[11])
            self.num_engines_S2 = int(l[12])
            self.tSI_S2 = self.tECO_S1 + l[13]    #Time for 2nd stage ignition
            self.tECO_S2 = self.tSI_S2 + l[14]  #Time for 2nd stage engine cut off
        else:
            self.enginetype_S2 = 0
            self.num_engines_S2 = 0
            self.tSI_S2 = self.tECO_S1 + 1
            self.tECO_S2 = self.tSI_S2 + 1

        # Stage 3
        if len(l) > 15:
            self.num_stages = 3
            self.enginetype_S3 = int(l[15])
            self.num_engines_S3 = int(l[16])
            self.tSI_S3 = self.tECO_S2 + l[17]    #Time for 2nd stage ignition
            self.tECO_S3 = self.tSI_S3 + l[18]  #Time for 2nd stage engine cut off
        else:
            self.enginetype_S3 = 0
            self.num_engines_S3 = 0
            self.tSI_S3 = self.tECO_S2 + 1
            self.tECO_S3 = self.tSI_S3 + 1

        #Stage 4
        if len(l) > 19:
            self.num_stages = 4
            self.enginetype_S4 = int(l[19])
            self.num_engines_S4 = int(l[20])
            self.tSI_S4 = self.tECO_S3 + l[21]    #Time for 2nd stage ignition
            self.tECO_S4 = self.tSI_S4 + l[22]  #Time for 2nd stage engine cut off
        else:
            self.enginetype_S4 = 0
            self.num_engines_S4 = 0
            self.tSI_S4 = self.tECO_S3 + 1
            self.tECO_S4 = self.tSI_S4 + 1

        # Stage 5
        if len(l) > 23:
            self.num_stages = 5
            self.enginetype_S5 = int(l[23])
            self.num_engines_S5 = int(l[24])
            self.tSI_S5 = self.tECO_S4 + l[25]    #Time for 2nd stage ignition
            self.tECO_S5 = self.tSI_S5 + l[26]  #Time for 2nd stage engine cut off
        else:
            self.enginetype_S5 = 0
            self.num_engines_S5 = 0
            self.tSI_S5 = self.tECO_S4 + 1
            self.tECO_S5 = self.tSI_S5 + 1

        self.hasS1 = 1 if self.num_stages >= 1 else 0
        self.hasS2 = 1 if self.num_stages >= 2 else 0
        self.hasS3 = 1 if self.num_stages >= 3 else 0
        self.hasS4 = 1 if self.num_stages >= 4 else 0
        self.hasS5 = 1 if self.num_stages == 5 else 0

    def calcDiameter(self):
        N = self.num_engines_S1
        dia = self.e.get('Diameter', self.enginetype_S1)
        big_dia = getRocketDiameter(N, dia)
        return big_dia

    def setSuccessRate(self):
        P = 1.0
        #Boosters
        for i in range(self.num_boosters):
            P = P * self.e.get('Prob_Failure', self.booster_type)
        for i in range(self.num_engines_S1):
            P = P * self.e.get('Prob_Failure', self.enginetype_S1)
        for i in range(self.num_engines_S2):
            P = P * self.e.get('Prob_Failure', self.enginetype_S2)
        for i in range(self.num_engines_S3):
            P = P * self.e.get('Prob_Failure', self.enginetype_S3)
        for i in range(self.num_engines_S4):
            P = P * self.e.get('Prob_Failure', self.enginetype_S4)
        for i in range(self.num_engines_S5):
            P = P * self.e.get('Prob_Failure', self.enginetype_S5)
        self.success_rate = P

    def defineTimeBounds(self):
        ''' Defines lower (0) and upper (1) bounds for each time in Rocket'''
        self.bounds.addBounds({
            'tD_S1' : [self.tD_S1 + self.getBounds('g_until_throttle_down')[i] for i in range(2)],
            'tDC_S1' : [self.tD_S1 + self.getBounds('g_ramp_throttle_down')[i] for i in range(2)],
            'tU_S1' : [self.tDC_S1 + self.getBounds('g_until_throttle_up')[i] for i in range(2)],
            'tUC_S1' : [self.tU_S1 + self.getBounds('g_ramp_throttle_up')[i] for i in range(2)],
            'tECO_S1' : [self.tUC_S1 + self.getBounds('g_until_end_S1')[i] for i in range(2)],
            'tSI_S2' : [self.tECO_S1 + self.getBounds('g_between_S1_S2')[i] for i in range(2)],
            'tECO_S2' : [self.tSI_S2 + self.getBounds('g_until_end_S2')[i] for i in range(2)],
            'tSI_S3' : [self.tECO_S2 + self.getBounds('g_between_S2_S3')[i] for i in range(2)],
            'tECO_S3' : [self.tSI_S3 + self.getBounds('g_until_end_S3')[i] for i in range(2)],
            'tSI_S4' : [self.tECO_S3 + self.getBounds('g_between_S3_S4')[i] for i in range(2)],
            'tECO_S4' : [self.tSI_S4 + self.getBounds('g_until_end_S4')[i] for i in range(2)],
            'tSI_S5' : [self.tECO_S4 + self.getBounds('g_between_S4_S5')[i] for i in range(2)],
            'tECO_S' : [self.tSI_S5 + self.getBounds('g_until_end_S5')[i] for i in range(2)]
            })

    # Access
    def lowerBound(self, var: str):
        ''' Returns the lower bound of the variable with the name var'''
        return self.bounds.lowerBound(var)

    def upperBound(self, var: str):
        ''' Returns the upper bound of the variable with the name var'''
        return self.bounds.upperBound(var)

    def getBounds(self, var: str) -> list:
        ''' Returns a list of the bounds of the variable with the name var -> [lb, ub]'''
        return self.bounds.get(var)

    #Simulation
    def addResults(self, results_list: list=None, orbital_altitude: tuple=None,
                   orbital_velocity: tuple=None,  injection_velocity: tuple=None,
                   max_acceleration: tuple=None, max_pressure: tuple=None):
        if (not results_list is None) and (len(results_list) >= 5):
            self.orbital_altitude = results_list[0]
            self.orbital_velocity = results_list[1]
            self.injection_velocity = results_list[2]
            self.max_acceleration = results_list[3]
            self.max_pressure = results_list[4]
        else: 
            if not orbital_altitude is None:
                self.orbital_altitude = orbital_altitude
            if not orbital_velocity is None:
                self.orbital_velocity = orbital_velocity
            if not injection_velocity is None:
                self.injection_velocity = injection_velocity
            if not max_acceleration is None:
                self.max_acceleration = max_acceleration
            if not max_pressure is None:
                self.max_pressure = max_pressure
        pass

    def addScore(self, score: float):
        self.score = score

    def addMessage(self, mesg: str):
        self.status_mesg = mesg

    def refresh(self):
        self.hasS1 = 1 if self.num_stages >= 1 else 0
        self.hasS2 = 1 if self.num_stages >= 2 else 0
        self.hasS3 = 1 if self.num_stages >= 3 else 0
        self.hasS4 = 1 if self.num_stages >= 4 else 0
        self.hasS5 = 1 if self.num_stages >= 5 else 0
        self.dia_S1 = self.calcDiameter()
        self.setSuccessRate()


    #toString
    def toString(self):
        out = '\n---  Rocket  ---------\n'
        out += 'Diamter: {}m, Payload: {:3g}kg, Probability of Success: {:3.3f}\n'.format(self.dia_S1, self.payload, self.success_rate)
        if not self.score is None:
            out += '\tObjective Function Cost: {:4.3f}\n'.format(self.score)
        if not self.status_mesg is None:
            out += '\tMission Status: {}\n\n'.format(self.status_mesg)
        if hasattr(self, 'orbital_altitude') and hasattr(self, 'orbital_velocity'):
            out += '\n\t---Results---\n'
            out += '\tOrbital Altitude: {:4.1f}km, Orbital Velocity: {:4.1f}m/s\n'.format(self.orbital_altitude[0], self.orbital_velocity[0])
        if hasattr(self, 'injection_velocity'):
            out += '\tMaximum Velocity: {:4.1f}m/s\n'.format(self.injection_velocity[0])
        if hasattr(self, 'max_acceleration') and hasattr(self, 'max_pressure'):
            out += '\tMax Acceleration: {:4.1f}g, Max Pressure: {:4.1f}Pa\n'.format(self.max_acceleration[0] / 9.81, self.max_pressure[0])
        
        out += '\n\t---Power---\n'
        out += '\tBoosters: {}'.format(self.num_boosters)
        if self.num_boosters > 0:
            out += '\tBooster type: {}'.format(self.booster_type)
        out += '\n\tStage 1:\tEngines: {}, Type: {}\n'.format(self.num_engines_S1, self.enginetype_S1)
        if self.num_stages >= 2:
            out += '\tStage 2:\tEngines: {}, Type: {}\n'.format(self.num_engines_S2, self.enginetype_S2)
        if self.num_stages >= 3:
            out += '\tStage 3:\tEngines: {}, Type: {}\n'.format(self.num_engines_S3, self.enginetype_S3)
        if self.num_stages >= 4:
            out += '\tStage 4:\tEngines: {}, Type: {}\n'.format(self.num_engines_S4, self.enginetype_S4)
        if self.num_stages >= 5:
            out += '\tStage 5:\tEngines: {}, Type: {}\n'.format(self.num_engines_S5, self.enginetype_S5)
        
        out += '\n\t---Timing---\n'
        out += '\tThrottle Down:\tStart: {:4.1f}s, Ramp down: {:4.1f}s, Level: {:4.1f}\n'.format(self.tD_S1, self.tDC_S1, self.lDC_S1)
        out += '\tThrottle Up:\tDuration: {:4.1f}s, Ramp up: {:4.1f}s\n'.format(self.tU_S1, self.tUC_S1)
        out += '\tStage 1:\tEngine Cut Off: {:4.1f}s\n'.format(self.tECO_S1)
        if self.num_stages >= 2:
            out += '\tStage 2:\tIgnition Time: {:4.1f}s, ECO: {:4.1f}s\n'.format(self.tSI_S2, self.tECO_S2)
        if self.num_stages >= 3:
            out += '\tStage 3:\tIgnition Time: {:4.1f}s, ECO: {:4.1f}s\n'.format(self.tSI_S3, self.tECO_S3)
        if self.num_stages >= 4:
            out += '\tStage 4:\tIgnition Time: {:4.1f}s, ECO: {:4.1f}s\n'.format(self.tSI_S4, self.tECO_S4)
        if self.num_stages >= 5:
            out += '\tStage 5:\tIgnition Time: {:4.1f}s, ECO: {:4.1f}s\n'.format(self.tSI_S5, self.tECO_S5)
        return out




    
