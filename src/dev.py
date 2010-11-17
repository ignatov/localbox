""" Script for developer. """

import sys

sys.path.append("./lib")
sys.path.append("./src")

from localbox.synchronizer import Synchronizer

def main():
    """ Main script. """
    Synchronizer("testing.ini").sync()

if __name__ == "__main__":
    sys.exit(main())
