from src.diameter.PackCircles import PackCircles

def t_diameter():
    N = 2
    Radius = 0.5
    offset = 0

    Radii = [Radius] * N
    obj = PackCircles(Radii, offset)
    print(obj.root)
    obj.plotCircles(obj.root)

if __name__ == '__main__':
    t_diameter()