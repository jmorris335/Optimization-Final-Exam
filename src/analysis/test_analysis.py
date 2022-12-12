from src.analysis.analysis import *
from src.response_surf.get_rs import *
from src.launch.parse_results import *

def test_analysis():
    rockets = findResponseSurface(10, 5)
    scores = parseFlownRockets(rockets)
    df = makeDataFrame(scores, rockets)
    scatterPlots(df)