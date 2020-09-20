"""
MIT License

Copyright (c) 2019 Bradley P. Allen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import pandas as pd
import skyfield
from matplotlib import pyplot as plt
from skyfield import almanac, api, data
import astropy
from astropy import units as u
from astropy.coordinates import SkyCoord
from skyfield.starlib import Star


def get_stars(zip_code, date_utc):
    """
    :param zip_code:  user zip code or coordinates
    :param date_utc:  current time in UTC
    :return:          returns a df of the bright stars
    """
    load = api.Loader('./data')     # put the data here
    manhattan_beach = api.Topos('33.881519 S', '118.388177 W')      # example location

    ephemeris = load('de421.bsp')   # download JPL ephemeris
    earth = ephemeris['earth']

    ts = load.timescale()
    t = ts.utc(2001, 1, 1)            # date is today

    with load.open(data.hipparcos.URL) as f:
        df = data.hipparcos.load_dataframe(f)

    barnards_star = Star.from_dataframe(df.loc[87937])

    astrometric = earth.at(t).observe(barnards_star)
    ra, dec, distance = astrometric.radec()
    print(ra)
    print(dec)

    bright = df[df['magnitude'] <= 5.5]                 # Prevent apparent magnitude from being greater than 5.5
    bright_stars = api.Star.from_dataframe(bright)

    t = ts.now()    # change the date here
    astrometric = earth.at(t).observe(bright_stars)
    ra, dec, distance = astrometric.radec()

    # ra.hours, dec.degrees, & distance.au returns ndarrays
    ra_array = ra.hours.tolist()
    dec_array = dec.degrees.tolist()
    distance_array = distance.au.tolist()

    # grab magnitudes of stars
    print(bright.describe())

    print(ra_array)
    print(dec_array)
    print(distance_array)

    return transform_stars(bright)


def transform_stars(df):
    """
    Transform the dataset
    :param df:  dataframe containing bright stars
    :return:    returns a two-dimensional list
                    [magnitude, ra_degrees, dec_degrees]
            will be [magnitude, x-coord, y-coord]
    """
    # Remove additional data from the star file
    df = df.drop(columns=['parallax_mas', 'ra_mas_per_year', 'dec_mas_per_year', 'ra_hours', 'epoch_year'])

    out = []    # list with sorted cartesian coords that will be returned
    for row_label, row in df.iterrows():
        n = 0
        inserted = 0
        while n < len(out) and inserted == 0:
            if row[1] <= out[n][1]:
                # shift items after index n and insert curr at n
                out.insert(n, [row[0], row[1], row[2]])
                inserted = 1
            else:
                n += 1

        if inserted == 0:               # curr has not been inserted in out yet - will be inserted at the end
            out.append([row[0], row[1], row[2]])

    print(out)
    return ""
