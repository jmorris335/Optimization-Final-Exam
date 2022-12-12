from subprocess import run

def compile():
    run('g++ *.cpp -std=c++14 -o sim.exe', cwd='./src/sim/SourceCode', shell=True)
    run('rm sim.exe', cwd='./src/sim', shell=True)
    run('mv ./SourceCode/sim.exe .', cwd='./src/sim', shell=True)

if __name__ == '__main__':
    compile()