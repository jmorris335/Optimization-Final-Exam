from src.rocket.test_rocket import *
from src.launch.test_launch import *
from src.response_surf.test_response_surf import *
from src.analysis.test_analysis import *
from src.predict.test_predict import *
from src.ga.ga_estimator import callerGA

from src.response_surf.get_rs import findResponseSurface

def main():
    # test_getRS()
    # test_SingleLaunch()
    # test_analysis()
    # getMasses(213, 3)
    # test_estimate()
    callerGA()

if __name__ == '__main__':
    main()