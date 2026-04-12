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


# blocking analysis with fixed block size L for ratio Z = X / Y
def blocking_fixed_ratio(data_x: np.array, data_y: np.array, L: int, pos=0):
    assert len(data_x) == len(data_y), "Input arrays must have the same length."
    start_index = int(pos * len(data_x))
    if start_index >= len(data_x) or start_index < 0:
        start_index = 0
    x_cut = data_x[start_index:]
    y_cut = data_y[start_index:]
    num_blocks = len(x_cut) // L
    if num_blocks < 2:
        raise ValueError("Block size L too large, resulting in less than 2 blocks.")

    x_trimmed = x_cut[-num_blocks * L :]
    y_trimmed = y_cut[-num_blocks * L :]

    x_blocked = x_trimmed.reshape(num_blocks, L).mean(axis=1)
    y_blocked = y_trimmed.reshape(num_blocks, L).mean(axis=1)

    mean_x = np.mean(x_blocked)
    mean_y = np.mean(y_blocked)

    cov_matrix = np.cov(x_blocked, y_blocked, ddof=1)
    var_x = cov_matrix[0, 0]
    var_y = cov_matrix[1, 1]
    cov_xy = cov_matrix[0, 1]

    mean_z = mean_x / mean_y
    rel_var_z = (var_x / (mean_x**2) + var_y / (mean_y**2) - 2.0 * cov_xy / (mean_x * mean_y)) / num_blocks
    std_err_z = np.abs(mean_z) * np.sqrt(max(0, rel_var_z))
    std_err_err_z = std_err_z / np.sqrt(2 * (num_blocks - 1))
    return mean_z, std_err_z, std_err_err_z


# blocking analysis with automatic block size selection
def blocking_auto(data: np.array, pos=0):
    if pos < 0 or pos >= 1:
        print("Warning: position pos is out of range. Using pos=0 instead.")
        pos = 0
    data_list = data[int(pos * len(data)) :]
    l_max = int(np.log2(len(data_list)))
    l_list = np.array([2**n for n in range(1, l_max)])
    mean_list = []
    std_list = []
    std_std_list = []
    for L in l_list:
        mean, std, std_std = blocking_fixed(data_list, L)
        mean_list.append(mean)
        std_list.append(std)
        std_std_list.append(std_std)
    mean_list = np.array(mean_list)
    std_list = np.array(std_list)
    std_std_list = np.array(std_std_list)
    decreasing_idx = np.where(np.diff(std_list) < 0)[0]
    if len(decreasing_idx) == 0:
        print("Warning: mean_list is monotonically increasing. Returning values at the end.")
        idx = len(l_list) - 1
    else:
        idx = decreasing_idx[0]
    return int(l_list[idx]), float(mean_list[idx]), float(std_list[idx]), float(std_std_list[idx])


# blocking analysis with automatic block size selection for ratio Z = X / Y
def blocking_auto_ratio(data_x: np.array, data_y: np.array, pos=0):
    if pos < 0 or pos >= 1:
        print("Warning: position pos is out of range. Using pos=0 instead.")
        pos = 0
    data_x_list = data_x[int(pos * len(data_x)) :]
    data_y_list = data_y[int(pos * len(data_y)) :]
    l_max = int(np.log2(len(data_x_list)))
    l_list = np.array([2**n for n in range(1, l_max)])
    mean_list = []
    std_list = []
    std_std_list = []
    for L in l_list:
        mean, std, std_std = blocking_fixed_ratio(data_x_list, data_y_list, L)
        mean_list.append(mean)
        std_list.append(std)
        std_std_list.append(std_std)
    mean_list = np.array(mean_list)
    std_list = np.array(std_list)
    std_std_list = np.array(std_std_list)
    decreasing_idx = np.where(np.diff(std_list) < 0)[0]
    if len(decreasing_idx) == 0:
        print("Warning: mean_list is monotonically increasing. Returning values at the end.")
        idx = len(l_list) - 1
    else:
        idx = decreasing_idx[0]
    return int(l_list[idx]), float(mean_list[idx]), float(std_list[idx]), float(std_std_list[idx])
