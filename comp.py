import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.optimize import curve_fit
from astropy import units as u
from matplotlib.offsetbox import AnchoredText


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

p_x_dmf, _, _, _, height_dmf = get_data(r"C:\Users\Mika Music\Nextcloud\Data\#AFM\260918_ssh_komplett\analyzed\rs93\rs93_42.txt")
p_x_methanol, _, _, _, height_methanol = get_data(r"C:\Users\Mika Music\Nextcloud\Data\#AFM\260918_ssh_komplett\analyzed\rs93_methanol\rs93_m_42.txt")

dist_to_time_factor = 3.3
x_time_dmf = ((p_x_dmf.to(u.um).value * dist_to_time_factor) * u.s).to(u.min)
x_time_methanol = ((p_x_methanol.to(u.um).value * dist_to_time_factor) * u.s).to(u.min)

fig, ax = plt.subplots()
plt.title("Polymer: RS93, Periode: 5 µm, laser power: 200 mW, objective: 40x")
plt.plot(x_time_dmf, height_dmf, label="dmf")
plt.ylabel(f'height ({height_dmf.unit})')
plt.legend(loc="lower right")
plt.plot(x_time_methanol, height_methanol, label="methanol")
plt.legend()
plt.xlabel(f'Δ illumination time ({x_time_dmf.unit})')

fig.tight_layout()

plt.show()