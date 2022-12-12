from subprocess import run

from src.rocket.Rocket import Rocket

def runSim():
    run('./sim.exe', cwd='./src/sim')

if __name__ == '__main__':
    runSim()

