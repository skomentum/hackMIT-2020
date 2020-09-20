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
import errno
import os

import numpy as np
import pandas as pd
import skyfield
from matplotlib import pyplot as plt
from skyfield import almanac, api, data
import astropy
from astropy import units as u
from astropy.coordinates import SkyCoord
from skyfield.starlib import Star


def get_stars(zip_code, date_utc) -> list:
    """
    :rtype: list
    :param zip_code:  user zip code or coordinates
    :param date_utc:  current time in UTC
    :return:          returns a df of the bright stars
    """

    load = api.Loader('./tmp/data')

    manhattan_beach = api.Topos('33.881519 S', '118.388177 W')      # TODO change location

    ephemeris = load('de421.bsp')   # download JPL ephemeris
    earth = ephemeris['earth']

    with load.open(data.hipparcos.URL) as f:
        df = data.hipparcos.load_dataframe(f)

    bright = df[df['magnitude'] <= 5.5]  # don't know what this does tbh

    ts = load.timescale()
    t = ts.utc(2020, 12, 20)                         # TODO set the date here

    df = df[df['ra_degrees'].notnull()]         # remove nulls values

    bright = df[df['magnitude'] <= 5.5]                 # Prevent apparent magnitude from being greater than 5.5
    bright_stars = api.Star.from_dataframe(bright)

    astrometric = earth.at(t).observe(bright_stars)
    ra, dec, distance = astrometric.radec()

    # ra.hours, dec.degrees, & distance.au returns ndarrays
    ra_array = ra.hours.tolist()
    dec_array = dec.degrees.tolist()
    distance_array = distance.au.tolist()

    apparent_magnitude_array = []

    for row_label, row in bright.iterrows():
        # grab magnitudes of stars
        apparent_magnitude_array.append(row[0])

    orig = []
    for i in range(len(ra_array)):
        orig.append([apparent_magnitude_array[i], ra_array[i], dec_array[i], distance_array[i]])

    sorted_list = []
    for i in range(len(orig)):
        n = 0
        inserted = False
        while n < len(sorted_list) and not inserted:
            if orig[i][2] <= sorted_list[n][2]:
                # shift items after index n and insert curr at n
                sorted_list.insert(n, orig[i])
                inserted = True
            else:
                n += 1

        if not inserted:  # curr has not been inserted in sorted_list yet - will be inserted at the end (x is largest)
            sorted_list.append(orig[i])
    return sorted_list
