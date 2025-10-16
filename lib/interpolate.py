import numpy as np


# interpolation using polynomial fitting and prediction
def poly_fit_predict(x: np.array, y: np.array, degree: int, x_target: np.array) -> np.array:
    coeffs = np.polyfit(x, y, degree)
    y_predict = np.polyval(coeffs, x_target)
    return y_predict
