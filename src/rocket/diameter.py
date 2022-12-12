from numpy import sin, pi, sqrt

''' Replaces PackCircles, which requires quite a bit more testing'''

def getRocketDiameter(N: int, dia: float) -> float:
    dia = dia * 1.1 #Adjust for offset
    radius = dia / 2
    match N:
        case 1:
            return dia
        case 2:
            return dia * 2
        case 3:
            return dia * (1 + 2 / sqrt(3))
        case 4:
            return dia * (1 + sqrt(2))
        case 5:
            return dia * (1 + sqrt( 2 * (1 + 1/sqrt(5))))
        case 6:
            return dia * 3
        case 7:
            return dia * 3
        case 8:
            return dia * (1 + (1 / sin(pi/7)))
        case 9:
            return dia * (1 + sqrt( 2*(2 + sqrt(2)) ))
        case 10:
            return dia * 3.813
        case 11:
            return dia * (1 + ( 1 / sin(pi/9)))
        case 12:
            return dia * 4.029
        case 13:
            return dia * (2 + sqrt(5))
        case 14:
            return dia * 4.328
        case 15:
            return dia * 4.521
        case 16:
            return dia * 4.615
        case 17:
            return dia * 4.729
        case 18:
            return dia * (1 + sqrt(2) + sqrt(6))
        case 19:
            return dia * (1 + sqrt(2) + sqrt(6))
        case 20:
            return dia * 5.122
        case _:
            return dia * 7

