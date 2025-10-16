import numpy as np
import scipy.optimize as opt


# exponential extrapolation
def extrapolate_exp(x_list: np.array, y_list: np.array, num_test: int = 100, x_test_list: np.array = None):
    if x_test_list is None:
        x_test_list = np.linspace(0.8 * np.min(x_list), 1.2 * np.max(x_list), num_test)
    x_scaled = (x_list - np.min(x_list)) / (np.max(x_list) - np.min(x_list))
    y_scaled = (y_list - np.min(y_list)) / (np.max(y_list) - np.min(y_list))

    def func(x, a, b, c):
        return a + b * np.exp(-c * x)

    def func_test(x, a, b, c, x_list, y_list):
        xmin = np.min(x_list)
        xmax = np.max(x_list)
        ymin = np.min(y_list)
        ymax = np.max(y_list)
        return ymin + (ymax - ymin) * (a + b * np.exp(-c * (x - xmin) / (xmax - xmin)))

    try:
        a, b, c = opt.curve_fit(func, x_scaled, y_scaled)[0]
    except RuntimeError:
        a, b, c = None, None, None
    if a is None or b is None or c is None:
        return None, x_test_list, None
    y_test_list = func_test(x_test_list, a, b, c, x_list, y_list)
    y_extrap = np.min(y_list) + (np.max(y_list) - np.min(y_list)) * a
    return y_extrap, x_test_list, y_test_list


# exponential extrapolation with statistical errors
def extrapolate_exp_stat(x_list: np.array, y_list: np.array, y_err_list: np.array, num_stat: int = 1000, threshold: float = None):
    if threshold is None:
        threshold = abs(y_err_list[-1] / y_list[-1])
    y_extrap_list = []
    for _ in range(num_stat):
        y_sample = np.random.normal(y_list, y_err_list)
        y_extrap, _, _ = extrapolate_exp(x_list, y_sample)
        if y_extrap is not None and abs((y_extrap - y_list[-1]) / y_list[-1]) < threshold:
            y_extrap_list.append(y_extrap)
    y_extrap_list = np.array(y_extrap_list)
    y_extrap_mean = np.mean(y_extrap_list)
    y_extrap_std = np.std(y_extrap_list, ddof=1)
    return y_extrap_list, y_extrap_mean, y_extrap_std
