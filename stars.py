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
from matplotlib import pyplot as plt
from skyfield import almanac, api, data
import astropy


def get_stars(zip_code, date_utc) -> list:
    """
    :rtype: list
    :param zip_code:  user zip code or coordinates
    :param date_utc:  current time in UTC
    :return:          returns a df of the bright stars
    """

    load = api.Loader('./tmp/data')
    # put the data here
    manhattan_beach = api.Topos('33.881519 N', '118.388177 W')  # example location

    ts = load.timescale()
    ephemeris = load('de421.bsp')  # download JPL ephemeris

    with load.open(data.hipparcos.URL) as f:
        df = data.hipparcos.load_dataframe(f)

    earth = ephemeris['earth']
    t = ts.now()  # date is today

    bright = df[df['magnitude'] <= 5.5]  # don't know what this does tbh
    bright_stars = api.Star.from_dataframe(bright)

    t = ts.now()
    astrometric = earth.at(t).observe(bright_stars)
    ra, dec, distance = astrometric.radec()

    observer = earth + manhattan_beach

    return transform_stars(bright)


def transform_stars(df):
    """
    :param df:  dataframe containing bright stars
    :return:    returns a two-dimensional list
                    [magnitude, ra_degrees, dec_degrees]
    """
    # Remove additional data from the star file
    df = df[df['ra_degrees'].notnull()]
    df = df.drop(columns=['parallax_mas', 'ra_mas_per_year', 'dec_mas_per_year', 'ra_hours', 'epoch_year'])
    out = []
    for row_label, row in df.iterrows():
        out.append([row[0], row[1], row[2]])
    return out
