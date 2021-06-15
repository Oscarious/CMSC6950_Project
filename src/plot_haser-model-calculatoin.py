# plot the distribution of CO2
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from sbpy.activity import gas
import pandas as pd
fig = plt.figure(1)
fig.clear()
ax = fig.gca()

rho = np.logspace(4, 7) * u.km
Q = 1e28 / u.s  # CO2 production rate
v = 0.8 * u.km / u.s  # gas radial expansion speed
tau = gas.photo_timescale('CO2', source='CE83') # Crovisier & Encrenaz 1983

for rh in np.arange(1, 11, 2) * u.au:
    gamma = v * tau * (rh / u.au)**2
    co2 = gas.Haser(Q, v, gamma)
    ax.plot(rho, co2.column_density(rho), label='{:.1f}'.format(rh))

plt.setp(ax, xlabel='Radial distance (km)', xscale='log',
         ylabel='Column density (m$^{-2}$)', ylim=(1e12, 1e18), yscale='log')
ax.legend()
plt.tight_layout()
plt.savefig("../image/haser.png")