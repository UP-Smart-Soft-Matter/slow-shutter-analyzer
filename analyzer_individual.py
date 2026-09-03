import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.optimize import curve_fit
from astropy import units as u
from matplotlib.offsetbox import AnchoredText


def get_data(filepath):
    x = []
    y = []
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))

    return x, y

def linear(x, a, b):
    return a * x + b

x, y = get_data(r'C:\Users\Mika Music\Nextcloud\Data\260903_rene_polymer_groth_rate\2%_rs239.txt')

x = np.array(x) * u.m
y = (np.array(list(reversed(y))) * u.m).to(u.nm)

dist_to_time_factor = 40
x_time = ((x.to(u.um).value * dist_to_time_factor) * u.s).to(u.min)

fit, _ = curve_fit(linear, x_time.value, y.value)
fit2, _ = curve_fit(linear, x_time.to(u.s).value, y.value)
print(f"steigung: {fit2[0]:.3f} nm/s")
fig, ax = plt.subplots()
ax.plot(x_time, y, label="data")
# ax.plot(x_time, linear(x_time.value, fit[0], fit[1]), label="linear fit: a={:.3f}, b={:.3f}".format(fit[0], fit[1]))
plt.xlabel(f'illumination time ({x_time.unit})')
plt.ylabel(f'srg height ({y.unit})')
# plt.legend()
text_box = AnchoredText(
    f"polymer: RS-239 (8%)\nlaser Power: 200 mW\nobjective lens: 40x",
    # f"\ngroth rate: {fit2[0]:.3f} {y.unit}/s",
    loc="upper left",
    prop=dict(size=12),
    frameon=True
)
fig.tight_layout()
ax.add_artist(text_box)
plt.show()