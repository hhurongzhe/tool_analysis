import numpy as np


def print_list(array, precision: int = 4):
    format_specifier = f".{precision}f"
    formatted = [f"{x:{format_specifier}}" for x in array]
    print("[" + ", ".join(formatted) + "]")
