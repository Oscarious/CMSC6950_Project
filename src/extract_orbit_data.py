# top level imports
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from sbpy.data import Ephem, Orbit


# Define the dates of interest and retrieve orbits for Earth, Jupiter, and the comet in 2018.  For the comet, we'll also want the perihelion date in 2008.
obs_dates = {
    'spitzer': Time(['2007-12-08', '2008-01-17', '2008-04-24',
                     '2008-05-24', '2008-07-02']),
    'bass': Time('2018-12-10')
}

epochs = (obs_dates['spitzer'].jd.mean(), obs_dates['bass'].jd)
comet = Orbit.from_horizons('46P', 'designation', epochs=epochs,
                            closest_apparition=True)

epochs = obs_dates['bass']
planets = Orbit.from_horizons((399, 599), 'majorbody', epochs=epochs)

# inspect the result
print(comet, planets)
print(comet.field_names)