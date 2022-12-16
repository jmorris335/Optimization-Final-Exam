import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from math import ceil

def makeDataFrame(scores: list, rockets: list) -> pd.DataFrame:
    data = {
        'scores' : scores,
        'num_stages' : [r.num_stages for r in rockets],
        'num_boosters' : [r.num_boosters for r in rockets],
        'booster_type' : [r.booster_type for r in rockets],
        'hasS1' : [(1 if r.num_stages >= 1 else 0) for r in rockets],
        'enginetype_S1' : [r.enginetype_S1 for r in rockets],
        'num_engines_S1' : [r.num_engines_S1 for r in rockets],
        'hasS2' : [(1 if r.num_stages >= 2 else 0) for r in rockets],
        'enginetype_S2' : [r.enginetype_S2 for r in rockets],
        'num_engines_S2' : [r.num_engines_S2 for r in rockets],
        'hasS3' : [(1 if r.num_stages >= 3 else 0) for r in rockets],
        'enginetype_S3' : [r.enginetype_S3 for r in rockets],
        'num_engines_S3' : [r.num_engines_S3 for r in rockets],
        'hasS4' : [(1 if r.num_stages >= 4 else 0) for r in rockets],
        'enginetype_S4' : [r.enginetype_S4 for r in rockets],
        'num_engines_S4' : [r.num_engines_S4 for r in rockets],
        'hasS5' : [(1 if r.num_stages >= 5 else 0) for r in rockets],
        'enginetype_S5' : [r.enginetype_S5 for r in rockets],
        'num_engines_S5' : [r.num_engines_S5 for r in rockets],
        'tD_S1' : [r.tD_S1 for r in rockets],      #Time to start throttle down
        'tDC_S1' : [r.tDC_S1 for r in rockets],    #Time to complete throttle down
        'lDC_S1' : [r.lDC_S1 for r in rockets],    #Level to throttle down to
        'tU_S1' : [r.tU_S1 for r in rockets],      # Time to start throttle Up
        'tUC_S1' : [r.tUC_S1 for r in rockets],     #Time to complete throttle up
        'tECO_S1' : [r.tECO_S1 for r in rockets],  #Time for main engine cut off
        'tSI_S2' : [r.tSI_S2 for r in rockets],   #Time for 2nd stage ignition
        'tECO_S2' : [r.tECO_S2 for r in rockets],  #Time for 2nd stage engine cut off
        'tSI_S3' : [r.tSI_S3 for r in rockets],    #Time for 3nd stage ignition
        'tECO_S3' : [r.tECO_S3 for r in rockets],  #Time for 3nd stage engine cut off
        'tSI_S4' : [r.tSI_S4 for r in rockets],    #Time for 4nd stage ignition
        'tECO_S4' : [r.tECO_S4 for r in rockets],  #Time for 4nd stage engine cut off
        'tSI_S5' : [r.tSI_S5 for r in rockets],    #Time for 5nd stage ignition
        'tECO_S5' : [r.tECO_S5 for r in rockets],  #Time for 5nd stage engine cut off
        'dia_S1' : [r.dia_S1 for r in rockets],    #Diameter for main stage
        'payload' : [r.payload for r in rockets]
    }
    df = pd.DataFrame(data)
    # df.to_excel('Batch_Run_Results.xlsx')
    return df
    
def scatterPlot(df: pd.DataFrame, ind_var: str, dep_var: str='scores', show_plot: bool=True):
    plt.scatter(df[ind_var], df[dep_var], color='red')
    plt.title('{} vs {})'.format(ind_var, dep_var))
    plt.xlabel(ind_var)
    plt.ylabel(dep_var)
    plt.grid(True)
    if show_plot: plt.show()

def scatterPlots(df: pd.DataFrame, dep_var: str='scores'):
    df = df[df['scores'] < 5]
    cols = list(df.columns)
    # Find desired columns
    try:
        cols.remove('scores')
        cols.remove('num_stages')
        cols.remove('booster_type')
        cols.remove('hasS1')
        cols.remove('hasS2')
        cols.remove('hasS3')
        cols.remove('hasS4')
        cols.remove('hasS5')
        cols.remove('enginetype_S1')
        cols.remove('enginetype_S2')
        cols.remove('enginetype_S3')
        cols.remove('enginetype_S4')
        cols.remove('enginetype_S5')
        cols.remove('dia_S1')
        cols.remove('payload')
        cols.remove('tSI_S3')
        cols.remove('tECO_S3')
        cols.remove('tSI_S4')
        cols.remove('tECO_S4')
        cols.remove('tSI_S5')
        cols.remove('tECO_S5')
    except:
        pass

    n = len(cols)
    num_r = ceil(n ** (1/2))
    fig, axs = plt.subplots(num_r, num_r)
    for r in range(num_r):
        for c in range(num_r):
            i = r * num_r + c
            if i >= n: break
            axs[r, c].scatter(df[cols[i]], df[dep_var], s=.5)
            axs[r, c].set_title(cols[i])
    plt.tight_layout()
    plt.show()

def lin_reg(df: pd.DataFrame, dep_var: str='scores'):
    x = df.loc[:, df.columns != dep_var]
    y = df[dep_var]

    # with statsmodels
    x = sm.add_constant(x) # adding a constant
    
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x) 
    
    print_model = model.summary()
    print(print_model)