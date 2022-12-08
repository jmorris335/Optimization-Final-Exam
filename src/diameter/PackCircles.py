from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np
from math import comb


# def getSmallestDiameter(inner_dias: list, offset: float=0.) -> float:
#     N = len(inner_dias)
#     xs = np.zeros([1, N])
#     ys = np.zeros([1, N])

    
# def dist(x1: float, y1: float, x2: float=0., y2: float=0.) -> float:
#     return ( (x1 - x2)**2 + (y1 - y2)**2) ** (1/2)


# def objFun(xs: np.array, ys: np.array, Rs: np.array, offset: float=0):
#     f = np.dot(xs, xs) + np.dot(ys, ys)
#     return f


# def constraints(xs, ys, Rs, offset: float=0):
#     N = len(xs)
#     g = list()
#     n = comb(N, 2)
#     for i in range(n-1):
#         for j in range(i+1, n):
#             xd = (xs[j] - xs[i])
#             yd = (ys[j] - ys[i])
#             k = Rs[i] + Rs[j] + 2 * offset
#             g.append(k - np.sqrt(xd + yd))
#     return np.array(g)


# def interiorPenalty(r, xs, ys, Rs, offset: float=0):
#     f = objFun(xs, ys, Rs, offset)
#     gs = constraints(xs, ys, Rs, offset)
#     rgs = [np.log(r*g) for g in gs]
#     T = f - np.sum(rgs)


class PackCircles:
    def __init__(self, R: list, offset: float=0):
        self.N = len(R)
        self.R = R
        self.offset = offset
        self.r = .01
        self.root = self.solve()
        
    
    def solve(self):
        ''' Calls Scipy's fsolve function to find the roots of the equations'''
        N = len(self.R)
        chi0 = [max(self.R)*i for i in range(N)] * 2
        root = fsolve(self.gradT, chi0)
        isclose = np.isclose(self.gradT(root), [0.0] *(2*N))
        if all(isclose) or self.r > 100:
            return root
        else:
            self.r = self.r * 2
            print(self.r)
            return self.solve()
        

    def gradT(self, chi: list):
        ''' Returns the gradient of the interior penalty function (T)'''
        N = len(chi) // 2
        A = [self.A_m(m, chi) for m in range(N*2)]
        out = [2*chi[m] - self.r * A[m] for m in range(N*2)]
        return out


    def A_m(self, m: int, chi: list):
        ''' The sum of the distances divided by the corresponding B*(C-B)'''
        yoffset = 0 if m < self.N else self.N
        if not yoffset == 0: m = m - yoffset
        A_m = 0
        for p in range(self.N):
            if p == m: continue
            B = self.B_ij(m, p, chi)
            C = self.C_ij(m, p)
            denom = ( B * (C - B))
            A_m += (chi[m+yoffset] - chi[p+yoffset]) / denom
        return A_m


    def C_ij(self, i: int, j: int):
        ''' Minimum distance between circles i and j'''
        if i >= self.N: i = i - self.N
        if j >= self.N: j = j - self.N
        return self.R[i] + self.R[j] + 2 * self.offset


    def B_ij(self, i: int, j: int, chi: list):
        ''' Distance between circles i and j'''
        x, y = self.getXY(chi)
        if i >= self.N: i = i - self.N
        if j >= self.N: j = j - self.N
        x_dist = (x[j] - x[i])**2
        y_dist = (y[j] - y[i])**2
        return np.sqrt(x_dist + y_dist)


    @staticmethod
    def getXY(chi: list) -> list:
        ''' Returns the x and y coordinates in chi'''
        N = len(chi) // 2
        x = chi[0:N]
        y = chi[N:len(chi)]
        return x, y
    
    
    def findOuterCircle(self, chi: list) -> list:
        ''' Guarantees to circumscribe all circles in list (not optimally)'''
        x, y = self.getXY(chi)
        centroid = [np.mean(x), np.mean(y)]
        farthest_pt = 0
        farthest_dist = 0
        for m in range(len(x)):
            dist = np.sqrt((x[m]-centroid[0])**2 + (y[m]-centroid[1])**2)
            dist += self.R[m]
            if dist > farthest_dist:
                farthest_pt = m
                farthest_dist = dist
        return [centroid[0], centroid[1], farthest_dist]


    def plotCircles(self, chi: list):
        ''' Plots all the circles'''
        x, y = self.getXY(chi)

        fig, axs = plt.subplots()
        axs.set_aspect('equal')

        circles = list()
        for m in range(len(x)):
            circle = plt.Circle((x[m], y[m]), self.R[m], fill=False)
            axs.add_artist(circle)

        bc = self.findOuterCircle(chi)
        big_circle = plt.Circle((bc[0], bc[1]), bc[2], fill=False)
        axs.add_artist(big_circle)

        axs.set_ylim(ymin=bc[1]-bc[2], ymax=bc[1]+bc[2])
        axs.set_xlim(xmin=bc[0]-bc[2], xmax=bc[0]+bc[2])

        plt.title('Packing Circles')
        plt.show()
