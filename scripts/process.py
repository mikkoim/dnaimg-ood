import pandas as pd
from pathlib import Path
import numpy as np

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str)

    args = parser.parse_args()