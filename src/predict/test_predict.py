from src.predict.estimate import adjust

def test_estimate():
    adjust(engine_id_S1=144, engine_id_S2plus=211, num_stages=1)