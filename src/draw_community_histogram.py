import pandas as pd
import numpy as np
import math
import sys
from matplotlib import pyplot as plt
from collections import Counter
from pprint import pprint

DATA_DIR = '..\data'
METRICS_DIR = f'{DATA_DIR}\metrics'


def histogram():
    df = pd.read_csv(f'{DATA_DIR}\{sys.argv[1]}.csv')
    classes = df['Modularity Class']
    counter = Counter(classes)
    data = np.array(list(counter.values()))
    NO_OF_RANGES = 100

    plt.figure(figsize=(20, 10))
    plt.ylabel('Count')
    plt.title(f'Community sizes for {sys.argv[1]}')

    bin_width = math.ceil(data.max() / NO_OF_RANGES)
    plt.xlabel(f'Size of community (bin width = {bin_width})')
    plt.hist(data, bins=range(data.min(), data.max() + 1, bin_width), log=True)
    plt.savefig(f'{METRICS_DIR}\histogram_{sys.argv[1]}.png')

    data = np.array(list(filter(lambda x: x < bin_width, list(counter.values()))))
    plt.figure(figsize=(20, 10))
    plt.ylabel('Count')
    plt.title(f'Community sizes for {sys.argv[1]} (x < {bin_width})')

    bin_width = math.ceil(data.max() / NO_OF_RANGES)
    plt.xlabel(f'Size of community (bin width = {bin_width})')
    plt.hist(data, bins=range(data.min(), data.max() + 1, bin_width), log=True)
    plt.savefig(f'{METRICS_DIR}\histogram_small_{sys.argv[1]}.png')


if __name__ == '__main__':
    histogram()
