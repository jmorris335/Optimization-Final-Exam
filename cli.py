from src.rocket.test_rocket import *
from src.launch.test_launch import *
from src.response_surf.test_response_surf import *
from src.analysis.test_analysis import *
from src.ga.ga_estimator import callerGA
from src.analysis.ml import ml_caller

from src.response_surf.get_rs import findResponseSurface

def main():
    # test_getRS()
    # test_SingleLaunch()
    # test_analysis()
    # getMasses(213, 3)
    # test_estimate()
    # callerGA()
    ml_caller()

if __name__ == '__main__':
    main()