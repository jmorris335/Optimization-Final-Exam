import ctypes
from subprocess import run

def import_lib():
    cSim = ctypes.cdll.LoadLibrary('./src/predict/libsim.so')
    cSim.cGravity.restype = ctypes.c_double

    g = cSim.cGravity(ctypes.c_double(0.0))
    print(g)

def compileClib():
    run('g++ -g -o libsim.so -shared -fPIC -std=c++14 Cdeclaration.cpp',
            cwd='./src/sim/SourceCode', shell=True)
    run('mv ./sim/SourceCode/libsim.so ./predict/', cwd='./src', shell=True)

if __name__ == '__main__':
    # compileClib()
    import_lib()
