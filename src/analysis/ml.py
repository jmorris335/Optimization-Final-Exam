import pandas as pd
import statsmodels.api as sm

from src.response_surf.get_rs import findResponseSurface
from src.launch.parse_results import parseFlownRockets
from src.rocket.Rocket import Rocket
from src.rocket.Engines import Engines

'''
Factors:
 - Thrust per stage
 - ISP per stage
 - Dry mass per stage
 - Diameter
 - Fuel consumption per stage
 - Burn time per stage
 - Payload

 Out:
 - Acceleration
 - Orb Vel
 - Altitude
 - Inj Vel
 - Pressure
 - Probability of Failure
 - Score
'''

def ml_caller():
    df = getLinRegData(50000)
    df = df[df['altitude'] > 50.0]
    acc_model = lin_reg(df, dep_var='acceleration')
    orb_model = lin_reg(df, dep_var='orbital_velocity')
    alt_model = lin_reg(df, dep_var='altitude')
    inj_model = lin_reg(df, dep_var='injection_velocity')
    pre_model = lin_reg(df, dep_var='pressure')
    fail_model = lin_reg(df, dep_var='success_rate')
    scor_model = lin_reg(df, dep_var='scores')

def lin_reg(df: pd.DataFrame, dep_var: str='scores'):
    x = df.loc[:, df.columns != 'acceleration']
    x = x.loc[:, x.columns != 'orbital_velocity']
    x = x.loc[:, x.columns != 'altitude']
    x = x.loc[:, x.columns != 'injection_velocity']
    x = x.loc[:, x.columns != 'pressure']
    x = x.loc[:, x.columns != 'success_rate']
    x = x.loc[:, x.columns != 'scores']
    y = df[dep_var]

    # with statsmodels
    x = sm.add_constant(x) # adding a constant
    
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x) 
    
    print_model = model.summary()
    print(print_model)
    return model

def getLinRegData(N: int=10000):
    e = Engines()
    divisions = (N // 26) // 5
    rockets = findResponseSurface(divisions, 5)
    parseFlownRockets(rockets)

    orb_vel = list()
    altitude = list()
    inj_vel = list()
    acceleration = list()
    pressure = list()
    scores = list()
    success_rate = list()
    diameter = list()
    payload = list()
    thrust0 = list()
    thrust1 = list()
    thrust2 = list()
    thrust3 = list()
    thrust4 = list()
    thrust5 = list()
    isp0 = list()
    isp1 = list()
    isp2 = list()
    isp3 = list()
    isp4 = list()
    isp5 = list()
    dry_mass0 = list()
    dry_mass1 = list()
    dry_mass2 = list()
    dry_mass3 = list()
    dry_mass4 = list()
    dry_mass5 = list()
    fuelpers0 = list()
    fuelpers1 = list()
    fuelpers2 = list()
    fuelpers3 = list()
    fuelpers4 = list()
    fuelpers5 = list()
    burn_time1 = list()
    burn_time2 = list()
    burn_time3 = list()
    burn_time4 = list()
    burn_time5 = list()

    for r in rockets:
        orb_vel.append(r.orbital_velocity[0])
        altitude.append(r.orbital_altitude[0])
        inj_vel.append(r.injection_velocity[0])
        acceleration.append(r.max_acceleration[0])
        pressure.append(r.max_pressure[0])
        scores.append(r.score)
        success_rate.append(r.success_rate)
        diameter.append(r.dia_S1)
        payload.append(r.payload)
        thrust0.append(e.get('Thrust', r.booster_type) * r.num_boosters)
        thrust1.append(e.get('Thrust', r.enginetype_S1) * r.num_engines_S1)
        thrust2.append(e.get('Thrust', r.enginetype_S2) * r.num_engines_S2)
        thrust3.append(e.get('Thrust', r.enginetype_S3) * r.num_engines_S3)
        thrust4.append(e.get('Thrust', r.enginetype_S4) * r.num_engines_S4)
        thrust5.append(e.get('Thrust', r.enginetype_S5) * r.num_engines_S5)
        isp0.append(e.get('ISP', r.booster_type))
        isp1.append(e.get('ISP', r.enginetype_S1))
        isp2.append(e.get('ISP', r.enginetype_S2))
        isp3.append(e.get('ISP', r.enginetype_S3))
        isp4.append(e.get('ISP', r.enginetype_S4))
        isp5.append(e.get('ISP', r.enginetype_S5))
        dry_mass0.append(e.get('Dry_Mass', r.booster_type))
        dry_mass1.append(e.get('Dry_Mass', r.enginetype_S1))
        dry_mass2.append(e.get('Dry_Mass', r.enginetype_S2))
        dry_mass3.append(e.get('Dry_Mass', r.enginetype_S3))
        dry_mass4.append(e.get('Dry_Mass', r.enginetype_S4))
        dry_mass5.append(e.get('Dry_Mass', r.enginetype_S5))
        fuelpers0.append(e.get('Fuel_Consumption', r.booster_type))
        fuelpers1.append(e.get('Fuel_Consumption', r.enginetype_S1))
        fuelpers2.append(e.get('Fuel_Consumption', r.enginetype_S1))
        fuelpers3.append(e.get('Fuel_Consumption', r.enginetype_S1))
        fuelpers4.append(e.get('Fuel_Consumption', r.enginetype_S1))
        fuelpers5.append(e.get('Fuel_Consumption', r.enginetype_S1))
        burn_time1.append(r.tECO_S1)
        burn_time2.append(r.tECO_S2 - r.tSI_S2)
        burn_time3.append(r.tECO_S3 - r.tSI_S3)
        burn_time4.append(r.tECO_S4 - r.tSI_S4)
        burn_time5.append(r.tECO_S5 - r.tSI_S5)

    data = {
        'scores' : scores,
        'success_rate' : success_rate,
        'orbital_velocity' : orb_vel,
        'altitude' : altitude,
        'injection_velocity' : inj_vel,
        'acceleration' : acceleration,
        'pressure' : pressure,
        'diameter' : diameter,
        'payload' : payload,
        'thrust0' : thrust0,
        'thrust1' : thrust1,
        'thrust2' : thrust2,
        'thrust3' : thrust3,
        'thrust4' : thrust4,
        'thrust5' : thrust5,
        'isp0' : isp0,
        'isp1' : isp1,
        'isp2' : isp2,
        'isp3' : isp3,
        'isp4' : isp4,
        'isp5' : isp5,
        'dry_mass0' : dry_mass0,
        'dry_mass1' : dry_mass1,
        'dry_mass2' : dry_mass2,
        'dry_mass3' : dry_mass3,
        'dry_mass4' : dry_mass4,
        'dry_mass5' : dry_mass5,
        'fuelpers0' : fuelpers0,
        'fuelpers1' : fuelpers1,
        'fuelpers2' : fuelpers2,
        'fuelpers3' : fuelpers3,
        'fuelpers4' : fuelpers4,
        'fuelpers5' : fuelpers5,
        'burn_time1' : burn_time1,
        'burn_time2' : burn_time2,
        'burn_time3' : burn_time3,
        'burn_time4' : burn_time4,
        'burn_time5' : burn_time5,
    }

    return pd.DataFrame(data)


    