# top level imports
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import sys
import os
from astropy.time import Time
from sbpy.data import Ephem, Orbit

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
    for label, orb in zip((target_id, 'Earth', 'Jupiter'),
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
    if 'src' in os.listdir():
        plt.savefig("images/orbit.png")
    else:
        plt.savefig("../images/orbit.png")

if __name__ == '__main__':
    if len(sys.argv) != 4 and len(sys.argv) != 1:
        print("Usage: python {} <target_id> <target_type> <time>".format(sys.argv[0]))
        print("default: python {} 46P designation 2007-12-08".format(sys.argv[0]))
        exit(1)
    # set default arguments, besides the input planet we also care about the Erth and Jupyter.
    obs_dates = {
        'spitzer': Time(['2008-12-10']),
        'bass': Time('2018-12-10')
    }
    target_id = '46P'
    target_type = 'designation'
    # set user's custom arguments
    if len(sys.argv) == 2:
        target_id = sys.argv[1]
        target_type = sys.argv[2]
        obs_dates['spitzer'] = sys.argv[3]

    epochs = (obs_dates['spitzer'].jd.mean(), obs_dates['bass'].jd)
    comet = Orbit.from_horizons(target_id, target_type, epochs=epochs,
                                closest_apparition=True)

    epochs = obs_dates['bass']
    planets = Orbit.from_horizons((399, 599), 'majorbody', epochs=epochs)

    # inspect the result
    print(comet, planets)
    print(comet.field_names)

    main()