import numpy as np


# read trace data from FCIQMC;
# matter mode: E_real_unnorm, E_imag_unnorm, norm_real, norm_imag, E_real, E_imag, S, Nw;
# nuclei mode: i, Nw, S, E, J2, norm.
def read_trace(mode: str, filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()
    data_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            data_lines.append(line)
    if len(data_lines) > 1:
        data_lines = data_lines[:-1]
    data = np.genfromtxt(data_lines, delimiter=",", unpack=True)
    if mode == "matter":
        E_real_unnorm, E_imag_unnorm, norm_real, norm_imag, E_real, E_imag, S, Nw = data
        return E_real_unnorm, E_imag_unnorm, norm_real, norm_imag, E_real, E_imag, S, Nw
    elif mode == "nuclei":
        i, Nw, S, E, J2, norm = data
        return i, Nw, S, E, J2, norm
    else:
        raise ValueError(f"unknown mode: {mode}")
