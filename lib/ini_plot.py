import matplotlib.pyplot as plt
from matplotlib import rcParams


def ini_plot():
    config = {
        "figure.dpi": 160,
        "mathtext.fontset": "cm",
        "font.family": "CMU Serif",
        # "mathtext.fontset": "stix",
        # "font.family": "Times New Roman",
        # "mathtext.fontset": "stixsans",
        # "font.family": "Arial",
        "legend.fancybox": True,
        "legend.handletextpad": 0.4,
        "legend.framealpha": 1.0,
        "legend.handlelength": 1.2,
        "patch.linewidth": 0.5,
        "axes.edgecolor": "k",
        "axes.labelcolor": "k",
        "xtick.color": "k",
        "ytick.color": "k",
    }
    rcParams.update(config)
