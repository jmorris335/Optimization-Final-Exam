from src.rocket.test_diameter import test_diameter
from src.launch.test_launch import test_BatchLaunch
from src.response_surf.test_response_surf import test_ResponseSurface

from src.response_surf.find_rs import findResponseSurface

def main():
    findResponseSurface(2)

if __name__ == '__main__':
    main()