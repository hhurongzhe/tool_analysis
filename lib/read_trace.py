import numpy as np


# read trace data from FCIQMC;
# matter mode: E_real, E_imag, norm_real, norm_imag, E_real, E_imag, S, Nw;
# nuclei mode: i, sidx, Nw, S, E, J2, norm.
def read_trace(mode: str, filename: str):
    data = np.loadtxt(filename, comments="#", delimiter=",", unpack=True)
    if mode == "matter":
        E_real, E_imag, norm_real, norm_imag, E_real, E_imag, S, Nw = data
        return E_real, E_imag, norm_real, norm_imag, E_real, E_imag, S, Nw
    elif mode == "nuclei":
        i, sidx, Nw, S, E, J2, norm = data
        return i, sidx, Nw, S, E, J2, norm
    else:
        raise ValueError(f"unknown mode: {mode}")
