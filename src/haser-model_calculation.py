# Top Level imports
import numpy as np
import astropy.units as u
import pickle as pk
from sbpy.activity import gas

Q = 1e28 / u.s  # CO2 production rate
v = 0.8 * u.km / u.s  # gas radial expansion speed

rh = 1.0 * u.au  # heliocentric distance
tau = gas.photo_timescale('CO2', source='CE83') # Crovisier & Encrenaz 1983
rho = np.logspace(4, 7) * u.km

res = {'rho': rho}

data = []
for rh in np.arange(1, 11, 2) * u.au:
    gamma = v * tau * (rh / u.au)**2
    co2 = gas.Haser(Q, v, gamma)
    data.append({'rh' : rh, 'cds': co2.column_density(rho)})
res['data'] = data

with open('haser_ds', 'wb') as f:
    pk.dump(res, f)