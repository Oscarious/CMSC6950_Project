# plot the distribution of CO2
from astropy.table import column
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from sbpy.activity import gas
import pandas as pd
import pickle as pk
import os

fig = plt.figure(1)
fig.clear()
ax = fig.gca()

with open('haser_ds', 'rb') as f:
    res = pk.load(f)
rho = res['rho']
data = res['data']

for entry in data:
    rh = entry['rh']
    column_density = entry['cds']
    ax.plot(rho, column_density, label='{:.1f}'.format(rh / u.au))

plt.setp(ax, xlabel='Radial distance (km)', xscale='log',
         ylabel='Column density (m$^{-2}$)', ylim=(1e12, 1e18), yscale='log')
ax.legend()
plt.tight_layout()
if 'src' in os.listdir():
    plt.savefig("images/haser.png")
else:
    plt.savefig("../images/haser.png")