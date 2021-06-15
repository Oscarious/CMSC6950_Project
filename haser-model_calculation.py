# Top Level imports
import numpy as np
import astropy.units as u
from sbpy.activity import gas

# Calculate the Haser model column density from 1 to  1e04  km for CO2  at 1 au, produced at a rate of  1e28 /s. Let the expansion velocity be 0.8 km/s.
Q = 1e28 / u.s  # CO2 production rate
v = 0.8 * u.km / u.s  # gas radial expansion speed

rh = 1.0 * u.au  # heliocentric distance
tau = gas.photo_timescale('CO2', source='CE83') # Crovisier & Encrenaz 1983
gamma = v * tau * (rh / u.au)**2
print('lengthscale = {:.0g}\n'.format(gamma))

co2 = gas.Haser(Q, v, gamma)

for rho in 10**np.arange(0, 5) * u.km:  # projected radial distance from the nucleus
    print('{:10.1f} {:10.2e}'.format(rho, co2.column_density(rho)))