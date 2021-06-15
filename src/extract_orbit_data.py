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

# Define some plotting functions
# Plot the full orbit
def plot_orbit(ax, orb, **plot_kwargs):
    """Orthographic projection onto the xy plane.

    2-body propagation of orbital elements, neglecting non-grav forces.

    """
    epochs = orb['epoch'] + np.linspace(-1, 1, 1000) * orb['P'] / 2
    eph = Ephem.from_oo(orb, epochs=epochs, dynmodel='2')
    ax.plot(eph['x'].value, eph['y'].value, **plot_kwargs)

# top level imports
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from sbpy.data import Ephem, Orbit

# Plot the positions of the object at particular dates
def plot_object(ax, orb, epochs, **plot_kwargs):
    """Same as plot_orbit, but for single points."""
    eph = Ephem.from_oo(orb, epochs=epochs, dynmodel='2')
    ax.scatter(eph['x'].value, eph['y'].value, **plot_kwargs)

def main():
    fig = plt.figure(1, (8, 8))
    fig.clear()
    ax = fig.gca()

    # H and G required for openorb's propagation
    comet['H'] = 0
    comet['G'] = 0.15
    planets['H'] = 0
    planets['G'] = 0.15

    # orbits
    for label, orb in zip(('46P/Wirtanen', 'Earth', 'Jupiter'),
                        (comet[1], planets[0], planets[1])):
        plot_orbit(ax, orb, label=label)

    Tp08 = Time(comet[0]['Tp'], format='jd', scale='tt')
    Tp19 = Time(comet[1]['Tp'], format='jd', scale='tt')

    # comet in 2008 (approximated with 2019 elements)
    TmTp = obs_dates['spitzer'] - Tp08
    epochs = (TmTp + Tp19)  # Julian Dates as a work around Issue #206
    print(epochs)
    plot_object(ax, comet[1], epochs, label='Spitzer epochs', zorder=99)

    # comet in 2019
    plot_object(ax, comet[1], obs_dates['bass'], label='BASS epoch', zorder=99)

    plt.setp(ax, xlabel='X (au)', ylabel='Y (au)')
    plt.legend()
    plt.savefig("../image/orbit.png")

if __name__ == '__main__':
    main()