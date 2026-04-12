import numpy as np


# read trace data from FCIQMC;
# matter mode: E_real_unnorm, E_imag_unnorm, norm_real, norm_imag, E_real, E_imag, S, Nw;
# nuclei mode: i, Nw, S, E, J2, norm;
# fermi mode: i, NwA1, NwB1, NwA2, NwB2, Num_A1_B2, Num_A2_B1, Ov_A1_A2, Ov_B1_B2, Den, MF1, MF2, MF.
def read_trace(mode: str, filename: str, pos: float = 0.0):
    if not 0 <= pos <= 1:
        raise ValueError(f"pos must be between 0 and 1, got {pos}")
    with open(filename, "r") as f:
        lines = f.readlines()
    data_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            data_lines.append(line)
    if len(data_lines) > 1:
        data_lines = data_lines[:-1]
    start_index = int(len(data_lines) * pos)
    data_lines = data_lines[start_index:]

    if mode == "matter":
        ncol = 7
    elif mode == "nuclei":
        ncol = 6
    elif mode == "fermi":
        ncol = 13
    else:
        raise ValueError(f"unknown mode: {mode}")

    parsed = []
    for line in data_lines:
        parts = line.split(",")
        if len(parts) != ncol:
            print(f"Skipped line (column mismatch): {line}")
            continue
        try:
            row = [float(x) for x in parts]
            parsed.append(row)
        except ValueError:
            print(f"Skipped line (non-numeric): {line}")
            continue

    if len(parsed) == 0:
        raise ValueError("No valid data after filtering.")

    data = np.array(parsed).T

    if mode == "matter":
        i, Nw, S, E_real, E_imag, norm_real, norm_imag = data
        return i, Nw, S, E_real, E_imag, norm_real, norm_imag
    elif mode == "nuclei":
        i, Nw, S, E, J2, norm = data
        return i, Nw, S, E, J2, norm
    elif mode == "fermi":
        i, NwA1, NwB1, NwA2, NwB2, Num_A1_B2, Num_A2_B1, Ov_A1_A2, Ov_B1_B2, Den, MF1, MF2, MF = data
        return i, Den, MF
