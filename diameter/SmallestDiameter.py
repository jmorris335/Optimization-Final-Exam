from scipy.optimize import linprog
import numpy as np
from math import comb


def getSmallestDiameter(inner_dias: list, offset: float=0.) -> float:
    N = len(inner_dias)
    xs = np.zeros([1, N])
    ys = np.zeros([1, N])

    
def dist(x1: float, y1: float, x2: float=0., y2: float=0.) -> float:
    return ( (x1 - x2)**2 + (y1 - y2)**2) ** (1/2)


def objFun(xs: np.array, ys: np.array, Rs: np.array, offset: float=0):
    f = np.dot(xs, xs) + np.dot(ys, ys)
    return f


def constraints(xs, ys, Rs, offset: float=0):
    N = len(xs)
    g = list()
    n = comb(N, 2)
    for i in range(n):
        for j in range(i, n):
            xd = (xs[j] - xs[i])
            yd = (ys[j] - ys[i])
            k = Rs[i] + Rs[j] + 2 * offset
            g.append(k - np.sqrt(xd + yd))
    return np.array(g)


def interiorPenalty(r, xs, ys, Rs, offset: float=0):
    f = objFun(xs, ys, Rs, offset)
    gs = constraints(xs, ys, Rs, offset)
    rgs = [np.log(r*g) for g in gs]
    T = f - np.sum(rgs)

