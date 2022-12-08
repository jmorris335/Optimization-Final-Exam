from subprocess import run

def runSim():
    run('./sim.exe', cwd='./src/sim')

if __name__ == '__main__':
    runSim()

