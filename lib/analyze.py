import numpy as np


# simple statistics: mean and standard deviation
def stat_simple(data: np.array, pos=0):
    start_index = int(pos * len(data))
    if start_index >= len(data) or start_index < 0:
        print("Warning: position pos is out of range. Using pos=0 instead.")
        start_index = 0
    data = data[start_index:]
    num = len(data)
    std = np.std(data, ddof=1)
    mean = np.mean(data)
    return mean, std


# blocking analysis with fixed block size L
def blocking_fixed(data: np.array, L: int, pos=0):
    start_index = int(pos * len(data))
    if start_index >= len(data) or start_index < 0:
        print("Warning: position pos is out of range. Using pos=0 instead.")
        start_index = 0
    data = data[start_index:]

    if L >= len(data):
        raise ValueError("block size L must be less than the length of data.")

    num_blocks = len(data) // L
    trimmed_data = data[-num_blocks * L :]

    if num_blocks < 2:
        raise ValueError("block size L too large, resulting in less than 2 blocks.")

    block_means = np.zeros(num_blocks)

    for i in range(num_blocks):
        block = trimmed_data[i * L : (i + 1) * L]
        if L != 1:
            mean, std = stat_simple(block)
        else:
            mean = np.mean(block)
        block_means[i] = mean

    mean, std = stat_simple(block_means)
    std_err = std / np.sqrt(num_blocks)
    std_err_err = std_err / np.sqrt(2 * (num_blocks - 1))

    return mean, std_err, std_err_err
