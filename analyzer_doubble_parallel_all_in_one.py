import os
import matplotlib.pyplot as plt
import csv
import numpy as np
from astropy import units as u
from pygwy_txt_analysis import get_folder_path
import glob
from natsort import natsorted

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

file_path = get_folder_path()
file_path_list = natsorted(glob.glob(os.path.join(file_path, "*.txt")))

fig, ax = plt.subplots()
plt.title("Polymer: RS93 (8%) in DMF, laser power: 200 mW, objective: 40x", fontsize=11.5)

periods = [0.8, 1.7, 2.5, 3.4, 4.2, 5]

for i, path in enumerate(file_path_list):
    p_x, p_y, v_x, v_y = get_data(path)

    p_x = np.array(p_x) * u.m
    p_y = (np.array(list(p_y)) * u.m).to(u.nm)

    v_x = np.array(v_x) * u.m
    v_y = (np.array(list(v_y)) * u.m).to(u.nm)

    height = p_y - v_y

    dist_to_time_factor = 3.3
    x_time = ((p_x.to(u.um).value * dist_to_time_factor) * u.s).to(u.min)

    plt.plot(x_time, height, label=f"period:{periods[i]}µm")
plt.ylabel(f'height ({p_y.unit})')
plt.legend()
plt.xlabel(f'Δ illumination time ({x_time.unit})')
fig.tight_layout()
plt.show()