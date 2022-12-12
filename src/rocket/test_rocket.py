from src.rocket.PackCircles import PackCircles
from src.rocket.Engines import Engines

def test_Engines():
    Es = Engines()
    print(Es.df.tail(5))


def test_diameter():
    N = 2
    Radius = 0.5
    offset = 0

    Radii = [Radius] * N
    obj = PackCircles(Radii, offset)
    print(obj.root)
    obj.plotCircles(obj.root)


if __name__ == '__main__':
    test_diameter()