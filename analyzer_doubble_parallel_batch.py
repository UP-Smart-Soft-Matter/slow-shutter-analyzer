import matplotlib.pyplot as plt
import csv
import numpy as np
from natsort import natsorted
from pygwy_txt_analysis import get_folder_path
from astropy import units as u
import glob
import os


def get_data(filepath):
    peak_x = []
    peak_y = []
    valley_x = []
    valley_y = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if row[0]!='' and row[1]!='' and row[2]!='' and row[3]!='':
                peak_x.append(float(row[0]))
                peak_y.append(float(row[1]))
                valley_x.append(float(row[2]))
                valley_y.append(float(row[3]))

        peak_x = np.array(peak_x) * u.m
        peak_y = (np.array(list(peak_y)) * u.m).to(u.nm)

        valley_x = np.array(valley_x) * u.m
        valley_y = (np.array(list(valley_y)) * u.m).to(u.nm)

        height = peak_y - valley_y

    return peak_x, peak_y, valley_x, valley_y, height

folder_path = get_folder_path()
file_list = natsorted(glob.glob(os.path.join(folder_path, "*.txt")))
periods = [0.8, 1.7, 2.5, 3.4, 4.2, 5]

for i, file in enumerate(file_list):
    p_x, p_y, v_x, v_y, height = get_data(file)

    dist_to_time_factor = 3.3
    x_time = ((p_x.to(u.um).value * dist_to_time_factor) * u.s).to(u.min)

    fig, ax = plt.subplots(2)
    fig.suptitle(f"Polymer: RS93, Periode: {periods[i]} µm, laser power: 200 mW, objective: 40x")
    ax[0].plot(x_time, height, label="srg height", c="r")
    ax[0].set_ylabel(f'height ({p_y.unit})')
    ax[0].legend(loc="lower right")

    ax[1].plot(x_time, p_y, label="peak height")
    ax[1].plot(x_time, v_y, label="valley height")
    ax[1].set_ylabel(f'height ({p_y.unit})')
    ax[1].legend()

    plt.xlabel(f'Δ illumination time ({x_time.unit})')
    fig.tight_layout()
    plt.show()