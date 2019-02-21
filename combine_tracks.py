#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 devon <devon@devon-XPS-13-9370>
#
# Distributed under terms of the MIT license.
"""
Combines multiple kmls.
"""

from __future__ import print_function
import argparse
import math
import os
import sys
import xml.etree.ElementTree as ET

COORDINATES_XPATH = ("{http://www.opengis.net/kml/2.2}Document" +
                     "/{http://www.opengis.net/kml/2.2}Placemark" +
                     "/{http://www.opengis.net/kml/2.2}LineString" +
                     "/{http://www.opengis.net/kml/2.2}coordinates")


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'inputs',
        help="""Input kml files, comma separated. The order of the
        input files is preserved in the merged output.""",
        type=str)
    parser.add_argument(
        'sample_rate',
        help="""Comma-separated list of downsampling rates, corresponding to
        each input. If <=1, the fraction of points to preserve, otherwise the
        number of points to keep.""",
        type=str)

    args = parser.parse_args(arguments)

    inputs = args.inputs.split(',')
    rates = args.sample_rate.split(',')

    if len(inputs) != len(rates):
        raise ValueError(
            "Exactly one sampling rate must be provided for each input.")

    ET.register_namespace('', 'http://www.opengis.net/kml/2.2')
    # Get metadata from first input
    if len(inputs) < 1:
        raise ValueError("Must provide at least one input.")

    # Combine all input points
    points = ""
    for i in range(len(inputs)):
        points += extract_points(ET.parse(inputs[i]), float(rates[i]))
    tree = ET.parse(inputs[0])
    tree.getroot().find(COORDINATES_XPATH).text = points
    tree.write(sys.stdout)


def extract_points(kml, sample_rate):
    points = kml.getroot().find(COORDINATES_XPATH).text
    n = points.count('\n')
    sampled_points = ""
    sample_factor = 1
    if sample_rate <= 1:
        sample_factor = math.floor(1 / sample_rate)
    else:
        sample_factor = math.floor(n / sample_rate)
    sample_factor = max(sample_factor, 1)
    for (i, p) in enumerate(points.splitlines()):
        if i % sample_factor == 0:
            sampled_points += (p + "\n")

    return sampled_points


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
