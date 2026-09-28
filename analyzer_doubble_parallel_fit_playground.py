import os

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.optimize import curve_fit
from astropy import units as u
from matplotlib.offsetbox import AnchoredText
import glob
from natsort import natsorted
from pygwy_txt_analysis import get_folder_path


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

    return peak_x, peak_y, valley_x, valley_y

def linear(x, a, b):
    return a * x + b



folder_path_list = glob.glob(os.path.join(get_folder_path(), '*'))

for folder in folder_path_list:
    for file in natsorted(glob.glob(f"{folder}/*.txt")):
        p_x, p_y, v_x, v_y = get_data(file)

        p_x = np.array(p_x) * u.m
        p_y = (np.array(list(p_y)) * u.m).to(u.nm)

        v_x = np.array(v_x) * u.m
        v_y = (np.array(list(v_y)) * u.m).to(u.nm)

        height = p_y - v_y

        dist_to_time_factor = 40
        x_time = ((p_x.to(u.um).value * dist_to_time_factor) * u.s).to(u.min)

        # fit, _ = curve_fit(linear, x_time.value, p_y.value)
        # fit2, _ = curve_fit(linear, x_time.to(u.s).value, p_y.value)
        # print(f"steigung: {fit2[0]:.3f} nm/s")
        fig, ax = plt.subplots(2,2, figsize=(10,10), dpi=200)
        fig.suptitle(f"{os.path.basename(file)[:-4]}")
        ax[0,0].plot(x_time, height, label="srg height", c="r")
        ax[0,0].set_title("original")
        ax[0,1].loglog(x_time, height, label="srg height", c="r")
        ax[0,1].set_title("log log")
        ax[1,0].semilogx(x_time, height, label="srg height", c="r")
        ax[1,0].set_title("semi  log x")
        ax[1,1].semilogy(x_time, height, label="srg height", c="r")
        ax[1,1].set_title("semi  log y")
        plt.ylabel(f'height ({p_y.unit})')
        # ax.plot(x_time, linear(x_time.value, fit[0], fit[1]), label="linear fit: a={:.3f}, b={:.3f}".format(fit[0], fit[1]))
        plt.xlabel(f'Δ illumination time ({x_time.unit})')

        fig.tight_layout()
        # ax.add_artist(text_box)
        plt.show()