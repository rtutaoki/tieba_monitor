import json
import re

import os


def test():
    print(os.getcwd())


if __name__ == '__main__':
    print(os.getcwd().split('/')[-1])
    print(os.path.dirname(os.getcwd()))

